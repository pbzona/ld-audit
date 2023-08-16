import os

import launchdarkly_api as ld
from launchdarkly_api.api import audit_log_api
from ld_audit.log_entry import LogEntrySeparator
from ld_audit.utils import get_timestamp_for_n_days_ago, get_timestamp_for_now

# This is the highest number of audit log entries that can be
# requested at once. Static value, do not change.
MAX_LOG_ENTRY_LIMIT = 20

# Timestamp at which to start log entries
LOG_ENTRIES_START = get_timestamp_for_n_days_ago(30)
# Timestamp up until which to collect logs
LOG_ENTRIES_END = get_timestamp_for_now()

default_api_key = os.environ.get("LD_API_TOKEN")


class DataFetcher:
    def __init__(self, project_key="", api_key=default_api_key):
        self.config = ld.Configuration()
        self.config.api_key["ApiKey"] = api_key
        if project_key:
            self.project_key = project_key
        self.report = None
        self.still_returning_results = True
        self.next_date = LOG_ENTRIES_END

        with ld.ApiClient(self.config) as api_client:
            self.api_client = audit_log_api.AuditLogApi(api_client)

    def get_all_audit_logs(self):
        if not self.report:
            raise RuntimeError("No report set for the DataFetcher object")

        print("Requesting audit log events from LaunchDarkly API...")
        next_date = get_timestamp_for_now()

        iteration = 0

        while self.still_returning_results:
            # Give status update every seventeenth iteration
            # There is no significance to this number, just works out to be reasonable timing
            if iteration % 17 == 0:
                print(f"Still working... {self.report.log_count} events processed")

            iteration += 1

            # Get the audit log entries from the API
            try:
                response = self.api_client.get_audit_log_entries(
                    before=next_date,
                    after=LOG_ENTRIES_START,
                    limit=MAX_LOG_ENTRY_LIMIT,
                )
            except ld.ApiException as e:
                e.body = e.body.decode("utf-8")
                raise e

            # If there are less than the max number of entries possible on the page,
            # this is the last page so stop returning after this iteration
            if len(response["items"]) < MAX_LOG_ENTRY_LIMIT:
                self.still_returning_results = False

            # Process the resources affected by the actions in this audit log event
            # Returns a list of LogEntry objects that will be identical except for the
            # resource and action fields. Can use id to correlate these objects together
            for item in response["items"]:
                log_entries = LogEntrySeparator(item)
                entries = log_entries.get_entries()

                # Break and exit if the date is before the specified start date
                if entries[0].get_date() < LOG_ENTRIES_START:
                    self.still_returning_results = False
                    break

                # Give the entries collected in this iteration back to the Report
                # so they can be written to a file
                yield entries

                # Use the date of the last item in the list to define "before"
                # when retrieving the next page of results
                next_date = entries[-1].get_date()

    def set_report(self, report):
        self.report = report
