from typing import Optional, Self, Type, Any

from pydantic import (
    BaseModel,
    model_serializer,
    model_validator,
    Field,
    ValidationError,
)

from hcm.const import (
    UNITS,
    FREQUENZKATEGORIEN,
    FUNKSTELLE,
    FUNKDIENST,
    BENUTZERKATEGORIEN,
    ANTENNENTYP,
    POLARISIERUNG,
    KOORDINIERUNGSSTATUS,
    KANALBELEGUNG,
    DATASET_LENGTH,
    FILETYPE,
    COUNTRY,
)


def _stringify(value: str | int | float | None, length: int, fmt: str = "") -> str:
    """Returns values in given format. Also handles required length per field. Empty space is filled with 0 or whitespace"""
    if value is not None:
        return f"{value:{fmt}}"
    else:
        return " " * length


def convert_errors(e: ValidationError):
    pass


class HCMCustomizableHeaders(BaseModel):
    person: str
    phone: str
    fax: str
    email: str


class HCMHeader(BaseModel):
    filenumber_medium: int = Field(lt=100)
    filecontent: str = Field(max_length=80)
    filetype: str = Field(default=FILETYPE)
    origin_country: str = Field(max_length=3, default=COUNTRY)
    email: str = Field(max_length=40)
    phone: str = Field(max_length=20)
    fax: str = Field(max_length=20)
    person: str = Field(max_length=20)
    record_count: int = Field(lt=1000000)
    creation_date: str = Field(max_length=8)
    destination_country: str = Field(max_length=3, default=COUNTRY)
    filenumber: Optional[int] = Field(lt=1000000, default=None)
    fileversion: float = Field(lt=10, default=1.0)
    reserved: Optional[str] = Field(max_length=7, default="")

    @model_serializer
    def serialize_model(self) -> str:
        hcm_header = [
            _stringify(self.filenumber_medium, 2, "2d"),
            _stringify(self.filecontent, 80, "<80"),
            _stringify(self.filetype, 1),
            _stringify(self.origin_country, 3, "<3"),
            _stringify(self.email, 40, "<40"),
            _stringify(self.phone, 20, "<20"),
            _stringify(self.fax, 20, "<20"),
            _stringify(self.person, 20, "<20"),
            _stringify(self.record_count, 6, "6d"),
            _stringify(self.creation_date, 8, "<8"),
            _stringify(self.destination_country, 3, "<3"),
            _stringify(self.filenumber, 6, "6d"),
            _stringify(self.fileversion, 3, "3.1f"),
            _stringify(self.reserved, 7, "<7"),
        ]

        header_string = "".join(hcm_header)

        if len(header_string) != DATASET_LENGTH:
            raise ValueError(f"Datensatzlänge falsch. {len(header_string)} != {DATASET_LENGTH}")

        return header_string


