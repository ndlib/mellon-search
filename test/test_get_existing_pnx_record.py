# test_get_existing_pnx_record.py
""" test get_existing_pnx_record """

import unittest
from xml.etree.ElementTree import Element
from urllib import error

# add parent directory to path
import os
import inspect
import sys
CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PARENTDIR = os.path.dirname(CURRENTDIR)
sys.path.insert(0, PARENTDIR)

from get_existing_pnx_record import get_pnx_given_filename, get_pnx_xml_given_docid


class Test(unittest.TestCase):
    """ Class for test fixtures """

    def test_get_pnx_given_filename(self):
        """ Call get_pnx_given_filename passing a known filename to verify Element is returned. """
        pnx_filename = './sample.xml'
        resulting_pnx = get_pnx_given_filename(pnx_filename)
        self.assertTrue(isinstance(resulting_pnx, Element))

    def test_get_pnx_given_filename_passing_missing_filename(self):
        """ Call get_pnx_given_filename passing a missing filename to verify error is raised. """
        pnx_filename = './xsample.xml'
        self.assertRaises(FileNotFoundError, get_pnx_given_filename, pnx_filename)

    def test_get_pnx_xml_given_docid(self):
        """ call get_pnx_xml_given_docid passing known existing docid """
        docid = 'ndu_aleph000909884'
        resulting_pnx = get_pnx_xml_given_docid(docid)
        self.assertTrue(isinstance(resulting_pnx, Element))

    def test_get_pnx_xml_given_docid_passing_missing_docid(self):
        """ call get_pnx_xml_given_docid passing non-existant docid """
        docid = 'ndu_aleph000909884xyz'
        self.assertRaises(error.HTTPError, get_pnx_xml_given_docid, docid)


def suite():
    """ define test suite """
    return unittest.TestLoader().loadTestsFromTestCase(Test)


# if __name__ == '__main__':
#     suite()
#     unittest.main()
