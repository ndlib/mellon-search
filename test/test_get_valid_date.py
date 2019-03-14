# test_get_valid_date.py 2/13/19 sm
""" test get_valid_date.py """

import unittest

# add parent directory to path
import os
import inspect
import sys
CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PARENTDIR = os.path.dirname(CURRENTDIR)
sys.path.insert(0, PARENTDIR)

from get_valid_date import get_valid_iso_date, get_valid_yyyymmdd_date


class Test(unittest.TestCase):
    """ class for all date tests """
    def test_get_valid_iso_date_1(self):
        """ test iso YYYY-MM-DD date """
        self.assertTrue(get_valid_iso_date('2019-02-07') == '2019-02-07')

    def test_get_valid_iso_date_2(self):
        """ test iso YYYY-MM date """
        self.assertTrue(get_valid_iso_date('2019-02') == '2019-02-01')

    def test_get_valid_iso_date_3(self):
        """ test YYYY date """
        self.assertTrue(get_valid_iso_date('2019') == '2019-01-01')

    def test_get_valid_iso_date_4(self):
        """ test YYYYMMDD date """
        self.assertTrue(get_valid_iso_date('20190207') == '2019-02-07')

    def test_get_valid_iso_date_5(self):
        """ test YYYYMM date """
        self.assertTrue(get_valid_iso_date('201902') == '2019-02-01')

    def test_get_valid_iso_date_6(self):
        """ test range of years, like YYYY - YYYY """
        self.assertTrue(get_valid_iso_date('2019 - 2019') == '2019-01-01')

    def test_get_valid_iso_date_7(self):
        """ test MM/DD/YYYY format """
        self.assertTrue(get_valid_iso_date('2/7/2019') == '2019-02-07')

    def test_get_valid_iso_date_8(self):
        """ blank out 0 date """
        self.assertTrue(get_valid_iso_date('0 - 0') == '')

    def test_get_valid_iso_date_9(self):
        """ non-valid dates return empty string """
        self.assertTrue(get_valid_iso_date('abc') == '')

    def test_get_valid_yyyymmdd_date1(self):
        """ verify conversion to YYYYMMDD format for output string """
        self.assertTrue(get_valid_yyyymmdd_date('2019-02-07') == '20190207')

    def test_get_valid_yyyymmdd_date2(self):
        """ verify YYYYMMDD works for different centuries too """
        self.assertTrue(get_valid_yyyymmdd_date('18910101') == '18910101')

    def test_get_valid_yyyymmdd_date3(self):
        """ verify YYYYMMDD returns empty string for invalid dates """
        self.assertTrue(get_valid_yyyymmdd_date('abc') == '')


def suite():
    """ define test suite """
    return unittest.TestLoader().loadTestsFromTestCase(Test)


if __name__ == '__main__':
    suite()
    unittest.main()
