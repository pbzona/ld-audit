import csv

from ld_audit.data_fetcher import DataFetcher


class Report:
    def __init__(self, project_key="", csv_file=""):
        self.project_key = project_key
        self.data_fetcher = DataFetcher(project_key)
        self.data_fetcher.set_report(self)

        self.audit_logs = []
        self.log_count = 0

        self.csv_file = csv_file
        self.csv_headers = []

        self.gen = None

        print(f"Created report for project: {self.project_key}")
        print(f"Data will be written to: {self.csv_file}")

    def fetch_data(self):
        self.gen = self.data_fetcher.get_all_audit_logs()

    def set_csv_headers(self, headers):
        self.csv_headers = headers

    def has_received_initial_data(self):
        return len(self.audit_logs) > 0

    def add_audit_logs(self, log_entries):
        self.audit_logs.extend(log_entries)

    def print_exit_message(self):
        print("###########################################")
        print(f"Retrieved {self.log_count} audit log events")
        print(f"Log successfully written to {self.csv_file}")
        print("###########################################")

    def write_items_to_csv_file(self):
        if self.gen is None:
            self.fetch_data()

        try:
            with open(self.csv_file, "w", newline="") as csvfile:
                writer = None
                items = next(self.gen)

                if len(items) > 0 and len(self.csv_headers) == 0:
                    self.log_count += len(items)

                    data_obj = items[0].to_dict()
                    self.set_csv_headers(data_obj.keys())

                    writer = csv.DictWriter(csvfile, fieldnames=self.csv_headers)
                    writer.writeheader()
                while True:
                    log_entries = [log_entry.to_dict() for log_entry in items]
                    writer.writerows(log_entries)
                    items = next(self.gen)
                    self.log_count += len(items)
        except AttributeError as e:
            print("Data could not be written to file: ", e)
        except StopIteration:
            self.print_exit_message()
