# test_create_pnx_from_json.py 2/18/19 sm
""" test create_pnx_from_json.py """

from __future__ import print_function

import json
import unittest
from xml.etree import ElementTree

# add parent directory to path
import os
import inspect
import sys
CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))  # noqa
PARENTDIR = os.path.dirname(CURRENTDIR)
sys.path.insert(0, PARENTDIR)

from create_pnx_from_json import create_pnx_from_json, create_pnx_from_json_and_write_file, \
    _create_xml_element, _get_json_value, _get_media_and_display, _get_exhibition, \
    _create_search_section, _create_browse_section, _create_sort_section, _create_facet_section, \
    _create_delivery_section  # noqa
from file_system_utilities import create_directory
from write_pnx_file import write_pnx_file


def get_json_input():
    """ get pre-formed json to make sure testing is uniform """
    with open('json_for_testing.json', 'r') as input_source:
        json_input = json.load(input_source)
    input_source.close()
    return json_input


class Test(unittest.TestCase):
    """ Class for test fixtures """

    def test_create_xml_element(self):
        """ test _create_xml_elemen """
        xml = _create_xml_element('a', 'b')
        self.assertTrue(ElementTree.tostring(xml) == b'<a>b</a>')

    def test_get_json_value(self):
        """ test _get_json_value """
        json_input = get_json_input()
        text = _get_json_value(json_input, 'recordId')
        self.assertTrue(text == '1976.057')

    def test_get_media_and_display(self):
        """ test _get_media_and_display(json_input) """
        json_input = get_json_input()
        text = _get_media_and_display(json_input)
        self.assertTrue(text == 'oil on canvas, 76 1/2 x 102 x 3 1/4 in. (194.31 x 259.08 x 8.26 cm)')

    def test_get_exhibition(self):
        """ test _get_exhibition """
        json_input = get_json_input()
        if 'exhibition' in json_input:
            for exhibition_json in json_input['exhibition']:
                if 'name' in exhibition_json:
                    text = _get_exhibition(exhibition_json)
                    self.assertTrue(text == 'Picturing History (09/01/94 - 12/01/94)')

    def test_create_search_section(self):
        """ test _create_search_section """
        json_input = get_json_input()
        xml = _create_search_section(json_input)
        create_directory('actual_results')
        create_directory('expected_results')
        actual_results_file_name = 'actual_results/test_create_search_section.xml'
        expected_results_file_name = 'expected_results/test_create_search_section.xml'
        write_pnx_file('.', actual_results_file_name, ElementTree.ElementTree(xml))
        actual_results = ElementTree.ElementTree(file=actual_results_file_name)
        expected_results = ElementTree.ElementTree(file=expected_results_file_name)
        # print(ElementTree.tostring(xml_tree.getroot()))
        self.assertTrue(ElementTree.tostring(actual_results.getroot())
                        == ElementTree.tostring(expected_results.getroot()))

    def test_create_browse_section(self):
        """ test _create_browse_section """
        json_input = get_json_input()
        xml = _create_browse_section(json_input)
        create_directory('actual_results')
        create_directory('expected_results')
        actual_results_file_name = 'actual_results/test_create_browse_section.xml'
        write_pnx_file('.', actual_results_file_name, ElementTree.ElementTree(xml))
        actual_results = ElementTree.ElementTree(file=actual_results_file_name)
        expected_results_file_name = 'expected_results/test_create_browse_section.xml'
        expected_results = ElementTree.ElementTree(file=expected_results_file_name)
        self.assertTrue(ElementTree.tostring(actual_results.getroot())
                        == ElementTree.tostring(expected_results.getroot()))

    def test_create_sort_section(self):
        """ test _create_sort_section """
        json_input = get_json_input()
        xml = _create_sort_section(json_input)
        create_directory('actual_results')
        create_directory('expected_results')
        actual_results_file_name = 'actual_results/test_create_sort_section.xml'
        write_pnx_file('.', actual_results_file_name, ElementTree.ElementTree(xml))
        actual_results = ElementTree.ElementTree(file=actual_results_file_name)
        expected_results_file_name = 'expected_results/test_create_sort_section.xml'
        expected_results = ElementTree.ElementTree(file=expected_results_file_name)
        self.assertTrue(ElementTree.tostring(actual_results.getroot())
                        == ElementTree.tostring(expected_results.getroot()))

    def test_create_facet_section(self):
        """ test _create_facet_section """
        json_input = get_json_input()
        xml = _create_facet_section(json_input)
        create_directory('actual_results')
        create_directory('expected_results')
        actual_results_file_name = 'actual_results/test_create_facet_section.xml'
        write_pnx_file('.', actual_results_file_name, ElementTree.ElementTree(xml))
        actual_results = ElementTree.ElementTree(file=actual_results_file_name)
        expected_results_file_name = 'expected_results/test_create_facet_section.xml'
        expected_results = ElementTree.ElementTree(file=expected_results_file_name)
        self.assertTrue(ElementTree.tostring(actual_results.getroot())
                        == ElementTree.tostring(expected_results.getroot()))

    def test_create_delivery_section(self):
        """ test _create_delivery_section """
        json_input = get_json_input()
        xml = _create_delivery_section(json_input)
        create_directory('actual_results')
        create_directory('expected_results')
        actual_results_file_name = 'actual_results/test_create_delivery_section.xml'
        write_pnx_file('.', actual_results_file_name, ElementTree.ElementTree(xml))
        actual_results = ElementTree.ElementTree(file=actual_results_file_name)
        expected_results_file_name = 'expected_results/test_create_delivery_section.xml'
        expected_results = ElementTree.ElementTree(file=expected_results_file_name)
        self.assertTrue(ElementTree.tostring(actual_results.getroot())
                        == ElementTree.tostring(expected_results.getroot()))

    def test_create_pnx_from_json(self):
        """ run test to create PNX record for a single item from a single JSON file """
        json_input = get_json_input()
        xml_tree = create_pnx_from_json(json_input)
        create_directory('actual_results')
        create_directory('expected_results')
        actual_results_file_name = 'actual_results/test_create_pnx_from_json.xml'
        expected_results_file_name = 'expected_results/test_create_pnx_from_json.xml'
        write_pnx_file('.', actual_results_file_name, xml_tree)
        actual_results = ElementTree.ElementTree(file=actual_results_file_name)
        expected_results = ElementTree.ElementTree(file=expected_results_file_name)
        # print(ElementTree.tostring(xml_tree.getroot()))
        self.assertTrue(ElementTree.tostring(actual_results.getroot())
                        == ElementTree.tostring(expected_results.getroot()))

    def test_create_pnx_from_json_and_write_file(self):
        """ run test to create PNX record for a single item from a single JSON file """
        json_input = get_json_input()
        xml_created = create_pnx_from_json(json_input)
        xml_written = create_pnx_from_json_and_write_file('pnx', json_input)
        self.assertTrue(ElementTree.tostring(xml_created.getroot()) == ElementTree.tostring(xml_written.getroot()))


def compare_files(file_1, file_2, diff_file_name):
    """ Compare Files to capture differences """
    with open(file_1, 'r') as f_1:
        with open(file_2, 'r') as f_2:
            difference = set(f_1).difference(f_2)
    # toss newline differences
    difference.discard('\n')
    if diff_file_name > '':
        with open(diff_file_name, 'w') as file_out:
            for line in difference:
                file_out.write(line)
    return difference


def suite():
    """ define test suite """
    return unittest.TestLoader().loadTestsFromTestCase(Test)


if __name__ == '__main__':
    suite()
    unittest.main()
