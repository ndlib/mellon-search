# createSniteJsonItemFromXML.py 2/5/19 sm
import os, json
import parseSniteXml
import readSniteFieldsJSONFile
import getSniteXmlDefinitions
from xml.etree.ElementTree import ElementTree, tostring
import createPNXfromJSON

# Get necessary information from JSON control file
# I had problems here trying to pass by reference, with values not being returned as expected
#def getSniteFieldDefinitionsFromFile(xpathOfSniteItem, fieldsDefinition):
#sniteFieldDefinitions = readSniteFieldsJSONFile.readAndValidateSniteFieldDefinitionsFile ()
#xpathOfSniteItem = getSniteXmlDefinitions.getItemXpath(sniteFieldDefinitions)
#fieldsDefinition = getSniteXmlDefinitions.getFieldsDefinition(sniteFieldDefinitions)


def writeJsonOutput (filename, jsonData):
  try:
    with open(filename, 'w') as outfile:
      json.dump(jsonData, outfile)
  except:
    print('Unable to write JSON data to output file named ' + filename)


def createSniteJsonItemFromXML(sniteXMLFilename):
  try:
    sniteXmlDoc = ElementTree(file=sniteXMLFilename)
  except:
    print('We were not able to open the file you specified. Please supply a valid XML filename and try again.')
  else:
    sniteFieldDefinitions = readSniteFieldsJSONFile.readAndValidateSniteFieldDefinitionsFile ()
    xpathOfSniteItem = getSniteXmlDefinitions.getItemXpath(sniteFieldDefinitions)
    fieldsDefinition = getSniteXmlDefinitions.getFieldsDefinition(sniteFieldDefinitions)
    #Loop through each EmbArk record, processing each individually
    for xmlOfSniteItem in sniteXmlDoc.findall(xpathOfSniteItem):
      jsonOfSniteItem = {}
      try:
        parseSniteXmlInstance = parseSniteXml.parseSniteXml(fieldsDefinition)
        jsonOfSniteItem = parseSniteXmlInstance.parseSniteRecord(xmlOfSniteItem)
      except:
        print('The XML representing a Snite Item didn\'t process as expected.  Please notify someone in IT.')
        #We will need to add some logging here
        raise
      else:
        writeJsonOutput(parseSniteXmlInstance.id + '.json', jsonOfSniteItem)
        createPNXfromJSON.createPNXfromJSON(parseSniteXmlInstance.id, jsonOfSniteItem)


#tests
# python3 -c 'from createSniteJsonItemFromXML import *; test()'
def test():
  testCreateSniteJsonItemFromXML()

def testCreateSniteJsonItemFromXML():
  createSniteJsonItemFromXML(sniteXMLFilename = 'objects 01_18_19.xml')

#def testReadingJsonFile():
#  xpathOfSniteItem = ""
#  fieldsDefinition = {}
#  filename = "./SniteXMLFields.json"
#  #getSniteFieldDefinitionsFromFile(filename, xpathOfSniteItem, fieldsDefinition)
#  print('here')
#  #print(filename)
#  print(xpathOfSniteItem)
#  print(fieldsDefinition)
