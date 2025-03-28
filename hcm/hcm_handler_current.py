from configparser import ConfigParser
from datetime import datetime
import os
import zipfile

from pydantic import ValidationError
from db.database_handler import DatabaseHandler
from hcm.const import CONFIG, FILEPREFIX
from hcm.model import Antenna, Coordination, HCMHeader, HCMRecord, RadioStation, ReceiverStation, Remarks
import json

test_data = {
    "filenumber_medium": 0,
    "filecontent": "",
    # "filetype": "O",
    # "origin_country": "AUT",
    "email": "",
    "phone": "",
    "fax": "",
    "person_name": "JoeHeinz",
    "record_count": 648430,
    "creation_date": "07032025",
    # "destination_country": "VPN",
    # "filenumber": 161,
}


class HCMHandlerCurrent:
    def __init__(self, file_headers: dict) -> None:
        self.db_handler = DatabaseHandler()
        self.incorrect_dataset = []
        self.file_headers = file_headers

        self.prefix_dir = "output/"
        self.dir_path = self.prefix_dir + FILEPREFIX + self.get_current_quarter() + str(datetime.now().year)
        self.dir = FILEPREFIX + self.get_current_quarter() + str(datetime.now().year)
        self.report_file = self.dir_path + "/" + "Report.json"
        self.total_records: int = 0
        self.file_number: int = 0

        # folder path, file name, zip name as init params from gui?

    def process(self):
        try:
            config = ConfigParser()
            config.read(CONFIG)
            tech = []
            tables = []

            for k, v in config.items("Tables"):
                tech.append(k)
                tables.append(v)

            self.create_dir(self.dir_path)
            # pass file_numer to create_file for multiproc
            for table, entry in zip(tables, tech):
                file_name = self.get_file_name(entry)
                data = self.create_file(table, file_name)
                self.write_to_file(file_name, data)

            incorrect_data = self.incorrect_dataset

            print(f"Incorrect Datasets: {len(incorrect_data)}\n")
            for data in self.incorrect_dataset:
                print(data, "\n")

            self.create_zip()
            self.create_report()

        except Exception as e:
            print(e)

    def write_to_file(self, file_name, input):

        # directory_path = FILEPREFIX + self.get_current_quarter() + str(datetime.now().year)
        # folder = self.prefix_dir + self.dir

        folder = self.dir_path + "/"
        # filename = "basemodel_test"
        with open(folder + file_name, "w") as file:
            file.write(input)

        print(f"\nFILE {file_name} written!\n")

    def get_current_quarter(self):
        """Returns current quarter and year in format Q1_"""
        now = datetime.now()
        year = now.year
        month = now.month
        quarter = (month - 1) // 3 + 1
        return f"Q{quarter}_"  # {year}"

    def get_file_name(self, tech: str):
        current_date = datetime.now()
        # Format the date as yyyymmdd
        formatted_date = current_date.strftime("%Y%m%d")
        quarter = self.get_current_quarter()
        name = f"{FILEPREFIX}{quarter}{tech.upper()}_{formatted_date}"

        return name

    def create_file(self, table: str, file_name: str) -> str:
        """For multiprocessing. Handles the actual file processing/creation."""

        result = self.db_handler.select_from_db(table)
        data = ""
        record_count = 0
        self.file_number += 1
        unique_id = []

        try:
            for entry in result:
                record = HCMRecord(**entry)
                if record.field_13X in unique_id:
                    continue
                unique_id.append(record.field_13X)
                data += "\n" + record.serialize_model()  # "\n" + for testing, to make files more readable
                self.total_records += 1
                record_count += 1

        except ValidationError as e:
            lst = self.format_exception(e)

            self.incorrect_dataset.append({entry.get("userlabel"): entry, "table": table, "Error": lst})
            print(f"Error for userlabel: {entry.get("userlabel")} in Table {table}")
        except Exception as e:
            self.incorrect_dataset.append({entry.get("userlabel"): entry, "table": table, "Error": str(e)})
            print(e)
            print(f"Error for userlabel: {entry.get("userlabel")} in Table {table}")

        headers = self.file_headers
        headers["record_count"] = record_count
        headers["creation_date"] = datetime.now().strftime("%d%m%Y")
        headers["filenumber_medium"] = self.file_number
        headers["filecontent"] = file_name

        print(headers)

        header = HCMHeader(**headers)
        header = header.serialize_model()

        print(headers)

        # return header + data & incorrect_dataset? better for multiproc
        # return {data: header + data, incorrect_dataset: incorrect_dataset}
        return header + data

    def create_dir(self, directory_path):
        # directory_path = FILEPREFIX + self.get_current_quarter() + datetime.now().year

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f"Directory '{directory_path}' created.")
        else:
            print(f"Directory '{directory_path}' already exists.")

    def create_zip(self):
        print(self.dir)
        output_file = f"{self.dir_path}/{self.dir}.zip"
        print(output_file)
        with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file in os.listdir(self.dir_path):
                file_path = os.path.join(self.dir_path, file)
                if os.path.isfile(file_path) and "." not in file:
                    zipf.write(file_path, file)

        return

    def create_report(self):
        """Creates both error and overview report in one file."""
        report_msg = {
            "Successfully created records": self.total_records,
            "Incorrect records": len(self.incorrect_dataset),
            "Errors": self.incorrect_dataset,
        }

        with open(self.report_file, "w") as file:
            json.dump(report_msg, file, indent=4)

    def format_exception(self, e: ValidationError):
        err_list = e.errors()
        lst = []
        for error in err_list:
            dic = {"Message": error.get("msg") + f", given value from type {str(error.get("input"))}"}
            print("error object", error)
            fields = error.get("loc")
            if len(fields) > 1:
                dic["Fields"] = fields[0]
            else:
                dic["Fields"] = ", ".join(fields)
            lst.append(dic)

        return lst
