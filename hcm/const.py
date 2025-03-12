from typing import Literal

CONFIG = r"C:\Users\bohrnjo\OneDrive - Hutchison Drei Austria GmbH\Documents\Python\HCM\config.ini"
FILEPREFIX = "H3A_"

DATASET_LENGTH = 219
FILETYPE = "O"
COUNTRY = "AUT"
UNITS = Literal["K", "M", "G"]
FUNKSTELLE = Literal["FB", "FL", "ML"]
FUNKDIENST = Literal["CO", "CP", "CR", "CV", "OT"]
FREQUENZKATEGORIEN = Literal[1, 2, 3, 4, 5, 6, 7, 8]
KANALBELEGUNG = Literal[0, 1]
POLARISIERUNG = Literal["H", "V", "SR", "SL", "CR", "CL", "D", "M"]
KOORDINIERUNGSSTATUS = Literal["P", "B"]
ANTENNENTYP = Literal["I", "E"]
BENUTZERKATEGORIEN = Literal[
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "HH",
    "I",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]
