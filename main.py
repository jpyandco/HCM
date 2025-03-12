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
    hcm_handler = HCMHandler()
    hcm_handler.create_zip("output/" + hcm_handler.dir)
    exit()
    try:
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

    except Exception as e:
        print(e)

    return


if __name__ == "__main__":
    main()
