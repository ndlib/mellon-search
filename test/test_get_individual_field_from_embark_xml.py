# test_get_individual_field_from_embark_xml.py 2/18/19 sm
""" test get_individual_field_from_embark_xml.py """

import json
import unittest
from xml.etree.ElementTree import ElementTree

# add parent directory to path
import os
import inspect
import sys
CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PARENTDIR = os.path.dirname(CURRENTDIR)
sys.path.insert(0, PARENTDIR)

from get_individual_field_from_embark_xml import GetEmbarkField, _starts_with_ok, _does_not_start_with_ok


class Test(unittest.TestCase):
    """ Class for test fixtures """

    def get_xml_doc(self):
        """ Need to load xml internally to control contents for testing """
        try:
            embark_xml_doc = ElementTree(file='./sample_xml_for_testing.xml')
        except OSError:
            print('Unable to open the file you specified. Please try again.')
            raise
        return embark_xml_doc

    def test_read_record_id(self):
        """ test Read and Parse """
        xml_of_embark_item = self.get_xml_doc()
        json_of_embark_field = {}
        field_definition = json.loads('{"name": "recordId","required": true,"duplicatesAllowed": false,'
                                      + '"xpath": "./variable[@id=\'object_00055\']"}')
        field = GetEmbarkField(field_definition)
        json_of_embark_field = field.get_json_representation_of_field(xml_of_embark_item)
        self.assertTrue(json.loads('{"recordId": "1976.057"}') == json_of_embark_field)

    def test_read_constant(self):
        """ test Read and Parse """
        xml_of_embark_item = self.get_xml_doc()
        json_of_embark_field = {}
        field_definition = json.loads('{"name": "repository","required": false,"duplicatesAllowed": false,'
                                      + '"xpath": "required, but not used here.","constant": "Snite"}')
        field = GetEmbarkField(field_definition)
        json_of_embark_field = field.get_json_representation_of_field(xml_of_embark_item)
        self.assertTrue(json.loads('{"repository": "Snite"}') == json_of_embark_field)

    def test_read_creator(self):
        """ test Read and Parse """
        xml_of_embark_item = self.get_xml_doc()
        json_of_embark_field = {}
        field_definition = json.loads('{"name": "creator","required": false,"duplicatesAllowed": false,'
                                      + '"xpath": "./variable[@id=\'object_00060\']"}')
        field = GetEmbarkField(field_definition)
        json_of_embark_field = field.get_json_representation_of_field(xml_of_embark_item)
        self.assertTrue(json.loads('{"creator": "Paul Wood"}') == json_of_embark_field)

    def test_read_creation_date(self):
        """ test Read and Parse """
        xml_of_embark_item = self.get_xml_doc()
        json_of_embark_field = {}
        field_definition = json.loads('{"name": "creationDate","required": false,"duplicatesAllowed": false,'
                                      + '"xpath": "./variable[@id=\'object_00062\']",'
                                      + '"validation": "validateYYYYMMDD"}')
        field = GetEmbarkField(field_definition)
        json_of_embark_field = field.get_json_representation_of_field(xml_of_embark_item)
        self.assertTrue(json.loads('{"creationDate": "18910101"}') == json_of_embark_field)

    def test_read_exhibition(self):
        """ test Read and Parse """
        xml_of_embark_item = self.get_xml_doc()
        json_of_embark_field = {}
        field_definition = json.loads('{"name": "exhibition","required": false,"duplicatesAllowed": true,"xpath":'
                                      + ' "./group[@id=\'object_00002\']/variable[@id=\'object_00002\']"}')
        field = GetEmbarkField(field_definition)
        json_of_embark_field = field.get_json_representation_of_field(xml_of_embark_item)
        self.assertTrue(json.loads('{"exhibition": [{"name": "Picturing History", "startDate": "09/01/94",'
                                   + '"endDate": "12/01/94"}]}') == json_of_embark_field)

    def test_read_keyword(self):
        """ test keyword """
        xml_of_embark_item = self.get_xml_doc()
        json_of_embark_field = {}
        field_definition = json.loads('{"name": "keyword","required": false,"duplicatesAllowed": true,"xpath":'
                                      + '"./group[@id=\'object_00080\']/variable[@id=\'object_00080\']"}')
        field = GetEmbarkField(field_definition)
        json_of_embark_field = field.get_json_representation_of_field(xml_of_embark_item)
        for keyword in json_of_embark_field['keyword']:
            value = keyword['value']
            self.assertTrue(value == 'confederate')
            break

    def test_read_default(self):
        """ test default """
        xml_of_embark_item = self.get_xml_doc()
        json_of_embark_field = {}
        field_definition = json.loads('{"name": "classification","required": false,"duplicatesAllowed": false,'
                                      + '"xpath": "./variable[@name=\'[Object]Class 2\']","default": "painting"}')
        field = GetEmbarkField(field_definition)
        json_of_embark_field = field.get_json_representation_of_field(xml_of_embark_item)
        # print(json_of_embark_field)
        self.assertTrue(json.loads('{"classification": "painting"}') == json_of_embark_field)

    def test_try_to_throw_required_value_missing_error(self):
        """ test default """
        xml_of_embark_item = self.get_xml_doc()
        json_of_embark_field = {}
        field_definition = json.loads('{"name": "classification","required": true,"duplicatesAllowed":'
                                      + ' false,"xpath": "./variable[@name=\'[Object]Class 2\']"}')
        field = GetEmbarkField(field_definition)
        self.assertRaises(ValueError, field.get_json_representation_of_field, xml_of_embark_item)
        field_definition = json.loads('{"name": "classification","required": true,"duplicatesAllowed":'
                                      + ' false,"xpath": "./variable[@name=\'[Object]Class 2\']","default":'
                                      + ' "painting"}')
        field.load_json_field_definition(field_definition)
        json_of_embark_field = field.get_json_representation_of_field(xml_of_embark_item)
        self.assertTrue(json.loads('{"classification": "painting"}') == json_of_embark_field)

    def test_starts_with(self):
        """ Test Starts With and Does Not Start With routines """
        self.assertTrue(_starts_with_ok('abc123', 'abc'))
        self.assertTrue(not _starts_with_ok('abc123', '123'))
        self.assertTrue(_starts_with_ok('abc123', ''))
        self.assertTrue(_does_not_start_with_ok('abc123', ''))
        self.assertTrue(_does_not_start_with_ok('abc123', '123'))
        self.assertTrue(not _does_not_start_with_ok('abc123', 'abc'))


def suite():
    """ define test suite """
    return unittest.TestLoader().loadTestsFromTestCase(Test)


if __name__ == '__main__':
    suite()
    unittest.main()
