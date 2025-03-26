import datetime
import json
from pydantic import ValidationError

from db.database_handler import DatabaseHandler
from hcm.const import FILEPREFIX
from hcm.model import Antenna, Coordination, HCMRecord, RadioStation, ReceiverStation, Remarks

# TODO create HCMHanlderBaseclass and inherit to this class and old hcm_handler


class HCMHandlerNew:
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

    def new_format(self, table: str, file_name, result: list[dict]):
        # result = self.db_handler.select_from_db(table)
        # move out of func and pass as parameter

        data = ""
        record_count = 0
        self.file_number += 1
        records = []
        print("results", result)
        try:
            for entry in result:
                # print("entry", entry)
                record = HCMRecord(**entry)
                # data += "\n" +
                validated_record = dict(record)
                print(validated_record)
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
                print(dic)

        except ValidationError as e:
            # lst = self.format_exception(e)

            # self.incorrect_dataset.append({entry.get("userlabel"): entry, "table": table, "Error": lst})
            print(f"Error for userlabel: {entry.get("userlabel")} in Table {table}")
            print("validated_record", validated_record)
        except Exception as e:
            self.incorrect_dataset.append({entry.get("userlabel"): entry, "table": table, "Error": str(e)})
            print(e)
            print(f"Error for userlabel: {entry.get("userlabel")} in Table {table}")  #
            print("validated_record", validated_record)

        # headers = self.file_headers
        # headers["record_count"] = record_count
        # headers["creation_date"] = datetime.now().strftime("%d%m%Y")
        # headers["filenumber_medium"] = self.file_number
        # headers["filecontent"] = file_name

        # print(headers)

        # header = HCMHeader(**headers)
        # header = header.serialize_model()
        return records

    def write_to_file_new(self, file_name, input):
        folder = self.dir_path + "/"

        with open(folder + file_name, "w") as file:
            file.write(json.dumps(input, indent=4))

        print(f"\nFILE {file_name} written!\n")
