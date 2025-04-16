from pydantic import ValidationError
from hcm.hcm_handler_new import HCMHandlerNew
from hcm.model import HCMHeader
from mock_data import *

handler_new = HCMHandlerNew(headers)
table = "table"
file_name = "testing"


def test_create_file_not_none():
    result = handler_new.new_format(table, list_sample)

    assert result is not None


def test_create_file_correct_json():
    result = handler_new.new_format(table, list_sample)

    assert len(result) == 2


def test_create_file_wrong_data_format():
    try:
        result = handler_new.new_format(table, sample)

    except Exception as e:
        assert isinstance(e, AttributeError)


def test_create_file_missing_fields():

    result = handler_new.new_format(table, missing_sample)
    assert len(handler_new.incorrect_dataset) > 0


def test_header_creation_error():
    try:
        handler_new.create_headers(file_name)
    except Exception as e:
        assert isinstance(e, ValidationError)


def test_header_creation():
    result = handler_new.create_headers(file_name)
    assert isinstance(result, dict)