class HCMRecord(BaseModel):
    field_1A: Optional[float] = Field(ge=0, lt=10000, validation_alias="1a")
    field_XX: UNITS = Field(validation_alias="xx")
    field_1Z: FREQUENZKATEGORIEN = Field(validation_alias="1z")
    field_6A: FUNKSTELLE = Field(validation_alias="6a")
    field_6B: FUNKDIENST = Field(validation_alias="6b")
    field_6Z: BENUTZERKATEGORIEN = Field(validation_alias="6z")
    field_10Z: KANALBELEGUNG = Field(validation_alias="10z")
    field_2C: Optional[str] = Field(min_length=8, max_length=8, validation_alias="2c")
    field_4A: str = Field(max_length=20, validation_alias="4a")
    field_4B: str = Field(min_length=3, max_length=3, validation_alias="4b")
    field_4C: str = Field(min_length=15, max_length=15, pattern=r"^\d{3}(E|W)\d{6}(N|S)\d{4}$", validation_alias="4c")
    field_4D: int = Field(le=100000, validation_alias="4d")
    field_4Z: int = Field(le=9999, validation_alias="4z", default=0)
    field_7A: str = Field(min_length=7, max_length=9, validation_alias="7a")
    field_8B1: Optional[float] = Field(ge=0, lt=1000, validation_alias="8b1")
    field_8B2: ANTENNENTYP = Field(validation_alias="8b2")
    field_9A: Optional[float] = Field(ge=0, lt=361, validation_alias="9a")
    field_9B: Optional[float] = Field(ge=-90, le=90, validation_alias="9b")
    field_9D: POLARISIERUNG = Field(validation_alias="9d")
    field_9G: Optional[float] = Field(ge=0, lt=100, validation_alias="9g")
    field_9Y: int = Field(le=9999, validation_alias="9y")
    field_9XH: str = Field(min_length=7, max_length=7, validation_alias="9xh")
    field_9XV: str = Field(min_length=7, max_length=7, validation_alias="9xv")
    field_1Y: Optional[float] = Field(ge=0, lt=100000, validation_alias="1y")
    field_XXX: UNITS = Field(validation_alias="xxx")
    field_13Z: Optional[str] = Field(max_length=50, validation_alias="13z")
    field_13Y: KOORDINIERUNGSSTATUS = Field(validation_alias="13y")
    field_2W: Optional[str] = Field(min_length=0, max_length=8, validation_alias="2w")
    field_2Z: Optional[str] = Field(min_length=0, max_length=8, validation_alias="2z")
    field_13X: str = Field(max_length=15, pattern=r"^AUT\d+", validation_alias="13x")
    user_label: Optional[str] = Field

    @model_validator(mode="after")
    def check_1A(self) -> Self:
        if self.field_1A is None and self.field_8B1 is not None:
            raise ValueError("wenn 1A leer ist, muss 8B1 leer sein.")
        return self

    @model_validator(mode="after")
    def check_4D(self) -> Self:
        if not self.field_6A.startswith("M") and self.field_4D != 0:
            raise ValueError("Beginnt 6A nicht mit 'M', ist 4D immer 0")
        return self

    @model_validator(mode="after")
    def check_4Z(self) -> Self:
        if self.field_4Z and not self.field_6A.startswith("F"):
            raise ValueError("Nur gültig, wenn 6A mit 'F' beginnt.")
        return self

    @model_validator(mode="after")
    def check_8B1(self) -> Self:
        if self.field_8B1 is None and self.field_1A is not None:
            raise ValueError("fehlt 1A, muss auch 8B1 fehlen")
        return self

    @model_validator(mode="after")
    def check_9A(self) -> Self:
        if self.field_6A.startswith("M") and self.field_9A is not None:
            raise ValueError("Beginnt 6A mit 'M', ist 9A immer leer.")
        if self.field_9A == 360:
            self.field_9A = 359.9
        return self

    @model_validator(mode="after")
    def check_9XH(self) -> Self:
        if self.field_9A is None and self.field_9XH != "000ND00":
            raise ValueError(" Ist 9A leer, so ist 9XH 000ND00")
        return self

    @model_validator(mode="after")
    def check_9XV(self) -> Self:
        if self.field_9B is None and self.field_9XH != "000ND00":
            raise ValueError(" Ist 9B leer, so ist 9XV 000ND00")
        return self

    @model_validator(mode="after")
    def check_1Y(self) -> Self:
        if self.field_1A is None and self.field_1Y is None:
            raise ValueError("1Y muss ausgefüllt werden, wenn 1A nicht ausgefüllt ist.")
        return self

    @model_serializer
    def serialize_model(self) -> str:
        hcm_dataset = [
            _stringify(self.field_1A, 11, "011.5f"),
            _stringify(self.field_XX, 1),
            _stringify(self.field_1Z, 1),
            _stringify(self.field_6A, 2, "<2"),
            _stringify(self.field_6B, 2, "<2"),
            _stringify(self.field_6Z, 2, "<2"),
            _stringify(self.field_10Z, 1),
            _stringify(self.field_2C, 8, "<8"),
            _stringify(self.field_4A, 20, "<20"),
            _stringify(self.field_4B, 3, "<3"),
            _stringify(self.field_4C, 15, "<15"),
            _stringify(self.field_4D, 5, "5d"),
            _stringify(self.field_4Z, 4, "4d"),
            _stringify(self.field_7A, 9, "<9"),
            _stringify(self.field_8B1, 6, "+06.1f"),
            _stringify(self.field_8B2, 1),
            _stringify(self.field_9A, 5, "05.1f"),
            _stringify(self.field_9B, 5, "05.1f"),
            _stringify(self.field_9D, 2, "<2"),
            _stringify(self.field_9G, 6, "04.1f"),
            _stringify(self.field_9Y, 4, "4d"),
            _stringify(self.field_9XH, 7, "<7"),
            _stringify(self.field_9XV, 7, "<7"),
            _stringify(self.field_1Y, 11, "11.5f"),
            _stringify(self.field_XXX, 1),
            _stringify(self.field_13Z, 50, "<50"),
            _stringify(self.field_13Y, 1),
            _stringify(self.field_2W, 8, "<8"),
            _stringify(self.field_2Z, 8, "<8"),
            _stringify(self.field_13X, 15, "<15"),
            # )
        ]

        dataset_string = "".join(hcm_dataset)

        if (dataset_length := len(dataset_string)) != DATASET_LENGTH:
            raise ValueError(f"Datensatzlänge falsch. {dataset_length} != {DATASET_LENGTH}")

        return dataset_string
