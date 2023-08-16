from ld_audit.report import Report

from dotenv import load_dotenv


def main():
    report = Report(csv_file="./reports/audit_log.csv")
    report.fetch_data()
    report.write_items_to_csv_file()


if __name__ == "__main__":
    load_dotenv()
    main()
