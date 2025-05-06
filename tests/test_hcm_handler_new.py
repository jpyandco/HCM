from pydantic import ValidationError
import pytest
from hcm.hcm_handler_current import HCMHandlerCurrent
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
    with pytest.raises(AttributeError):
        result = handler_new.new_format(table, sample)


def test_create_file_missing_fields():

    result = handler_new.new_format(table, missing_sample)
    assert len(handler_new.incorrect_dataset) > 0


def test_header_creation_error():
    handler = HCMHandlerCurrent(headers)
    handler.record_count = None
    with pytest.raises(ValidationError):
        result = handler.create_headers(file_name)


def test_header_creation():
    result = handler_new.create_headers(file_name)
    assert isinstance(result, dict)
