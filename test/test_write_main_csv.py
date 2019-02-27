# test_write_main_csv.py 2/18/19 sm
""" test write_main_csv.py """

import json
import unittest
import csv

# add parent directory to path
import os
import inspect
import sys
CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PARENTDIR = os.path.dirname(CURRENTDIR)
sys.path.insert(0, PARENTDIR)

# this adds the current directory to the path if needed
# sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# import what I need from the parent directory
from write_main_csv import _create_first_row, _create_metadata_row, _create_metadata_row_from_string, \
    _create_exhibition_metadata_row, _create_metadata_array_row, _create_metadata_rows, write_main_csv


def get_json_input():
    """ get pre-formed json to make sure testing is uniform """
    with open('json_for_testing.json', 'r') as input_source:
        json_input = json.load(input_source)
    input_source.close()
    return json_input


class Test(unittest.TestCase):
    """ Class for test fixtures """

    def test_create_first_row(self):
        """ test _create_first_row """
        json_data = get_json_input()
        row = _create_first_row(json_data)
        with open('./actual_results/test_create_first_row.json', 'w') as outfile:
            json.dump(row, outfile)
        with open('./expected_results/test_create_first_row.json', 'r') as expected_file:
            expected_results = json.load(expected_file)
        expected_file.close()
        with open('./actual_results/test_create_first_row.json', 'r') as actual_file:
            actual_results = json.load(actual_file)
        actual_file.close()
        self.assertTrue(actual_results == expected_results)

    def test_create_metadata_row(self):
        """ test create_metadata_row """
        json_data = get_json_input()
        row = _create_metadata_row(json_data, 'recordId', 'Accession Number')
        self.assertTrue(row == json.loads('{"Metadata_label": "Accession Number", "Metadata_value": "1976.057"}'))

    def test_create_metadata_row_from_string(self):
        """ test _create_metadata_row_from_string """
        row = _create_metadata_row_from_string('element_label', 'element_string')
        self.assertTrue(row == json.loads('{"Metadata_label": "element_label", "Metadata_value": "element_string"}'))

    def test_create_exhibition_metadata_row(self):
        """ test _create_exhibition_metadata_row """
        json_data = get_json_input()
        row = _create_exhibition_metadata_row(json_data, 'exhibition', 'Exhibition')
        self.assertTrue(row == json.loads('{"Metadata_label": "Exhibition", "Metadata_value": "Picturing History(09/01/94 - 12/01/94)\\n"}'))

    def test_create_metadata_array_row(self):
        """ test _create_metadata_array_row(json_data, 'bibliography', 'Bibliography') """
        json_data = get_json_input()
        row = _create_metadata_array_row(json_data, 'bibliography', 'Bibliography')
        with open('./actual_results/test_create_metadata_array_row.json', 'w') as outfile:
            json.dump(row, outfile)
        with open('./expected_results/test_create_metadata_array_row.json', 'r') as expected_file:
            expected_results = json.load(expected_file)
        expected_file.close()
        with open('./actual_results/test_create_metadata_array_row.json', 'r') as actual_file:
            actual_results = json.load(actual_file)
        actual_file.close()
        self.assertTrue(actual_results == expected_results)

    def test_create_metadata_rows(self):
        """ test _create_metadata_rows """
        json_data = get_json_input()
        metadata_results = _create_metadata_rows(json_data)
        with open('./actual_results/test_create_metadata_rows.json', 'w') as outfile:
            json.dump(metadata_results, outfile)
        with open('./expected_results/test_create_metadata_rows.json', 'r') as expected_file:
            expected_results = json.load(expected_file)
        expected_file.close()
        with open('./actual_results/test_create_metadata_rows.json', 'r') as actual_file:
            actual_results = json.load(actual_file)
        actual_file.close()
        self.assertTrue(actual_results == expected_results)

    def test_write_main_csv(self):
        """ test write_main_csv """
        json_data = get_json_input()
        write_main_csv('actual_results', json_data)
        # read the file we just wrote
        with open('actual_results/main.csv', 'r') as read_actual_file:
            reader = csv.reader(read_actual_file)
            actual_results = list(reader)
        with open('expected_results/main.csv', 'r') as read_expected_file:
            reader = csv.reader(read_expected_file)
            expected_results = list(reader)
        self.assertTrue(actual_results == expected_results)


def suite():
    """ define test suite """
    return unittest.TestLoader().loadTestsFromTestCase(Test)


if __name__ == '__main__':
    unittest.main()
