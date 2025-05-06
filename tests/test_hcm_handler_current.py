from cgitb import handler
from unittest.mock import MagicMock
from pydantic import ValidationError
import pytest
from hcm.hcm_handler_current import HCMHandlerCurrent
from hcm.model import HCMHeader
from mock_data import *
from db.database_handler import DatabaseHandler

handler_new = HCMHandlerCurrent(headers)
table = "table"
file_name = "testing"


def test_create_file_not_none():
    result = handler_new.create_file(table, list_sample)

    assert result is not None


def test_create_file_correct_json():
    result = handler_new.create_file(table, list_sample)
    # 2 entries, 219 * 2 = 438
    assert len(result) == 438


def test_create_file_wrong_data_format():
    with pytest.raises(AttributeError):
        result = handler_new.create_file(table, sample)


def test_create_file_missing_fields():
    result = handler_new.create_file(table, missing_sample)
    assert len(handler_new.incorrect_dataset) > 0


def test_header_creation_error():
    handler = HCMHandlerCurrent(headers)
    handler.record_count = None
    with pytest.raises(ValidationError):
        result = handler.create_headers(file_name)


def test_header_creation():
    result = handler_new.create_headers(file_name)
    assert isinstance(result, str)
    assert len(result) == 219


def test_process(tmpdir):
    handler = HCMHandlerCurrent(headers)
    db_handler = DatabaseHandler()
    temp_dir = tmpdir.mkdir("tmp")
    temp_file = temp_dir.join("temp_file")
    tmp_file = "temp_file"
    print(temp_file)
    path = temp_dir + "/tmp_file"
    handler.dir_path = str(temp_dir)
    db_handler.select_from_db = MagicMock(return_value=list_sample)
    handler.get_file_name = MagicMock(return_value=str(tmp_file))
    handler.db_handler = db_handler
    handler.process()

    # 657 = 3 * 219, 2 entries + 1 header entry
    assert len(temp_file.read()) == 657


def test_create_temp_file(tmpdir):
    # Create a temporary file
    temp_file = tmpdir.join("temp_file.txt")

    # Write data to the temporary file
    temp_file.write("This is a temporary file.")

    # Read data from the temporary file
    assert temp_file.read() == "This is a temporary file."
