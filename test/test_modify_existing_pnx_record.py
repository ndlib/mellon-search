# test_modify_existing_pnx_record.py
""" test modify_existing_pnx_record """

import unittest
from xml.etree.ElementTree import ElementTree, tostring

# add parent directory to path
import os
import inspect
import sys
CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PARENTDIR = os.path.dirname(CURRENTDIR)
sys.path.insert(0, PARENTDIR)

from modify_existing_pnx_record import modify_existing_pnx_record, get_unique_identifier_from_original_pnx
from get_existing_pnx_record import get_pnx_given_filename
from write_pnx_file import write_pnx_file


def get_sample_pnx():
    """ Retrieve known sample pnx file for use in testing """
    pnx_filename = './sample.xml'
    resulting_pnx = get_pnx_given_filename(pnx_filename)
    return resulting_pnx


class Test(unittest.TestCase):
    """ Class for test fixtures """

    def test_get_unique_identifier_from_original_pnx(self):
        """test get_unique_identifier_from_original_pnx"""
        sample_pnx = get_sample_pnx()
        unique_identifier = get_unique_identifier_from_original_pnx(sample_pnx)
        # print(unique_identifier)
        self.assertTrue(unique_identifier == "ndu_aleph000909884")

    def test_modify_existing_pnx_record(self):
        """ compare actual an expected 'modified_ndu_aleph000909884.xml' """
        sample_pnx = get_sample_pnx()
        resulting_pnx = modify_existing_pnx_record(sample_pnx, 'snite', 'ndu_aleph000909884')
        self.assertTrue(isinstance(resulting_pnx, ElementTree))
        # need to save resulting_pnx and compare it with known good new pnx
        write_pnx_file('actual_results', 'modified_ndu_aleph000909884.xml', resulting_pnx)
        # now we will read actual and expected results and compare them
        actual_results_file_name = 'actual_results/modified_ndu_aleph000909884.xml'
        expected_results_file_name = 'expected_results/modified_ndu_aleph000909884.xml'
        actual_results = ElementTree(file=actual_results_file_name)
        expected_results = ElementTree(file=expected_results_file_name)
        # print(ElementTree.tostring(xml_tree.getroot()))
        self.assertTrue(tostring(actual_results.getroot()) == tostring(expected_results.getroot()))


def suite():
    """ define test suite """
    return unittest.TestLoader().loadTestsFromTestCase(Test)


# if __name__ == '__main__':
#     suite()
#     unittest.main()
