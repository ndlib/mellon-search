# test_recreate_pnx_record.py
""" test recreate_pnx_record """

import unittest
from xml.etree.ElementTree import ElementTree

# add parent directory to path
import os
import inspect
import sys
CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PARENTDIR = os.path.dirname(CURRENTDIR)
sys.path.insert(0, PARENTDIR)


from recreate_pnx_record import recreate_pnx_record, get_unique_identifier_from_original_pnx
from get_existing_pnx_record import get_pnx_given_filename


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

    def test_recreate_pnx_record(self):
        """test recreate_pnx_record"""
        actual_results_file_name = 'pnx/ndu_aleph000909884.xml'
        try:
            # remove existing results to make sure we are recreating the file
            os.remove(actual_results_file_name)
        except FileNotFoundError:
            pass
        recreate_pnx_record('ndu_aleph000909884')
        # self.assertTrue(isinstance(resulting_pnx, ElementTree))
        actual_results_file_name = 'pnx/ndu_aleph000909884.xml'
        # expected_results_file_name = 'expected_results/modified_ndu_aleph000909884.xml'
        try:
            ElementTree(file=actual_results_file_name)
        except FileNotFoundError:
            self.assertTrue(False)
        self.assertTrue(True)


def suite():
    """ define test suite """
    return unittest.TestLoader().loadTestsFromTestCase(Test)


# if __name__ == '__main__':
#     suite()
#     unittest.main()
