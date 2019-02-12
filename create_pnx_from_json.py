#create_pnx_from_json.py 2/6/19 sm
""" This module will transform JSON input into PNX XML output for loading into Primo. """

import json
import xml.etree.ElementTree as ET
#import pprint


def _create_display_section(json_input):
    ''' Create Display Section of Primo Record '''
    display = ET.Element("display")
    ET.SubElement(display, 'lds02').text = json_input['recordId']
    ET.SubElement(display, 'title').text = json_input['title']
    ET.SubElement(display, 'creator').text = json_input['creator']
    ET.SubElement(display, 'creationdate').text = json_input['displayDate']
    ET.SubElement(display, 'format').text = json_input['media'] + ', ' + json_input['displayDimensions']
    ET.SubElement(display, 'lds09').text = json_input['classification']
    ET.SubElement(display, 'type').text = json_input['classification']
    ET.SubElement(display, 'lsd10').text = json_input['repository'].title() # Make sure this is mixed case
    return display

def _create_search_section(json_input):
    ''' Create Search Section of Primo Record '''
    search = ET.Element("search")
    ET.SubElement(search, 'recordid').text = json_input['recordId']
    ET.SubElement(search, 'title').text = json_input['title']
    ET.SubElement(search, 'creator').text = json_input['creator']
    ET.SubElement(search, 'creationdate').text = json_input['creationDate']
    ET.SubElement(search, 'general').text = json_input['media'] + ', ' + json_input['displayDimensions']
    ET.SubElement(search, 'lsr09').text = json_input['classification']
    ET.SubElement(search, 'rsrctype').text = json_input['classification']
    ET.SubElement(search, 'scope').text = json_input['repository'].upper() # Make sure this is upper case
    return search


def _create_browse_section(json_input):
    ''' Create Browse Section of Primo Record '''
    browse = ET.Element("browse")
    ET.SubElement(browse, 'title').text = json_input['title']
    ET.SubElement(browse, 'author').text = json_input['creator']
    ET.SubElement(browse, 'institution').text = json_input['repository'].upper() # Make sure this is upper case
    return browse

def _create_sort_section(json_input):
    ''' Create Sort Section of Primo Record '''
    sort = ET.Element("sort")
    ET.SubElement(sort, 'title').text = json_input['title']
    ET.SubElement(sort, 'author').text = json_input['creator']
    ET.SubElement(sort, 'creationdate').text = json_input['creationDate']
    return sort

def _create_facet_section(json_input):
    ''' Create Facet Section of Primo Record '''
    facet = ET.Element("facet")
    ET.SubElement(facet, 'creatorcontrib').text = json_input['creator']
    ET.SubElement(facet, 'lfc09').text = json_input['classification']
    ET.SubElement(facet, 'rsrctype').text = json_input['classification']
    ET.SubElement(facet, 'library').text = json_input['repository'].upper()
    ET.SubElement(facet, 'creationdate').text = json_input['creationDate']
    return facet

def create_pnx_from_json(json_input):
    ''' Create PNX Record for Primo '''
    root = ET.Element("record")
    ET.SubElement(root, 'id').text = json_input['recordId']
    root.append(_create_display_section(json_input))
    root.append(_create_search_section(json_input))
    root.append(_create_browse_section(json_input))
    root.append(_create_sort_section(json_input))
    root.append(_create_facet_section(json_input))
    tree = ET.ElementTree(root)
    tree.write('example/' + json_input['recordId'] + '.xml')


# python3 -c 'from create_pnx_from_json import *; test("example/1976.057.json")'
def test(filename):
    ''' run test to create PNX record for a single item from a single JSON file '''
    try:
        with open(filename, 'r') as input_source:
            json_input = json.load(input_source)
        input_source.close()
    except IOError:
        print('Cannot open ' + filename)
        raise
    except:
        print(filename + ' does not contain valid JSON.')
        raise
    create_pnx_from_json(json_input)
    print("Completed test")