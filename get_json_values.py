# get_json_values.py 2/1/19 sm
""" This module deals with extracting a JSON value from a JSON variable.
    If a value is required, it must exist and must not be blank.
    If an error is encountered, we raise a ValueError."""

import json
#import pprint

def get_json_value(json_variable, json_key, field_is_required=True):
    """ Retrieve a value from a JSON variable """
    json_value = ""
    if json_key not in json_variable:
        if field_is_required:
            raise ValueError(
                'Required Key Missing: "'
                + json_key + '" does not exist in JSON Control File.'
                + ' Offending portion of file includes: ' + json.dumps(json_variable))
        return json_value
    json_value = json_variable[json_key]
    if json_value == "" and field_is_required:
        raise ValueError(
            json_key
            + ' contained a blank value where it should have contained a required value.'
            + '   Offending portion of file includes:  '
            + json.dumps(json_variable))
    return json_value
