import configparser

from pydantic import BaseModel
from db.database_handler import DatabaseHandler
from hcm import HCMRecord, HCMHeader
import csv
from datetime import datetime
from hcm.const import CONFIG, FILEPREFIX, FILETYPE
from hcm.hcm_handler import HCMHandler

CSV_DELIMITER = ";"
CSV_ENCODING = "utf-8-sig"

HCM_FIELD_PREFIX = "field_"
# every entry/row has to be 219 bytes(characters) long
LENGHT = 219


def main():
    # move to HCMHandler
    config = configparser.ConfigParser()
    config.read(CONFIG)
    tech = []
    tables = []
    for k, v in config.items("Tables"):
        tech.append(k)
        tables.append(v)

    hcm_handler = HCMHandler()
    for table, entry in zip(tables, tech):
        data = hcm_handler.create_file(table)
        file_name = hcm_handler.get_file_name(entry)
        hcm_handler.write_to_file(file_name, data)

    incorrect_data = hcm_handler.incorrect_dataset

    print(f"Incorrect Datasets: {len(incorrect_data)}\n")
    for data in hcm_handler.incorrect_dataset:
        print(data, "\n")

    # for entry in

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


# def write_to_file(file_name, input):

#     folder = "output/"
#     # filename = "basemodel_test"
#     with open(folder + file_name, "w") as file:
#         file.write(input)

#     print(f"\nFILE {file_name} written!\n")


# def get_current_quarter():
#     """Returns current quarter and year in format Q1_2025"""
#     now = datetime.now()
#     year = now.year
#     month = now.month
#     quarter = (month - 1) // 3 + 1
#     return f"Q{quarter}_"  # {year}"


# def get_file_name(tech: str):
#     current_date = datetime.now()
#     # Format the date as yyyymmdd
#     formatted_date = current_date.strftime("%Y%m%d")
#     quarter = get_current_quarter()
#     name = f"{FILEPREFIX}{quarter}{tech.upper()}_{formatted_date}"

#     return name


# def create_file(table: str) -> str:
#     """For multiprocessing. Handles the actual file processing/creation."""
#     db_handler = DatabaseHandler()
#     header = HCMHeader(**test_data)
#     header = header.serialize_model()
#     incorrect_dataset = []

#     result = db_handler.select_from_db(table)
#     data = ""

#     if result[0]:
#         print(table)
#         print(result[0])
#     try:
#         for entry in result:

#             bobo = HCMRecord(**entry)
#             data += "\n" + bobo.serialize_model()  # "\n" + for testing, to make files more readable
#     except Exception as e:
#         # move to class, save in instance variable
#         incorrect_dataset.append({entry.get("userlabel"): entry})
#         print(e)
#         print(f"Error for userlabel: {entry.get("userlabel")} in Table {table}")

#     return header + data


if __name__ == "__main__":
    main()
