from datetime import datetime
import os
import zipfile
from db.database_handler import DatabaseHandler
from hcm.const import FILEPREFIX
from hcm.model import HCMHeader, HCMRecord

test_data = {
    "filenumber_medium": 2,
    "filecontent": "SHzgZ3shvZ4unKky3IrN7rgJzW",
    # "filetype": "O",
    # "origin_country": "AUT",
    "email": "ElWSI@example.com",
    "phone": "08464935133887792",
    "fax": "4866832259",
    "person_name": "JoeHeinz",
    "record_count": 648430,
    "creation_date": "07032025",
    # "destination_country": "VPN",
    # "filenumber": 161,
}


class HCMHandler:
    def __init__(self) -> None:
        self.db_handler = DatabaseHandler()
        self.incorrect_dataset = []
        self.dir = FILEPREFIX + self.get_current_quarter() + str(datetime.now().year)

        # folder path, file name, zip name as init params from gui?

    def write_to_file(self, file_name, input):

        # directory_path = FILEPREFIX + self.get_current_quarter() + str(datetime.now().year)
        folder = "output/" + self.dir
        self.create_dir(folder)
        folder += "/"
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

    def create_file(self, table: str) -> str:
        """For multiprocessing. Handles the actual file processing/creation."""
        header = HCMHeader(**test_data)
        header = header.serialize_model()

        result = self.db_handler.select_from_db(table)
        data = ""

        if result[0]:
            print(table)
            print(result[0])
        try:
            for entry in result:

                bobo = HCMRecord(**entry)
                data += "\n" + bobo.serialize_model()  # "\n" + for testing, to make files more readable
        except Exception as e:
            self.incorrect_dataset.append({entry.get("userlabel"): entry, "error": e})
            print(e)
            print(f"Error for userlabel: {entry.get("userlabel")} in Table {table}")

        return header + data

    def create_dir(self, directory_path):
        # directory_path = FILEPREFIX + self.get_current_quarter() + datetime.now().year

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f"Directory '{directory_path}' created.")
        else:
            print(f"Directory '{directory_path}' already exists.")

    def create_zip(self, directory_path):
        print(self.dir)
        print(directory_path)
        output_file = f"{directory_path}/{self.dir}.zip"
        with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file in os.listdir(directory_path):
                file_path = os.path.join(directory_path, file)
                if os.path.isfile(file_path) and ".zip" not in file:
                    zipf.write(file_path, file)

        return

    def create_error_report(self):
        if self.incorrect_dataset:
            pass
        return
