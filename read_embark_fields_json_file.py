# read_embark_fields_json_file.py 2/4/19 sm
""" This module will read and validate the JSON that defines the EmbArk XML. """

import json
#import pprint
import get_embark_xml_definitions


def _read_embark_field_definitions_file(filename):
    ''' read json from json file '''
    try:
        with open(filename, 'r') as input_source:
            data = json.load(input_source)
        input_source.close()
    except IOError:
        print('Cannot open ' + filename)
        raise
    except:
        print(filename + ' does not contain valid JSON.')
        raise
    return data

def _validate_embark_field_definitions_file(embark_field_definitions):
    ''' validate format of json file '''
    get_embark_xml_definitions.get_item_xpath(embark_field_definitions)
    fields_definition = get_embark_xml_definitions.get_fields_definition(embark_field_definitions)
    for field in fields_definition:
        try:
            get_embark_xml_definitions.get_field_name(field)
            get_embark_xml_definitions.get_field_required(field)
            get_embark_xml_definitions.get_field_duplicates_allowed(field)
            get_embark_xml_definitions.get_field_xpath(field)
            get_embark_xml_definitions.get_field_default(field)
            get_embark_xml_definitions.get_does_not_start_with(field)
            get_embark_xml_definitions.get_starts_with(field)
            get_embark_xml_definitions.get_validation_rule(field)
            get_embark_xml_definitions.get_constant(field)
        except ValueError:
            print('Error attempting to validate JSON file.')
            raise

def read_and_validate_embark_field_definitions_file(filename="./EmbArkXMLFields.json"):
    ''' calls routines to read and validate json file '''
    embark_field_definitions = ""
    try:
        embark_field_definitions = _read_embark_field_definitions_file(filename)
        _validate_embark_field_definitions_file(embark_field_definitions)
    except:
        print('Read_embark_fields_json_file.read_and_validate_embark_field_definitions_file encountered an error.')
        raise
    return embark_field_definitions
