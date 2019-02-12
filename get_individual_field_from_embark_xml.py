# get_individual_field_from_embark_xml.py 2/12/19 sm
""" This module will accept an individual JSON field definition and will use that definition to retrieve
    data from EmbArk XML (also passed). """

from xml.etree.ElementTree import ElementTree
import json
import get_embark_xml_definitions
import read_embark_fields_json_file
import get_valid_date

def _starts_with_ok(text, starts_with):
    ''' This returns True if text starts with the string (if any) in starts_with.    Else False '''
    if (starts_with == "") or text.startswith(starts_with):
        return True
    return False

def _does_not_start_with_ok(text, does_not_start_with):
    ''' This returns True if text does not start with the string (if any) in startsWith.
        Else return False '''
    if (does_not_start_with == "") or not text.startswith(does_not_start_with):
        return True
    return False

class GetEmbarkField():
    ''' Class does heavy lifting translating XML to JSON '''

    def __init__(self, field_definition):
        ''' Initialize fields_definition only once for local use later '''
        self.result_json = {}
        self.field_definition = field_definition
        self.error = []
        self.output = {}
        self.field = {}
        self.field['name'] = get_embark_xml_definitions.get_field_name(field_definition)
        self.field['required'] = get_embark_xml_definitions.get_field_required(field_definition)
        self.field['duplicates_allowed'] = get_embark_xml_definitions.get_field_duplicates_allowed(field_definition)
        self.field['xpath'] = get_embark_xml_definitions.get_field_xpath(field_definition)
        self.field['does_not_start_with'] = get_embark_xml_definitions.get_does_not_start_with(field_definition)
        self.field['starts_with'] = get_embark_xml_definitions.get_starts_with(field_definition)
        self.field['validation'] = get_embark_xml_definitions.get_validation_rule(field_definition)
        self.field['constant'] = get_embark_xml_definitions.get_constant(field_definition)

    def load_json_field_definition(self, field_definition):
        ''' This allows the user to move to pass a new field definition '''
        self.__init__(field_definition)

    def get_json_representation_of_field(self, embark_item_xml):
        ''' This retrieves an individual field (possibly as an array)
            from EmbArk XML and saves to JSON '''
        json_for_this_field = {}
        try:
            if self.field['constant'] > "": # Use this for "repository", which doesn't exist in XML
                json_for_this_field[self.field['name']] = self.field['constant']
            elif self.field['name'] == 'exhibition': # exhibitions have highly unusual XML format
                json_for_this_field = self._get_exhibition_information(embark_item_xml)
            else:
                json_for_this_field = self._get_node(embark_item_xml)
        except ValueError:
            print('get_individual_field_from_embark_xml.get_json_represetation_of_field encountered an error.')
            json_for_this_field = {}
            raise
        return json_for_this_field

    def _get_node(self, embark_item_xml):
        ''' This retrieves an individual value (or array) from XML
            , optionally validates it, and saves to JSON '''
        node = {}
        self._validate_record_count(embark_item_xml)
        for item in embark_item_xml.findall(self.field['xpath']):
            this_item = {}
            value_found = ""
            if _starts_with_ok(item.text, self.field['starts_with']) and _does_not_start_with_ok(item.text, self.field['does_not_start_with']):
                value_found = item.text
            if self.field['validation'] == 'validateYYYYMMDD' and value_found > '':
                value_found = get_valid_date.get_valid_yyyymmdd_date(value_found)
# bump this up a level
#            if self.field['name'] == 'recordId':
#                self.id = value_found
            if self.field['duplicates_allowed']:
                this_item["value"] = value_found
                if self.field['name'] not in node:
                    node[self.field['name']] = []
                node[self.field['name']].append(this_item)
            else:
                this_item[self.field['name']] = value_found
                node = this_item
                break #if duplicates are not allowed, only accept first occurrence
        return node


    def _get_exhibition_information(self, embark_item_xml):
        ''' This is to accommodate the special (crazy) data format which represents exhibitions '''
        exhibition_node = {}
        exhibition_node[self.field['name']] = []
        exhibition_iterator = -1
        for item in embark_item_xml.findall(self.field['xpath']):
            this_item = {}
            exhibition_iterator += 1
            this_item["name"] = item.text # Capture the name of the exhibit
            date_group_iterator = -1
            for start_date_group in embark_item_xml.findall('./group[@id=\'object_00001\']'):
                #note:    first group record is start_date
                #second group record is EndDate (although both are called StartDate)
                date_group_iterator += 1
                individual_date_iterator = -1
                if date_group_iterator == 0: #start_date
                    for start_date in start_date_group.findall('./variable[@id=\'object_00001\']'):
                        individual_date_iterator += 1
                        if individual_date_iterator == exhibition_iterator:
                            this_item["startDate"] = start_date.text
                else: #EndDate (Note: the XML calls End_Date by the name of Start_Date.
                    #End_Date is the second occurance of Start_Date.)
                    for end_date in start_date_group.findall('./variable[@id=\'object_00001\']'):
                        individual_date_iterator += 1
                        if individual_date_iterator == exhibition_iterator:
                            this_item["endDate"] = end_date.text
            exhibition_node[self.field['name']].append(this_item)
        return exhibition_node


    def _validate_record_count(self, embark_item_xml):
        ''' This ensures required fields exist '''
        error_text = ""
        error = {}
        element_count = len(embark_item_xml.findall(self.field['xpath']))
        if element_count == 0 and self.field['required']:
            error_text = 'Required field ' + self.field['name'] + ' is missing.    Unable to process record '
            error["ValueError"] = error_text
            raise ValueError(error_text)
        return error


# Tests
# python3 -c 'from get_individual_field_from_embark_xml import *; test("example/objects 01_18_19.xml")'
def test(filename='example/objects 01_18_19.xml'):
    ''' Run all tests for this module '''
    _test_starts_with()
    _test_read_and_parse(filename)

def _test_read_and_parse(filename):
    ''' test Read and Parse '''
    xmldoc = ElementTree(file=filename)
    filename = "./EmbArkXMLFields.json"
    embark_field_definitions = read_embark_fields_json_file.read_and_validate_embark_field_definitions_file(filename)
    item_xpath = get_embark_xml_definitions.get_item_xpath(embark_field_definitions)
    #fields_definition = get_embark_xml_definitions.get_fields_definition(embark_field_definitions)
    for xml_of_embark_item in xmldoc.findall(item_xpath):
        # xml_of_embark_item contains EmbArk xml for one item.
        json_of_embark_field = {}
        field_definition = json.loads('{"name": "recordId","required": true,"duplicatesAllowed": false,"xpath": "./variable[@id=\'object_00055\']"}')
        #field_definition = json.loads('{"name": "creator","required": false,"duplicatesAllowed": false,"xpath": "./variable[@id=\'object_00060\']"}')
        field = GetEmbarkField(field_definition)
        json_of_embark_field = field.get_json_representation_of_field(xml_of_embark_item)
        #print(json_of_embark_field)


def _test_starts_with():
    ''' Test Starts With and Does Not Start With routines '''
    assert _starts_with_ok('abc123', 'abc')
    assert not _starts_with_ok('abc123', '123')
    assert _starts_with_ok('abc123', '')
    assert _does_not_start_with_ok('abc123', '')
    assert _does_not_start_with_ok('abc123', '123')
    assert not _does_not_start_with_ok('abc123', 'abc')
