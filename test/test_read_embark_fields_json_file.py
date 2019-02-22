#test_read_embark_fields_json_file.py 2/18/19 sm
''' test read_embark_fields_json_file.py '''

import json
import unittest

# add parent directory to path
import os
import inspect
import sys
CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PARENTDIR = os.path.dirname(CURRENTDIR)
sys.path.insert(0, PARENTDIR)

from read_embark_fields_json_file import read_and_validate_embark_field_definitions_file

class Test(unittest.TestCase):
    ''' Class for test fixtures '''

    def test_read_and_validate_embark_field_definitions_file(self):
        ''' run all tests in this module '''
        filename = PARENTDIR + "/EmbArkXMLFields.json"
        resulting_json = read_and_validate_embark_field_definitions_file(filename)
        with open(filename, 'r') as input_source:
            local_json = json.load(input_source)
        input_source.close()
        self.assertTrue(local_json == resulting_json)

    def test_missing_embark_field_definitions_file(self):
        ''' test for missing field definitions file '''
        self.assertRaises(FileNotFoundError, read_and_validate_embark_field_definitions_file, "./EmbArkXMLFields.jsonx")

    def test_invalid_embark_field_definitions_file(self):
        ''' test for missing field definitions file '''
        self.assertRaises(json.decoder.JSONDecodeError, read_and_validate_embark_field_definitions_file, PARENTDIR + "/InvalidEmbArkXMLFields.json")

    def test_embark_field_definitions_file_missing_field(self):
        ''' test for missing field definitions file '''
        self.assertRaises(ValueError, read_and_validate_embark_field_definitions_file, PARENTDIR + "/EmbArkXMLFieldsMissingField.json")

if __name__ == '__main__':
    unittest.main()
