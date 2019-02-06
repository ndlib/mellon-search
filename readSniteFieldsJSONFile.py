# readSniteFieldsJSONFile.py 2/4/19 sm
""" This module will read and validate the JSON that defines the Snite XML. """

import json
import getSniteXmlDefinitions
import pprint

def _read_snite_field_definitions_file (filename):
  try:
    with open(filename, 'r') as input_source:
        data = json.load(input_source)
    input_source.close()
  except IOError:
    print ('Cannot open ' + filename)
    raise
  except:
    print (filename + ' does not contain valid JSON.')
    raise
  return(data)


def _validate_snite_field_definitions_file (sniteFieldDefinitions) :
  itemXPath = getSniteXmlDefinitions.getItemXpath(sniteFieldDefinitions)
  #print (itemXPath)
  fieldsDefinition = getSniteXmlDefinitions.getFieldsDefinition(sniteFieldDefinitions)
  #pprint.pprint(fieldsDefinition)
  for field in fieldsDefinition:
    name = getSniteXmlDefinitions.getFieldName(field)
    required = getSniteXmlDefinitions.getFieldRequired(field)
    duplicatesAllowed = getSniteXmlDefinitions.getFieldDuplicatesAllowed(field)
    xpath = getSniteXmlDefinitions.getFieldXpath(field)
    doesNotStartWith = getSniteXmlDefinitions.getDoesNotStartWith(field)
    startsWith = getSniteXmlDefinitions.getStartsWith(field)

    return


def readAndValidateSniteFieldDefinitionsFile (filename = "./SniteXMLFields.json"):
  sniteFieldDefinitions=""
  try:
    sniteFieldDefinitions = _read_snite_field_definitions_file (filename)
    #print (sniteFieldDefinitions)
    _validate_snite_field_definitions_file (sniteFieldDefinitions)
  except:
    print ('Error occurred during Read but before validate. ')
    raise
  return(sniteFieldDefinitions)

#tests
# python3 -c 'from readSniteFieldsJSONFile import *; test()'
def test():
  testreadAndValidateSniteFieldDefinitionsFile("./SniteXMLFields.json")
  testMissingSniteFielDefinitionsFile("./SniteXMLFields.jsonx")

# python3 -c 'from readSniteFieldsJSONFile import *; testReadSniteFieldDefinitionsFile("./SniteXMLFields.json")'
def testreadAndValidateSniteFieldDefinitionsFile(filename):
  try:
    sniteFieldDefinitions = readAndValidateSniteFieldDefinitionsFile (filename)
  except FileNotFoundError:
    print ('File Not Found')

def testMissingSniteFielDefinitionsFile(filename):
  try:
    sniteFieldDefinitions = readAndValidateSniteFieldDefinitionsFile (filename)
  except FileNotFoundError:
    print ('File Not Found')
