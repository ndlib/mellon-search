# read_embark_fields_json_file.py 2/4/19 sm
"""This module will read and validate the JSON that defines the EmbArk XML."""

from __future__ import print_function

import json
from get_embark_xml_definitions import get_fields_definition, get_item_xpath, \
    get_field_name, get_field_required, get_field_duplicates_allowed, \
    get_field_xpath, get_field_default, get_does_not_start_with, \
    get_starts_with, get_validation_rule, get_constant


def _read_embark_fields_file(filename):
    """ read json from json file """
    try:
        with open(filename, 'r') as input_source:
            data = json.load(input_source)
        input_source.close()
    except IOError:
        print('Cannot open ' + filename)
        raise
    return data


def _validate_embark_fields_file(embark_field_definitions):
    """ validate format of json file """
    get_item_xpath(embark_field_definitions)
    fields_definition = get_fields_definition(embark_field_definitions)
    for field in fields_definition:
        try:
            get_field_name(field)
            get_field_required(field)
            get_field_duplicates_allowed(field)
            get_field_xpath(field)
            get_field_default(field)
            get_does_not_start_with(field)
            get_starts_with(field)
            get_validation_rule(field)
            get_constant(field)
        except ValueError:
            print('Error attempting to validate JSON file.')
            raise


def read_embark_fields_json_file(filename="./EmbArkXMLFields.json"):
    """ calls routines to read and validate json file """
    embark_field_definitions = ""
    try:
        embark_field_definitions = _read_embark_fields_file(filename)
        _validate_embark_fields_file(embark_field_definitions)
    except ValueError:
        print('ValueError in read_embark_fields_json_file encountered.')
        raise
    return embark_field_definitions
