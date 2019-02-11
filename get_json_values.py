#get_json_values.py 2/1/19 sm
''' This module deals with extracting a JSON value from a JSON variable.
    If a value is required, it must exist and must not be blank.
    If an error is encountered, we raise a ValueError.'''

import json
#import pprint

def get_json_value(json_variable, json_key, field_is_required=True):
    ''' Retrieve a value from a JSON variable '''
    if json_variable is None:
        print ("Missing in Action")
        return None
    json_value = ""
    #pprint.pprint(json_variable)
    try:
        json_value = json_variable[json_key]
        if json_value is None:
            raise ValueError(json_key + ' cannot be found.    JSON Control file is invalid.')
        if json_value == "" and field_is_required:
            raise ValueError(
                json_key
                + ' contained a blank value where it should have contained a required value.'
                + '   Offending portion of file includes:  '
                + json.dumps(json_variable))
    except KeyError:
        if field_is_required:
            raise ValueError(
                'Required Key Missing: "'
                + json_key + '" does not exist in JSON Control File.'
                + ' Offending portion of file includes: ' + json.dumps(json_variable))
    return json_value


#testing
# python3 -c 'from get_json_values import *; test()'

def test():
    ''' Test '''
    try:
        test_get_required_value()
        test_missing_required_value()
        test_blank_required_value()
        test_malformed_json()
        test_get_optional_value()
        test_blank_optional_value()
        test_missing_optional_value()
        print ('All tests ran successfully.')
    except:
        print ('We have a problem.')
        raise

def test_get_required_value():
    ''' Test getting a required value '''
    original_path = '{"itemPath": "./Section[@name=\'Body\'][@id=\'section_07\']","FieldsToExtract": []}'
    embark_field_definitions = json.loads(original_path)
    item_xpath = get_json_value(embark_field_definitions, 'itemPath')
    assert item_xpath == embark_field_definitions['itemPath']

def test_missing_required_value():
    ''' Test a missing required value '''
    embark_field_definitions = json.loads('{"xitemPath": "./Section[@name=\'Body\'][@id=\'section_07\']","FieldsToExtract": []}')
    value_error_encountered = False
    try:
        get_json_value(embark_field_definitions, 'itemPath')
    except ValueError:
        value_error_encountered = True
    if not value_error_encountered:
        print ('Expected error but didn\'t throw one.')

def test_blank_required_value():
    ''' Test a required value is blank '''
    value_error_encountered = False
    embark_field_definitions = json.loads('{"itemPath": "",	"FieldsToExtract": []}')
    try:
        get_json_value(embark_field_definitions, 'itemPath')
    except ValueError:
        value_error_encountered = True
    if not value_error_encountered:
        print ('Expected error but didn\'t throw one.')

def test_malformed_json():
    ''' Test to make sure we catch mal-formed json '''
    json_decode_error_encountered = False
    try:
        json.loads('{x"itemPath": "","FieldsToExtract": []}')
    except json.decoder.JSONDecodeError:
        json_decode_error_encountered = True
    if not json_decode_error_encountered:
        print ('Expected error but didn\'t throw one.')

def test_get_optional_value():
    ''' Test process of getting an optional value '''
    embark_field_definitions = json.loads('{"name": "facet","required": false,"duplicatesAllowed": true,"xpath": "./group[@id=\'object_00080\']/variable[@id=\'object_00080\']","startsWith": "AAT:"}')
    starts_with = get_json_value(embark_field_definitions, 'startsWith', False)
    assert starts_with == "AAT:"

def test_blank_optional_value():
    ''' Test to ensure retrieving a blank optional value is acceptable '''
    embark_field_definitions = json.loads('{"name": "facet","required": false,"duplicatesAllowed": true,"xpath": "./group[@id=\'object_00080\']/variable[@id=\'object_00080\']","startsWith": ""}')
    starts_with = get_json_value(embark_field_definitions, 'startsWith', False)
    assert starts_with == ""

def test_missing_optional_value():
    ''' Test to ensure missing optional value is acceptable '''
    embark_field_definitions = json.loads('{"name": "facet","required": false,"duplicatesAllowed": true,"xpath": "./group[@id=\'object_00080\']/variable[@id=\'object_00080\']"}')
    starts_with = get_json_value(embark_field_definitions, 'startsWith', False)
    assert starts_with == ""
