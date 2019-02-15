#test_get_json_values.py 2/14/19 sm

import json
import unittest
from get_json_values import get_json_value

class TestGetJsonValues(unittest.TestCase):

    def test_get_required_value(self):
        ''' Test getting a required value '''
        original_path = '{"itemPath": "./Section[@name=\'Body\'][@id=\'section_07\']","FieldsToExtract": []}'
        embark_field_definitions = json.loads(original_path)
        item_xpath = get_json_value(embark_field_definitions, 'itemPath')
        self.assertTrue(item_xpath == embark_field_definitions['itemPath'])

    def test_missing_required_value(self):
        ''' Test a missing required value '''
        embark_field_definitions = json.loads('{"xitemPath": "./Section[@name=\'Body\'][@id=\'section_07\']","FieldsToExtract": []}')
        value_error_encountered = False
        try:
            self.assertRaises(get_json_value(embark_field_definitions, 'itemPath'))
        except ValueError:
            value_error_encountered = True
        if not value_error_encountered:
            print('Expected error but didn\'t throw one.')

    def test_blank_required_value():
        ''' Test a required value is blank '''
        value_error_encountered = False
        embark_field_definitions = json.loads('{"itemPath": "",	"FieldsToExtract": []}')
        try:
            get_json_value(embark_field_definitions, 'itemPath')
        except ValueError:
            value_error_encountered = True
        if not value_error_encountered:
            print('Expected error but didn\'t throw one.')

    def test_malformed_json():
        ''' Test to make sure we catch mal-formed json '''
        json_decode_error_encountered = False
        try:
            json.loads('{x"itemPath": "","FieldsToExtract": []}')
        except json.decoder.JSONDecodeError:
            json_decode_error_encountered = True
        if not json_decode_error_encountered:
            print('Expected error but didn\'t throw one.')

    def test_get_optional_value():
        ''' Test process of getting an optional value '''
        embark_field_definitions = json.loads('{"xpath": "./group[@id=\'object_00080\']/variable[@id=\'object_00080\']","startsWith": "AAT:"}')
        starts_with = get_json_value(embark_field_definitions, 'startsWith', False)
        self.assertTrue(starts_with == "AAT:")

    def test_blank_optional_value():
        ''' Test to ensure retrieving a blank optional value is acceptable '''
        embark_field_definitions = json.loads('{"xpath": "./group[@id=\'object_00080\']/variable[@id=\'object_00080\']","startsWith": ""}')
        starts_with = get_json_value(embark_field_definitions, 'startsWith', False)
        test.assertTrue(starts_with == "")

    def test_missing_optional_value():
        ''' Test to ensure missing optional value is acceptable '''
        embark_field_definitions = json.loads('{"xpath": "./group[@id=\'object_00080\']/variable[@id=\'object_00080\']"}')
        starts_with = get_json_value(embark_field_definitions, 'startsWith', False)
        assert starts_with == ""


if __name__ == '__main__':
    unittest.main()
