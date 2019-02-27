# create_json_items_from_embark_xml.py 2/5/19 sm.
r"""This translates EmbArk XML to PNX XML.

This is the first module in a series of modules to first create a JSON \
file given EmbArk xml.  From that JSON, we then create a PNX record \
and a main.csv file for each item in the original EmbArk XML. \
"""

from __future__ import print_function

import os
import sys
import json
from xml.etree.ElementTree import ElementTree
from parse_embark_xml import ParseEmbarkXml
from read_embark_fields_json_file import read_embark_fields_json_file
from get_embark_xml_definitions import get_item_xpath, get_fields_definition
from create_pnx_from_json import create_pnx_from_json_and_write_file
import write_main_csv


def create_directory(directory):
    """ create directory if it does not exist """
    if not os.path.exists(directory):
        os.makedirs(directory)


def write_json_output(directory, filename, json_data):
    """Write JSON to file whose name is passed."""
    try:
        create_directory(directory)
        filename = directory + '/' + filename
        with open(filename, 'w') as outfile:
            json.dump(json_data, outfile)
    except OSError:
        print('Unable to write JSON data to output file named ' + filename)
        raise


def create_json_items_from_embark_xml(embark_xml_filename, pnx_output_directory='pnx', csv_output_root_directory='mellon_input_directory'):
    """Create JSON representation of each item from embark xml file."""
    try:
        embark_xml_doc = ElementTree(file=embark_xml_filename)
    except OSError:
        print('Unable to open the file you specified. Please try again.')
        raise
    else:
        emb_ark_field_definitions = read_embark_fields_json_file()
        xpath_of_embark_item = get_item_xpath(emb_ark_field_definitions)
        fields_definition = get_fields_definition(emb_ark_field_definitions)
        # Loop through each EmbArk record, processing each individually
        for xml_of_embark_item in embark_xml_doc.findall(xpath_of_embark_item):
            json_of_embark_item = {}
            try:
                embark_instance = ParseEmbarkXml(fields_definition)
                json_of_embark_item = embark_instance.parse_embark_record(xml_of_embark_item)
            except ValueError:
                print('EmbArk Item didn\'t process as expected.')
                # We will need to add some logging here
                raise
            else:
                mellon_input_directory = csv_output_root_directory + '/' + embark_instance.id
                write_json_output(mellon_input_directory, embark_instance.id + '.json', json_of_embark_item)
                create_pnx_from_json_and_write_file(pnx_output_directory, json_of_embark_item)
                write_main_csv.write_main_csv(
                    mellon_input_directory, json_of_embark_item)


if __name__ == "__main__":
    XML_FILENAME = ''
    PNX_OUTPUT_DIRECTORY = ''
    if len(sys.argv) >= 1:
        XML_FILENAME = ''.join(sys.argv[1])
    if XML_FILENAME > '':
        create_json_items_from_embark_xml(XML_FILENAME)
