# readEmbArkFieldsJSONFile.py 2/4/19 sm
""" This module will read and validate the JSON that defines the EmbArk XML. """

import json
import getEmbarkXmlDefinitions
import pprint

def _read_embark_field_definitions_file (filename):
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


def _validate_embark_field_definitions_file (embarkFieldDefinitions) :
  itemXPath = getEmbarkXmlDefinitions.getItemXpath(embarkFieldDefinitions)
  fieldsDefinition = getEmbarkXmlDefinitions.getFieldsDefinition(embarkFieldDefinitions)
  for field in fieldsDefinition:
    name = getEmbarkXmlDefinitions.getFieldName(field)
    required = getEmbarkXmlDefinitions.getFieldRequired(field)
    duplicatesAllowed = getEmbarkXmlDefinitions.getFieldDuplicatesAllowed(field)
    xpath = getEmbarkXmlDefinitions.getFieldXpath(field)
    doesNotStartWith = getEmbarkXmlDefinitions.getDoesNotStartWith(field)
    startsWith = getEmbarkXmlDefinitions.getStartsWith(field)
    validation = getEmbarkXmlDefinitions.getValidation(field)
    constant = getEmbarkXmlDefinitions.getConstant(field)
    return


def readAndValidateEmbArkFieldDefinitionsFile (filename = "./EmbArkXMLFields.json"):
  embarkFieldDefinitions=""
  try:
    embarkFieldDefinitions = _read_embark_field_definitions_file (filename)
    _validate_embark_field_definitions_file (embarkFieldDefinitions)
  except:
    raise
  return(embarkFieldDefinitions)

#tests
# python3 -c 'from readEmbArkFieldsJSONFile import *; test()'
def test():
  try:
    testreadAndValidateEmbArkFieldDefinitionsFile("./EmbArkXMLFields.json")
    try:
      testMissingEmbArkFielDefinitionsFile("./EmbArkXMLFields.jsonx")
    except FileNotFoundError:
      pass
    print("All tests ran successfully")
  except:
    Print("Tests failed.")
    raise

# python3 -c 'from readEmbArkFieldsJSONFile import *; testReadembarkFieldDefinitionsFile("./EmbArkXMLFields.json")'
def testreadAndValidateEmbArkFieldDefinitionsFile(filename):
  try:
    embarkFieldDefinitions = readAndValidateEmbArkFieldDefinitionsFile (filename)
  except FileNotFoundError:
    print ('File Not Found')

def testMissingEmbArkFielDefinitionsFile(filename):
  try:
    embarkFieldDefinitions = readAndValidateEmbArkFieldDefinitionsFile (filename)
  except FileNotFoundError:
    print ('File Not Found')
