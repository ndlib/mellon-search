# test_get_embark_xml_definitions.py 2/18/19 sm
""" test get_embark_xml_definitions.py """

import json
import unittest

# add parent directory to path
import os
import inspect
import sys
CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PARENTDIR = os.path.dirname(CURRENTDIR)
sys.path.insert(0, PARENTDIR)

import get_embark_xml_definitions


class Test(unittest.TestCase):
    """ Class for test fixtures """

    def test_get_item_xpath(self):
        """test retrieving known item xpath"""
        original_path = '{"itemPath": "./Section[@name=\'Body\'][@id=\'section_07\']",	"FieldsToExtract": []}'
        embark_field_definitions = json.loads(original_path)
        item_xpath = get_embark_xml_definitions.get_item_xpath(embark_field_definitions)
        self.assertTrue(item_xpath == embark_field_definitions['itemPath'])

    def test_get_fields_definition(self):
        """ test retrieving known fields definition """
        embark_field_definitions = json.loads('{"xitemPath": "./Section[@name=\'Body\'][@id=\'section_07\']",'
                                              + '"FieldsToExtract": [{"name": "recordId", "required": true, '
                                              + '"duplicatesAllowed": false, "xpath":'
                                              + ' "./variable[@id=\'object_00055\']"}]}')
        fields_definitions = get_embark_xml_definitions.get_fields_definition(embark_field_definitions)
        self.assertTrue(fields_definitions == embark_field_definitions['FieldsToExtract'])

    def test_get_field_name(self):
        """ test retrieving known field name """
        embark_field_definition = json.loads('{"name": "recordId", "required": true, "duplicatesAllowed": false,'
                                             + ' "xpath": "./variable[@id=\'object_00055\']"}')
        name = get_embark_xml_definitions.get_field_name(embark_field_definition)
        self.assertTrue(name == embark_field_definition['name'])

    def test_get_field_required(self):
        """ test retrieving known field required """
        embark_field_definition = json.loads('{"name": "recordId", "required": true, "duplicatesAllowed": false,'
                                             + ' "xpath": "./variable[@id=\'object_00055\']"}')
        required = get_embark_xml_definitions.get_field_required(embark_field_definition)
        self.assertTrue(required == embark_field_definition['required'])
        self.assertTrue(required)

    def test_get_field_duplicates_allowed(self):
        """ test retrieving known Duplicates Allowed """
        embark_field_definition = json.loads('{"name": "recordId", "required": true, "duplicatesAllowed": false,'
                                             + ' "xpath": "./variable[@id=\'object_00055\']"}')
        duplicates_allowed = get_embark_xml_definitions.get_field_duplicates_allowed(embark_field_definition)
        self.assertTrue(duplicates_allowed == embark_field_definition['duplicatesAllowed'])
        self.assertTrue(not duplicates_allowed)

    def test_get_field_xpath(self):
        """ test retrieving known field xpath """
        embark_field_definition = json.loads('{"name": "recordId", "required": true, "duplicatesAllowed": false,'
                                             + ' "xpath": "./variable[@id=\'object_00055\']"}')
        xpath = get_embark_xml_definitions.get_field_xpath(embark_field_definition)
        self.assertTrue(xpath == embark_field_definition['xpath'])

    def test_get_does_not_start_with(self):
        """ test retrieving known Does Not Start With """
        embark_field_definition = json.loads('{"duplicatesAllowed": false, "xpath": "./variable[@id=\'object_00055\']"'
                                             + ',"doesNotStartWith": "AAT:" }')
        does_not_start_with = get_embark_xml_definitions.get_does_not_start_with(embark_field_definition)
        self.assertTrue(does_not_start_with == embark_field_definition['doesNotStartWith'])
        self.assertTrue(does_not_start_with == "AAT:")

    def test_get_starts_with(self):
        """ test retrieving known Starts With """
        embark_field_definition = json.loads('{"required": true, "duplicatesAllowed": false, "xpath":'
                                             + ' "./variable[@id=\'object_00055\']","startsWith": "AAT:" }')
        starts_with = get_embark_xml_definitions.get_starts_with(embark_field_definition)
        self.assertTrue(starts_with == embark_field_definition['startsWith'])
        self.assertTrue(starts_with == "AAT:")

    def test_get_validation_rule(self):
        """ test retrieving known Validation rule """
        embark_field_definition = json.loads('{"required": true, "duplicatesAllowed": false, "xpath":'
                                             + ' "","constant": "Snite","validation":"validateYYYYMMDD" }')
        validation = get_embark_xml_definitions.get_validation_rule(embark_field_definition)
        self.assertTrue(validation == embark_field_definition['validation'])

    def test_get_constant(self):
        """ test retrieving known Constant """
        embark_field_definition = json.loads('{"required": true, "duplicatesAllowed": false, "xpath": "",'
                                             + '"constant": "Snite","validation":"validateYYYYMMDD" }')
        constant = get_embark_xml_definitions.get_constant(embark_field_definition)
        self.assertTrue(constant == embark_field_definition['constant'])

    def test_get_default(self):
        """ test retrieving known Constant """
        embark_field_definition = json.loads('{"required": true, "duplicatesAllowed": false, "xpath": "",'
                                             + '"constant": "Snite","validation":"validateYYYYMMDD",'
                                             + '"default":"painting" }')
        default = get_embark_xml_definitions.get_field_default(embark_field_definition)
        self.assertTrue(default == embark_field_definition['default'])


def suite():
    """ define test suite """
    return unittest.TestLoader().loadTestsFromTestCase(Test)


if __name__ == '__main__':
    suite()
    unittest.main()
