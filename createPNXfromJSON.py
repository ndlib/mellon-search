#createPNXfromJSON.py 2/6/19 sm
""" This module will transform JSON input into PNX XML output for loading into Primo. """

import os, json
import xml.etree.ElementTree as ET
import pprint


def _create_display_section (jsonInput):
  display = ET.Element("display")
  ET.SubElement(display, 'lds02').text = jsonInput['recordId']
  ET.SubElement(display, 'title').text = jsonInput['title']
  ET.SubElement(display, 'creator').text = jsonInput['creator']
  ET.SubElement(display, 'creationdate').text = jsonInput['displayDate']
  ET.SubElement(display, 'format').text = jsonInput['media'] + ', ' + jsonInput['displayDimensions']
  ET.SubElement(display, 'lds09').text = jsonInput['classification']
  ET.SubElement(display, 'type').text = jsonInput['classification']
  ET.SubElement(display, 'lsd10').text = jsonInput['repository'].title() # Make sure this is mixed case
  return (display)

def _create_search_section (jsonInput):
  search = ET.Element("search")
  ET.SubElement(search, 'recordid').text = jsonInput['recordId']
  ET.SubElement(search, 'title').text = jsonInput['title']
  ET.SubElement(search, 'creator').text = jsonInput['creator']
  ET.SubElement(search, 'creationdate').text = jsonInput['creationDate']
  ET.SubElement(search, 'general').text = jsonInput['media'] + ', ' + jsonInput['displayDimensions']
  ET.SubElement(search, 'lsr09').text = jsonInput['classification']
  ET.SubElement(search, 'rsrctype').text = jsonInput['classification']
  ET.SubElement(search, 'scope').text = jsonInput['repository'].upper() # Make sure this is upper case
  return (search)


def _create_browse_section (jsonInput):
  browse = ET.Element("browse")
  ET.SubElement(browse, 'title').text = jsonInput['title']
  ET.SubElement(browse, 'author').text = jsonInput['creator']
  ET.SubElement(browse, 'institution').text = jsonInput['repository'].upper() # Make sure this is upper case
  return (browse)

def _create_sort_section (jsonInput):
  sort = ET.Element("sort")
  ET.SubElement(sort, 'title').text = jsonInput['title']
  ET.SubElement(sort, 'author').text = jsonInput['creator']
  ET.SubElement(sort, 'creationdate').text = jsonInput['creationDate']
  return (sort)

def _create_facet_section (jsonInput):
  facet = ET.Element("facet")
  ET.SubElement(facet, 'creatorcontrib').text = jsonInput['creator']
  ET.SubElement(facet, 'lfc09').text = jsonInput['classification']
  ET.SubElement(facet, 'rsrctype').text = jsonInput['classification']
  ET.SubElement(facet, 'library').text = jsonInput['repository'].upper()
  ET.SubElement(facet, 'creationdate').text = jsonInput['creationDate'] 
  return (facet)

def createPNXfromJSON (jsonInput):
  root = ET.Element("record")
  ET.SubElement(root, 'id').text = jsonInput['recordId']
  root.append(_create_display_section(jsonInput))
  root.append(_create_search_section(jsonInput))
  root.append(_create_browse_section(jsonInput))
  root.append(_create_sort_section(jsonInput))
  root.append(_create_facet_section(jsonInput))
  tree = ET.ElementTree(root)
  tree.write('example/' + jsonInput['recordId'] + '.xml')


# python3 -c 'from createPNXfromJSON import *; test("example/1976.057.json")'
def test(filename):
  try:
    with open(filename, 'r') as input_source:
        jsonInput = json.load(input_source)
    input_source.close()
  except IOError:
    print ('Cannot open ' + filename)
    raise
  except:
    print (filename + ' does not contain valid JSON.')
    raise
  createPNXfromJSON(jsonInput)
  print ("Completed test")
