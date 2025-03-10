import configparser
from db.database_handler import DatabaseHandler
from hcm import HCMRecord, HCMHeader
import csv
from datetime import datetime
from hcm.const import CONFIG, FILETYPE

CSV_DELIMITER = ";"
CSV_ENCODING = "utf-8-sig"

HCM_FIELD_PREFIX = "field_"
# every entry/row has to be 219 bytes(characters) long
LENGHT = 219

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


def main():
    file_list = ["gsm900"]
    create_file(file_list[0])
    # db_handler = DatabaseHandler()
    # print(db_handler.config["DB"]["user"])

    # header = HCMHeader(**test_data)
    # print(FILETYPE)
    # # print(header)
    # header = header.serialize_model()
    # # print(header)

    # folder = "output/"
    # filename = "testkest2"
    # with open(folder + filename, "w") as file:
    #     file.write(header)

    return


def write_to_file(input):

    folder = "output/"
    filename = "basemodel_test"
    with open(folder + filename, "w") as file:
        file.write(input)


def get_current_quarter():
    """Returns current quarter and year in format Q1_2025"""
    now = datetime.now()
    year = now.year
    month = now.month
    quarter = (month - 1) // 3 + 1
    return f"Q{quarter}_{year}"


def create_file(tech: str):
    """For multiprocessing. Handles the actual file processing/creation."""
    db_handler = DatabaseHandler()
    config = configparser.ConfigParser()
    config.read(CONFIG)
    print(tech)
    print(config["Tables"][tech])
    result = db_handler.select_from_db(config["Tables"][tech])
    print(result[0])
    bobo = HCMRecord(**result[0])
    data = bobo.serialize_model()
    header = HCMHeader(**test_data)
    header = header.serialize_model()
    write_to_file(header + data)
    return


if __name__ == "__main__":
    main()
