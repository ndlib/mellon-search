# create_json_items_from_embark_xml.py 2/5/19 sm
""" This is the first module in a series of modules to create JSON (and PNX) given EmbArk input. """

import os
import sys
import json
from xml.etree.ElementTree import ElementTree
import parse_embark_xml
import read_embark_fields_json_file
import get_embark_xml_definitions
import create_pnx_from_json
import write_main_csv


def create_directory(directory):
    ''' Create a directory if it doesn't exist '''
    try:
        os.makedirs(directory)
    except FileExistsError:
        pass # directory already exists


def write_json_output(directory, filename, json_data):
    ''' Write JSON to file whose name is passed '''
    try:
        create_directory(directory)
        filename = directory + '/' + filename
        with open(filename, 'w') as outfile:
            json.dump(json_data, outfile)
    except:
        print('Unable to write JSON data to output file named ' + filename)
        raise


def create_json_items_from_embark_xml(embark_xml_filename, pnx_output_directory='pnx', csv_output_root_directory='mellon_input_directory'):
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
                mellon_input_directory = csv_output_root_directory + '/' + parse_embark_xml_instance.id
                write_json_output(mellon_input_directory, parse_embark_xml_instance.id + '.json', json_of_embark_item)
                create_pnx_from_json.create_pnx_from_json_and_write_file(pnx_output_directory, json_of_embark_item)
                write_main_csv.write_main_csv(mellon_input_directory, json_of_embark_item)


if __name__ == "__main__":
    XML_FILENAME = ''
    PNX_OUTPUT_DIRECTORY= ''
    if len(sys.argv) >= 1:
        XML_FILENAME = ''.join(sys.argv[1])
    if XML_FILENAME > '':
        create_json_items_from_embark_xml(XML_FILENAME)
