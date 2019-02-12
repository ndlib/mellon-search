# create_json_items_from_embark_xml.py 2/5/19 sm
""" This is the first module in a series of modules to create JSON (and PNX) given EmbArk input. """

import json
from xml.etree.ElementTree import ElementTree
import parse_embark_xml
import read_embark_fields_json_file
import get_embark_xml_definitions
import create_pnx_from_json

# Get necessary information from JSON control file
# I had problems here trying to pass by reference, with values not being returned as expected
#def getemb_ark_field_definitionsFromFile(xpath_of_embark_item, fields_definition):
#emb_ark_field_definitions = read_embark_fields_json_file.read_and_validate_embark_field_definitions_file ()
#xpath_of_embark_item = get_embark_xml_definitions.get_item_xpath(emb_ark_field_definitions)
#fields_definition = get_embark_xml_definitions.get_fields_definition(emb_ark_field_definitions)


def write_json_output(filename, json_data):
    ''' Write JSON to file whose name is passed '''
    try:
        with open(filename, 'w') as outfile:
            json.dump(json_data, outfile)
    except:
        print('Unable to write JSON data to output file named ' + filename)
        raise


def create_json_items_from_embark_xml(embark_xml_filename):
    ''' Create JSON representation of each item from embark xml file '''
    try:
        embark_xml_doc = ElementTree(file=embark_xml_filename)
    except:
        print('We were not able to open the file you specified. Please supply a valid XML filename and try again.')
        raise
    else:
        emb_ark_field_definitions = read_embark_fields_json_file.read_and_validate_embark_field_definitions_file()
        xpath_of_embark_item = get_embark_xml_definitions.get_item_xpath(emb_ark_field_definitions)
        fields_definition = get_embark_xml_definitions.get_fields_definition(emb_ark_field_definitions)
        #Loop through each EmbArk record, processing each individually
        for xml_of_embark_item in embark_xml_doc.findall(xpath_of_embark_item):
            json_of_embark_item = {}
            try:
                parse_embark_xml_instance = parse_embark_xml.ParseEmbarkXml(fields_definition)
                json_of_embark_item = parse_embark_xml_instance.parse_embark_record(xml_of_embark_item)
            except ValueError:
                print('The XML representing a EmbArk Item didn\'t process as expected.    Please notify someone in IT.')
                #We will need to add some logging here
                raise
            else:
                write_json_output('example/' + parse_embark_xml_instance.id + '.json', json_of_embark_item)
                create_pnx_from_json.create_pnx_from_json(json_of_embark_item)


#tests
# python3 -c 'from create_json_items_from_embark_xml import *; test()'
def test():
    ''' run all tests for this module '''
    _test_create_json_items_from_embark_xml()

def _test_create_json_items_from_embark_xml():
    ''' test creating json item from embark xml '''
    create_json_items_from_embark_xml(embark_xml_filename='example/objects 01_18_19.xml')

#def testReadingJsonFile():
#    xpath_of_embark_item = ""
#    fields_definition = {}
#    filename = "./EmbArkXMLFields.json"
#    #getemb_ark_field_definitionsFromFile(filename, xpath_of_embark_item, fields_definition)
#    print('here')
#    #print(filename)
#    print(xpath_of_embark_item)
#    print(fields_definition)
