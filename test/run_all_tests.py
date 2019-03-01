"""Run all tests associated with this package.

Run by executing Python3 run_all_tests.py (do not use -m)
"""

import unittest
import os
# from hesburgh import heslog
import test_create_json_items_from_embark_xml
import test_create_pnx_from_json
import test_get_embark_xml_definitions
import test_get_individual_field_from_embark_xml
import test_get_json_values
import test_get_valid_date
import test_parse_embark_xml
import test_read_embark_fields_json_file
import test_write_main_csv

modules = [test_create_json_items_from_embark_xml,
           test_create_pnx_from_json,
           test_get_embark_xml_definitions,
           test_get_individual_field_from_embark_xml,
           test_get_json_values,
           test_get_valid_date,
           test_parse_embark_xml,
           test_read_embark_fields_json_file,
           test_write_main_csv]

TESTS_ = []
for module in modules:
    TESTS_.append(module.suite())

ALL_TESTS_ = unittest.TestSuite(TESTS_)


if __name__ == '__main__':
    # Set seret for encode/decode to use
    os.environ["JWT_SECRET"] = 'secret'
    # Hide most (if not all) heslogs
    # heslog.setLevels(heslog.LEVEL_TEST)

    unittest.TextTestRunner(verbosity=2).run(ALL_TESTS_)
