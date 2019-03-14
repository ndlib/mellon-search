# test_get_json_values.py 2/14/19 sm
""" test get_json_values.py """

import json
import unittest

# add parent directory to path
import os
import inspect
import sys
CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PARENTDIR = os.path.dirname(CURRENTDIR)
sys.path.insert(0, PARENTDIR)

from get_json_values import get_json_value


class Test(unittest.TestCase):
    """ Class for test fixtures """

    def test_get_required_value(self):
        """ Test getting a required value """
        original_path = '{"itemPath": "./Section[@name=\'Body\'][@id=\'section_07\']","FieldsToExtract": []}'
        embark_field_definitions = json.loads(original_path)
        item_xpath = get_json_value(embark_field_definitions, 'itemPath')
        self.assertTrue(item_xpath == embark_field_definitions['itemPath'])

    def test_missing_required_value(self):
        """ Test a missing required value """
        embark_field_definitions = json.loads('{"xitemPath": "./Section[@name=\'Body\'][@id=\'section_07\']",'
                                              + '"FieldsToExtract": []}')
        self.assertRaises(ValueError, get_json_value, embark_field_definitions, 'itemPath')

    def test_blank_required_value(self):
        """ Test a required value is blank """
        embark_field_definitions = json.loads('{"itemPath": "",	"FieldsToExtract": []}')
        self.assertRaises(ValueError, get_json_value, embark_field_definitions, 'itemPath')

    def test_malformed_json(self):
        """ Test to make sure we catch mal-formed json """
        self.assertRaises(json.decoder.JSONDecodeError, json.loads, '{x"itemPath": "","FieldsToExtract": []}')

    def test_get_optional_value(self):
        """ Test process of getting an optional value """
        embark_field_definitions = json.loads('{"xpath": "./group[@id=\'object_00080\']'
                                              + '/variable[@id=\'object_00080\']","startsWith": "AAT:"}')
        starts_with = get_json_value(embark_field_definitions, 'startsWith', False)
        self.assertTrue(starts_with == "AAT:")

    def test_blank_optional_value(self):
        """ Test to ensure retrieving a blank optional value is acceptable """
        embark_field_definitions = json.loads('{"xpath": "./group[@id=\'object_00080\']'
                                              + '/variable[@id=\'object_00080\']","startsWith": ""}')
        starts_with = get_json_value(embark_field_definitions, 'startsWith', False)
        self.assertTrue(starts_with == "")

    def test_missing_optional_value(self):
        """ Test to ensure missing optional value is acceptable """
        embark_field_definitions = json.loads('{"xpath": "./group[@id=\'object_00080\']'
                                              + '/variable[@id=\'object_00080\']"}')
        starts_with = get_json_value(embark_field_definitions, 'startsWith', False)
        self.assertTrue(starts_with == "")


def suite():
    """ define test suite """
    return unittest.TestLoader().loadTestsFromTestCase(Test)


if __name__ == '__main__':
    suite()
    unittest.main()
