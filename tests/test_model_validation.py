from hcm.model import HCMRecord
import pytest
from pydantic import ValidationError

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
    "9b": 45,  # 45
    "9d": "M",
    "9g": 50,
    "9y": 9999,
    "9xh": "000ND00",
    "9xv": "000ND00",
    "1y": 50000,
    "xxx": "M",
    "13z": "Field 13Z",
    "13y": "B",
    "2w": "12345678",
    "2z": "12345678",
    "13x": "AUT123456789012",
    "userlabel": "User Label",
}

deserialized_record = {
    "field_1A": 5000,
    "field_XX": "M",
    "field_1Z": 1,
    "field_6A": "FB",
    "field_6B": "CP",
    "field_6Z": "L",
    "field_10Z": 1,
    "field_2C": "12345678",
    "field_4A": "Field 4A",
    "field_4B": "123",
    "field_4C": "123E456789N1234",
    "field_4D": 0,
    "field_4Z": 0,
    "field_7A": "1234567",
    "field_8B1": 500,
    "field_8B2": "I",
    "field_9A": 359,
    "field_9B": 45,  # 45
    "field_9D": "M",
    "field_9G": 50,
    "field_9Y": 9999,
    "field_9XH": "000ND00",
    "field_9XV": "000ND00",
    "field_1Y": 50000,
    "field_XXX": "M",
    "field_13Z": "Field 13Z",
    "field_13Y": "B",
    "field_2W": "12345678",
    "field_2Z": "12345678",
    "field_13X": "AUT123456789012",
    "user_label": "User Label",
}


missing = {
    "1a": 5000,
    # "xx": "M",
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
}


def test_valid_hcm_record():
    record = HCMRecord(**sample_dic)
    assert record.field_1A == 5000


def test_invalid_1A_8B1():
    data = sample_dic.copy()
    data["1a"] = None
    data["8b1"] = 500
    with pytest.raises(ValidationError):
        HCMRecord(**data)


def test_invalid_4D():
    data = sample_dic.copy()
    data["6a"] = "A"
    data["4d"] = 1
    with pytest.raises(ValidationError):
        HCMRecord(**data)


def test_invalid_4Z():
    data = sample_dic.copy()
    data["4z"] = 1
    data["6a"] = "A"
    with pytest.raises(ValidationError):
        HCMRecord(**data)


def test_invalid_9A():
    data = sample_dic.copy()
    data["6a"] = "M"
    data["9a"] = 359
    with pytest.raises(ValidationError):
        HCMRecord(**data)


def test_invalid_9XH():
    data = sample_dic.copy()
    data["9a"] = None
    data["9xh"] = "1234567"
    with pytest.raises(ValidationError):
        HCMRecord(**data)


def test_invalid_9XV():
    data = sample_dic.copy()
    data["9b"] = None
    data["9xv"] = "1234567"
    # with pytest.raises(ValidationError):
    #     HCMRecord(**data)

    # assert record.field_9XV == "1234567"
    # assert record.field_9B == None
    # assert record == None


def test_invalid_1Y():
    data = sample_dic.copy()
    data["1a"] = None
    data["1y"] = None
    with pytest.raises(ValidationError):
        HCMRecord(**data)


def test_missing_fields():
    with pytest.raises(ValidationError):
        HCMRecord(**missing)


def test_data_deserialized():
    record = HCMRecord(**sample_dic)
    dic = dict(record)
    assert dic == deserialized_record


if __name__ == "__main__":
    pytest.main()
