#test_get_valid_date.py 2/13/19 sm

import unittest
from get_valid_date import get_valid_iso_date, get_valid_yyyymmdd_date

class TestGetValidDate(unittest.TestCase):
    def test_get_valid_iso_date_1(self):
        self.assertTrue(get_valid_iso_date('2019-02-07') == '2019-02-07')

    def test_get_valid_iso_date_2(self):
        self.assertTrue(get_valid_iso_date('2019-02') == '2019-02-01')

    def test_get_valid_iso_date_3(self):
        self.assertTrue(get_valid_iso_date('2019') == '2019-01-01')

    def test_get_valid_iso_date_4(self):
        self.assertTrue(get_valid_iso_date('20190207') == '2019-02-07')

    def test_get_valid_iso_date_5(self):
        self.assertTrue(get_valid_iso_date('201902') == '2019-02-01')

    def test_get_valid_iso_date_6(self):
        self.assertTrue(get_valid_iso_date('2019 - 2019') == '2019-01-01')

    def test_get_valid_iso_date_7(self):
        self.assertTrue(get_valid_iso_date('2019-02-07') == '2019-02-07')

    def test_get_valid_iso_date_8(self):
        self.assertTrue(get_valid_iso_date('2/7/2019') == '2019-02-07')

    def test_get_valid_iso_date_9(self):
        self.assertTrue(get_valid_iso_date('0 - 0') == '')

    def test_get_valid_iso_date_10(self):
        self.assertTrue(get_valid_iso_date('abc') == '')

    def test_get_valid_yyyymmdd_date1(self):
        self.assertTrue(get_valid_yyyymmdd_date('2019-02-07') == '20190207')

    def test_get_valid_yyyymmdd_date2(self):
        self.assertTrue(get_valid_yyyymmdd_date('18910101') == '18910101')

if __name__ == '__main__':
    unittest.main()
