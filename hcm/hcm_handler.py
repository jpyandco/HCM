from configparser import ConfigParser
from datetime import datetime
import json
import os
import time
import zipfile

from pydantic import ValidationError
from db.database_handler import DatabaseHandler
from hcm.const import CONFIG, FILEPREFIX


class HCMHandler:
    def __init__(self, file_headers: dict) -> None:
        self.db_handler = DatabaseHandler()
        self.incorrect_dataset = []
        self.file_headers = file_headers
        self.config = ConfigParser()
        self.config.read(CONFIG)

        self.prefix_dir = self.config["Path"]["folder_path"] + "\\"
        self.dir_path = self.prefix_dir + FILEPREFIX + self.get_current_quarter() + str(datetime.now().year)
        self.dir = FILEPREFIX + self.get_current_quarter() + str(datetime.now().year)
        self.report_file = self.dir_path + "/" + "Report.json"
        self.total_records: int = 0
        self.file_number: int = 0

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
