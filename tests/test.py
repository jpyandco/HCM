from db.database_handler import DatabaseHandler
from hcm.hcm_handler_current import HCMHandlerCurrent
from hcm.hcm_handler_new import HCMHandlerNew
from hcm.model import HCMCustomizableHeaders, HCMRecord


# db_handler = DatabaseHandler()
# data = db_handler.select_from_db("VIEW_rtr_data_gsm09")
# print(data)


sample = {
    "latitude": 48.20102778,
    "longitude": 15.53290833,
    "site_id": "240041A",
    "technology": "GSM",
    "cell-id": "28302",
    "channel": "941.4",
    "power": None,
    "outdoor": "TRUE",
    "enduser": "TRUE",
    "actual_control": "TRUE",
    "radio": "ZTE",
    "antenna": "80010123",
    "active_sharing": None,
    "sharing_partner": None,
    "1a": "941.4",
    "xx": "M",
    "1z": 1,
    "6a": "FB",
    "6b": "CP",
    "6z": "L",
    "10z": 1,
    "2c": "21062024",
    "4a": "3385_Gst. Nr. 479/2",
    "4b": "AUT",
    "4c": "015E315848N1203",
    "4d": 0,
    "4z": 290,
    "7a": "200KG7WEF",
    "8b1": 32,
    "8b2": "I",
    "9a": 270,
    "9b": 2.0,
    "9d": "M",
    "9g": 16.0,
    "9y": 27,
    "9xh": "033EA03",
    "9xv": "004EA03",
    "1y": "896.4",
    "xxx": "M",
    "13z": "2                                                 ",
    "13y": "B",
    "2w": None,
    "2z": None,
    "13x": "AUT241068442",
    "userlabel": "240041A0229",
    "antennatype": "80010123",
    "coveragearea": "Macro",
}

sample_dic = {
    "1a": 5000,
    "xx": "M",
    "1z": 1,
    "6a": "FB",
    "6b": "CP",
    "6z": "L",
    "10z": 1,
    "2c": "12345678",
    "4a": "Field 4A",
    "4b": "123",
    "4c": "123E456789N1234",
    "4d": 0,
    "4z": 0,
    "7a": "1234567",
    "8b1": 500,
    "8b2": "I",
    "9a": 359,
    "9b": None,
    "9d": "M",
    "9g": 50,
    "9y": 9999,
    "9xh": "1234567",
    "9xv": "1234567",
    "1y": 50000,
    "xxx": "M",
    "13z": "Field 13Z",
    "13y": "B",
    "2w": "12345678",
    "2z": "12345678",
    "13x": "AUT123456789012",
    "userlabel": "User Label",
}


# headers = HCMCustomizableHeaders(
#     person="Joe Heinz",
#     phone="",
#     email="bobo@drei.com",
#     fax="",
# )

# hcm_handler = HCMHandlerNew(headers.model_dump())
# hcm_handler.process()

record = HCMRecord(**sample_dic)
print(record.field_9XH)
# data = hcm_handler.new_format("TEST", "smacho", [sample])
# print(data)
# hcm_handler.write_to_file_new("NEW_JSON.json", data)

# value_str = "2  BOBo                              BLOCKSBERG                 "
# field_list = [1, 9, 2, 1, 37]
# resutlts = []
# starts = 0
# for length in field_list:
#     resutlts.append(value_str[starts : starts + length])
#     starts += length

# print(resutlts)
