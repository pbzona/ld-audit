from datetime import datetime


class LogEntrySeparator:
    def __init__(self, entry):
        self.log_entries = []
        for access in entry["accesses"]:
            try:
                log_entry = LogEntry(entry, access)
                self.log_entries.append(log_entry)
            except KeyError as e:
                print("Error parsing log entry: ", e)

    def get_entries(self):
        return self.log_entries


class LogEntry:
    def __init__(self, entry, access):
        member = {"email": "n/a", "first_name": "n/a", "last_name": "n/a"}

        if "member" in entry:
            member = entry["member"]

        self.user_email = member["email"]
        self.user_first_name = member["first_name"]
        self.user_last_name = member["last_name"]

        self.action = access["action"]
        self.resource = access["resource"]

        self.date = entry["date"]
        self.kind = entry["kind"]
        self.name = entry["name"]
        self.description = entry.description.replace("\n", "").replace(",", "")
        self.id = entry["id"]

    def keys(self):
        return vars(self)

    def get_date(self):
        return self.date

    def get_formatted_date(self):
        return datetime.fromtimestamp(self.date / 1000).strftime("%Y-%m-%d %H:%M:%S")

    # Return a plain dictionary representation of the object
    # This is what gets written to the CSV file
    # The keys on this object represent headers in the CSV, so to add or change
    # what gets logged, make those changes here
    def to_dict(self):
        return {
            "user_email": self.user_email,
            "user_first_name": self.user_first_name,
            "user_last_name": self.user_last_name,
            "date": self.date,
            "formatted_date": self.get_formatted_date(),
            "kind": self.kind,
            "name": self.name,
            "action": self.action,
            "resource": self.resource,
            "description": self.description,
            "id": self.id,
        }

    def __getitem__(self, item):
        print(item)
        return self[item]
