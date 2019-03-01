# test_parse_embark_xml.py 2/19/19 sm
""" test parse_embark_xml.py """

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

from parse_embark_xml import ParseEmbarkXml
import read_embark_fields_json_file
import get_embark_xml_definitions


class Test(unittest.TestCase):
    """ Class for test fixtures """

    def test_read_and_parse(self):
        """ test Read and Parse """
        xmldoc = ElementTree(file='./objects 01_18_19.xml')
        filename = PARENTDIR + "/EmbArkXMLFields.json"
        embark_field_definitions = read_embark_fields_json_file.read_embark_fields_json_file(filename)
        item_xpath = get_embark_xml_definitions.get_item_xpath(embark_field_definitions)
        fields_definition = get_embark_xml_definitions.get_fields_definition(embark_field_definitions)
        for xml_of_embark_item in xmldoc.findall(item_xpath):
            # xml_of_embark_item contains EmbArk xml for one item.
            json_of_embark_item = {}
            section = ParseEmbarkXml(fields_definition)
            json_of_embark_item = section.parse_embark_record(xml_of_embark_item)
            if section.id == "1976.057":
                with open('./expected_results/test_read_and_parse.json', 'r') as input_source:
                    expected_json = json.load(input_source)
                input_source.close()
                self.assertTrue(expected_json == json_of_embark_item)


def suite():
    """ define test suite """
    return unittest.TestLoader().loadTestsFromTestCase(Test)


if __name__ == '__main__':
    unittest.main()
