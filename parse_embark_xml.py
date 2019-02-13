# parse_embark_xml.py 2/5/19 sm
""" This module will accept JSON field definitions and will use those definitions to retrieve
    data from EmbArk XML (also passed). """

from xml.etree.ElementTree import ElementTree
import get_embark_xml_definitions
import read_embark_fields_json_file
import get_individual_field_from_embark_xml

class ParseEmbarkXml():
    ''' Class does heavy lifting translating XML to JSON '''
    def __init__(self, fields_definition):
        ''' Initialize fields_definition only once for local use later '''
        self.result_json = {}
        self.fields_definition = fields_definition
        self.error = []
        self.id = ""
        self.output = {}


    def parse_embark_record(self, embark_item_xml):
        ''' This translates information from EmbArk XML representing an
            individual museum item to JSON '''
        fields_definition = self.fields_definition
        self.output = {} # reinitialize output record at beginning of each EmbArk Item
        node = {}
        try:
            for field in fields_definition:
                get_embark_field_instance = get_individual_field_from_embark_xml.GetEmbarkField(field)
                node = get_embark_field_instance.get_json_representation_of_field(embark_item_xml)
                if 'recordId' in node:
                    self.id = node['recordId']
                #node = self._get_individual_field(field, embark_item_xml)
                self.output.update(node)
        except ValueError as e:
            self.output = {} #Blank out output if an error was encountered
            error_node = {}
            error_node["ValueError"] = e
            self.error.append(error_node)
            raise
        return self.output

# Tests
# python3 -c 'from parse_embark_xml import *; test("example/objects 01_18_19.xml")'
def test(filename='example/objects 01_18_19.xml'):
    ''' Run all tests for this module '''
    _test_read_and_parse(filename)

def _test_read_and_parse(filename):
    ''' test Read and Parse '''
    xmldoc = ElementTree(file=filename)
    filename = "./EmbArkXMLFields.json"
    embark_field_definitions = read_embark_fields_json_file.read_and_validate_embark_field_definitions_file(filename)
    item_xpath = get_embark_xml_definitions.get_item_xpath(embark_field_definitions)
    fields_definition = get_embark_xml_definitions.get_fields_definition(embark_field_definitions)
    for xml_of_embark_item in xmldoc.findall(item_xpath):
    # xml_of_embark_item contains EmbArk xml for one item.
        json_of_embark_item = {}
        section = ParseEmbarkXml(fields_definition)
        json_of_embark_item = section.parse_embark_record(xml_of_embark_item)
        print(json_of_embark_item)
        print(section.id)
        #break
