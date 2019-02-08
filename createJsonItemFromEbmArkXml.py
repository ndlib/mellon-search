# createJsonItemFromEbmArkXml.py 2/5/19 sm
""" This is the first module in a series of modules to create JSON (and PNX) given EmbArk input. """

import os, json
import parseEmbArkXml
import readEmbArkFieldsJSONFile
import getEmbarkXmlDefinitions
from xml.etree.ElementTree import ElementTree, tostring
import createPNXfromJSON

# Get necessary information from JSON control file
# I had problems here trying to pass by reference, with values not being returned as expected
#def getembArkFieldDefinitionsFromFile(xpathOfEmbArkItem, fieldsDefinition):
#embArkFieldDefinitions = readEmbArkFieldsJSONFile.readAndValidateEmbArkFieldDefinitionsFile ()
#xpathOfEmbArkItem = getEmbarkXmlDefinitions.getItemXpath(embArkFieldDefinitions)
#fieldsDefinition = getEmbarkXmlDefinitions.getFieldsDefinition(embArkFieldDefinitions)


def writeJsonOutput (filename, jsonData):
  try:
    with open(filename, 'w') as outfile:
      json.dump(jsonData, outfile)
  except:
    print('Unable to write JSON data to output file named ' + filename)


def createJsonItemFromEbmArkXml(embArkXmlFilename):
  try:
    embArkXmlDoc = ElementTree(file=embArkXmlFilename)
  except:
    print('We were not able to open the file you specified. Please supply a valid XML filename and try again.')
  else:
    embArkFieldDefinitions = readEmbArkFieldsJSONFile.readAndValidateEmbArkFieldDefinitionsFile ()
    xpathOfEmbArkItem = getEmbarkXmlDefinitions.getItemXpath(embArkFieldDefinitions)
    fieldsDefinition = getEmbarkXmlDefinitions.getFieldsDefinition(embArkFieldDefinitions)
    #Loop through each EmbArk record, processing each individually
    for xmlOfEmbArkItem in embArkXmlDoc.findall(xpathOfEmbArkItem):
      jsonOfEmbArkItem = {}
      try:
        parseEmbArkXmlInstance = parseEmbArkXml.parseEmbArkXml(fieldsDefinition)
        jsonOfEmbArkItem = parseEmbArkXmlInstance.parseEmbArkRecord(xmlOfEmbArkItem)
      except:
        print('The XML representing a EmbArk Item didn\'t process as expected.  Please notify someone in IT.')
        #We will need to add some logging here
        raise
      else:
        writeJsonOutput('example/' + parseEmbArkXmlInstance.id + '.json', jsonOfEmbArkItem)
        createPNXfromJSON.createPNXfromJSON(jsonOfEmbArkItem)


#tests
# python3 -c 'from createJsonItemFromEbmArkXml import *; test()'
def test():
  testcreateJsonItemFromEbmArkXml()

def testcreateJsonItemFromEbmArkXml():
  createJsonItemFromEbmArkXml(embArkXmlFilename = 'example/objects 01_18_19.xml')

#def testReadingJsonFile():
#  xpathOfEmbArkItem = ""
#  fieldsDefinition = {}
#  filename = "./EmbArkXMLFields.json"
#  #getembArkFieldDefinitionsFromFile(filename, xpathOfEmbArkItem, fieldsDefinition)
#  print('here')
#  #print(filename)
#  print(xpathOfEmbArkItem)
#  print(fieldsDefinition)
