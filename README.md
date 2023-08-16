# LD Audit

This script creates a CSV file from LaunchDarkly audit log events, which can then be queried or analyzed to derive usage
data.

## Setup

First, you'll need a [LaunchDarkly API token](https://docs.launchdarkly.com/home/account-security/api-access-tokens) for
the account you want to query.

Copy/rename the `.env.example` file to `.env` and set your API token as the value for the `LD_API_TOKEN` environment
variable.

Install dependencies by creating a virtual environment:

```shell
python -m venv venv
source bin/venv/activate
pip install -r requirements.txt
```

Once the dependencies have finished installing, run the report creator script:

```shell
python main.py
```

## Things you might want to change

### Time range for events in the report

The start and end times for logs to be retrieved are set in the `ld_audit.data_fetcher` module. Look for the
variables `LOG_ENTRIES_START` and `LOG_ENTRIES_END`. Each of these must be a Unix timestamp in milliseconds.

### Format or fields included in CSV file

This is controlled by the `LogEntry.to_dict` method, found in the `ld_audit.log_entry` module. This method returns a
plain Python dictionary that is later used to create a row in the CSV file.

### Writing behavior

Writing to the CSV file is handled by the `Report` class, found in the `ld_audit.report` module.

The destination file for the written report is set in `main.py` when instantiating the report object.

### Data fetching behavior

The `DataFetcher` class is responsible for fetching data from the LaunchDarkly API. It is a component of a `Report`, and
passes data back to the report via its `get_all_audit_logs` method, which is used by the report as a generator so that
it can write log entries to the file as they are received.

All logic happens in the `get_all_audit_logs` method. To change the actual API call that is being made, look for the
call to `self.api_client.get_audit_log_entries`. For more info on what can be done here, see the documentation for the
[Python API client](https://github.com/launchdarkly/api-client-python).

## FAQ

### What kind of data does the audit log API return?

The API returns a list of events that happened in a LaunchDarkly account, along with metadata about those events. For
example, an event might be someone creating a flag. In this case, the metadata would be things like the name of the
flag, its key, who made the change, etc.

For a full list of events captured by the audit log, see
the [LaunchDarkly docs](https://docs.launchdarkly.com/home/flags/audit-log-history#actions-recorded-in-the-audit-log-and-history-tabs).

### How long does this thing take to run?

This will vary, but it was tested against an account with about 62000 audit log events in the last 30 days. During this
test it took about 15 minutes to complete the CSV report.

### Why does it take that long?

The audit log API does not have a pagination feature. To work around this, we use the date of the last item in each
response, in combination with the absolute start time to create a new "time range" for the next request. In order for
this to work, requests must be made and processed sequentially. Sorry, no async!

