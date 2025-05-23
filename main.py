# from pydantic import BaseModel
# from db.database_handler import DatabaseHandler
from gui.gui import GUI

# from hcm import HCMRecord, HCMHeader
# from datetime import datetime
from hcm.const import CONFIG, FILEPREFIX, FILETYPE

# from hcm.hcm_handler_current import HCMHandler

CSV_DELIMITER = ";"
CSV_ENCODING = "utf-8-sig"

HCM_FIELD_PREFIX = "field_"
# every entry/row has to be 219 bytes(characters) long
LENGHT = 219


def main():

    try:
        gui_handler = GUI()
        gui_handler.start_gui()
        # hcm_handler = HCMHandler()
        # hcm_handler.process()

    except Exception as e:
        print(e)

    return


if __name__ == "__main__":
    main()
