#createPNXfromJSON.py 2/6/19 sm
""" This module will transform JSON input into PNX XML output for loading into Primo. """
import os, json
import xml.etree.ElementTree as ET
#from xml.etree.ElementTree import Element, ElementTree, tostring

#
#import xml.etree.cElementTree as ET

#root = ET.Element("root")
#doc = ET.SubElement(root, "doc")

#ET.SubElement(doc, "field1", name="blah").text = "some value1"
#ET.SubElement(doc, "field2", name="asdfasd").text = "some vlaue2"

#tree = ET.ElementTree(root)
#tree.write("filename.xml")

def _create_display_section (jsonInput):
  display = ET.Element("display")
  #ET.SubElement(display, 'lds02').text = jsonInput.recordid
  return (display)

def createPNXfromJSON (recordid, jsonInput):
  root = ET.Element("record")
  root.append(_create_display_section(jsonInput))
  #ET.SubElement(root, _create_display_section(jsonInput))
  tree = ET.ElementTree(root)
  tree.write(recordid + '.xml')
