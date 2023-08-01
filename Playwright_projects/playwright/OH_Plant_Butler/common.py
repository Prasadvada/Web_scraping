import os


def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path


from cerberus import Validator
from datetime import datetime

_string0 = {"type": "string", "empty": False, "required": True}
_string1 = {"type": "string", "required": True, "empty": True}
_string2 = {"type": "string", "required": False}

schema_input = {
    "state": _string0,
    "county": _string0,
    "start_date": _string0,
    "end_date": _string0,
}

schema_output = {
    "document_number": _string1,
    "document_type": _string1,
    "recording_date": _string1,
    "book": _string2,
    "page": _string2,
    "legal": _string2,
    "grantor": _string1,
    "grantee": _string1
}


def validate_schema_input(data):
    if not Validator(schema_input).validate(data):
        raise Exception("Please Enter All The Search Parameters.JobID, State, County, Dates Are Compulsory")
    else:
        return True


def validate_schema_output(data):
    if not Validator(schema_output).validate(data):
        raise Exception("Output Fields Are Incomplete")
    else:
        return True


def check_weekday(date):
    weekdays = {
        1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"
    }
    date_time_obj = datetime.strptime(date, '%m/%d/%Y')
    day = date_time_obj.isoweekday()
    return day, weekdays[day]
