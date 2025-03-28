from hcm.hcm_handler_new import HCMHandlerNew
from mock_data import *

handler_new = HCMHandlerNew()


def test_create_file_not_none():
    result = handler_new.new_format()

    assert result.get("content") is not None


def test_create_file_correct_json():
    result = handler_new.new_format()

    assert result.get("content") is not None


def test_create_file_validation_error():
    result = handler_new.new_format()

    assert result.get("content") is not None
