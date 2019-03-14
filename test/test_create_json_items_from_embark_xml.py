# test_create_json_items_from_embark_xml.py 2/18/19 sm
""" test create_json_items_from_embark_xml.py """

import sys
import json
import unittest
import csv
from xml.etree.ElementTree import ElementTree, tostring

# add parent directory to path
import os
import inspect
CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PARENTDIR = os.path.dirname(CURRENTDIR)
sys.path.insert(0, PARENTDIR)

import create_json_items_from_embark_xml


class Test(unittest.TestCase):
    """ Class for test fixtures """

    def test_write_json_output(self):
        """ test writing json output """
        json_data = '{"sample" : "test"}'
        create_json_items_from_embark_xml.write_json_output('.', 'test_write_json_output.json', json_data)
        with open('./test_write_json_output.json', 'r') as input_source:
            data = json.load(input_source)
        input_source.close()
        self.assertTrue(json_data == data)

    def test_everything(self):
        """ run test on whole process, verifying expected results """
        create_json_items_from_embark_xml.create_json_items_from_embark_xml('./objects 01_18_19.xml', 'temp/pnx',
                                                                            csv_output_root_directory='temp')

        # verify one csv
        with open('temp/1976.057/main.csv', 'r') as read_actual:
            reader = csv.reader(read_actual)
            actual_csv = list(reader)
        with open('./expected_results/test_everything.csv', 'r') as read_expected:
            reader = csv.reader(read_expected)
            expected_csv = list(reader)
        self.assertTrue(actual_csv == expected_csv)

        # verify one pnx
        actual_results_file_name = 'temp/pnx/1976.057.xml'
        expected_results_file_name = 'expected_results/test_everything.xml'
        actual_results = ElementTree(file=actual_results_file_name)
        expected_results = ElementTree(file=expected_results_file_name)
        # print(ElementTree.tostring(xml_tree.getroot()))
        self.assertTrue(tostring(actual_results.getroot()) == tostring(expected_results.getroot()))


def suite():
    """ define test suite """
    return unittest.TestLoader().loadTestsFromTestCase(Test)


if __name__ == '__main__':
    suite()
    unittest.main()
