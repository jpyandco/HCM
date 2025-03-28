from configparser import ConfigParser
from datetime import datetime
import json
from pydantic import ValidationError

from db.database_handler import DatabaseHandler
from hcm.const import CONFIG, FILEPREFIX
from hcm.hcm_handler import HCMHandler
from hcm.model import Antenna, Coordination, HCMHeader, HCMRecord, RadioStation, ReceiverStation, Remarks

# TODO create HCMHanlderBaseclass and inherit to this class and old hcm_handler


class HCMHandlerNew(HCMHandler):
    def __init__(self, file_headers: dict) -> None:
        super().__init__(file_headers)

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
                result = self.db_handler.select_from_db(table)
                # print("DB DATA:", result)
                data = self.new_format(table, file_name, result)
                # print("DATA: ", data)
                self.write_to_file_new(file_name, data)

            incorrect_data = self.incorrect_dataset

            print(f"Incorrect Datasets: {len(incorrect_data)}\n")
            for data in self.incorrect_dataset:
                # print(data, "\n")
                pass

            self.create_zip()
            self.create_report()

        except Exception as e:
            print(e)

    def new_format(self, table: str, file_name: str, data: list[dict]):
        # result = self.db_handler.select_from_db(table)
        # move out of func and pass as parameter

        # data = ""
        record_count = 0
        self.file_number += 1
        records = []
        complete_data = None
        unique_id = []
        # print("results", data)

        for entry in data:
            try:
                record = HCMRecord(**entry)
                validated_record = dict(record)
                if record.field_13X in unique_id:
                    continue
                unique_id.append(record.field_13X)
                # print(validated_record)
                radio_station = RadioStation(**validated_record)
                antenna = Antenna(**validated_record)
                reciever_station = ReceiverStation(**validated_record)
                coordination = Coordination(**validated_record)
                remarks = Remarks(**validated_record)
                self.total_records += 1
                record_count += 1
                dic = {
                    radio_station.object_name: radio_station.model_dump(),
                    antenna.object_name: antenna.model_dump(),
                    reciever_station.object_name: reciever_station.model_dump(),
                    coordination.object_name: coordination.model_dump(),
                    remarks.object_name: remarks.model_dump(),
                }

                records.append(dic)

            except ValidationError as e:
                lst = self.format_exception(e)

                self.incorrect_dataset.append({entry.get("userlabel"): entry, "table": table, "Error": lst})
                print(f"Error for userlabel: {entry.get("userlabel")} in Table {table}")
                print("validated_record", validated_record)
            except Exception as e:
                self.incorrect_dataset.append({entry.get("userlabel"): entry, "table": table, "Error": str(e)})
                print(e)
                print(f"Error for userlabel: {entry.get("userlabel")} in Table {table}")  #
                print("validated_record", validated_record)
                # print(dic)

        header = self.create_headers(file_name, record_count)
        print("HEADER:", header)
        complete_data = {"header": header, "content": records}

        return complete_data

    def create_headers(self, file_name, record_count):
        headers = self.file_headers
        headers["record_count"] = record_count
        headers["creation_date"] = datetime.now().strftime("%d%m%Y")
        headers["filenumber_medium"] = self.file_number
        headers["filecontent"] = file_name

        # print(headers)

        header = HCMHeader(**headers)
        header = dict(header)

        return header

    def write_to_file_new(self, file_name, data: dict):
        folder = self.dir_path + "/"

        with open(folder + file_name + ".json", "w") as file:
            file.write(json.dumps(data, indent=4))

        print(f"\nFILE {file_name} written!\n")
