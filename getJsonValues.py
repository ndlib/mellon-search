#getJsonValues.py 2/1/19 sm
""" This module deals with extracting a JSON value from a JSON variable.
  If a value is required, it must exist and must not be blank.
  If an error is encountered, we raise a ValueError."""

import json
import pprint

def getJsonValue(jsonVariable, jsonKey, fieldIsRequired = True):
  if jsonVariable is None:
    print ("Missing in Action")
    return
  jsonValue=""
  #pprint.pprint(jsonVariable)
  try:
    jsonValue = jsonVariable[jsonKey]
    if jsonValue is None:
      raise ValueError(jsonKey + ' cannot be found.  JSON Control file is invalid.')
    if jsonValue == "" and fieldIsRequired:
      raise ValueError(jsonKey + ' contained a blank value where it should have contained a required value.   Offending portion of file includes:  ' + json.dumps(jsonVariable))
  except:
    if fieldIsRequired:
      raise ValueError('Required Key Missing: "' + jsonKey + '" does not exist in JSON Control File.  Offending portion of file includes:  ' + json.dumps(jsonVariable))
  return(jsonValue)


#testing
# python3 -c 'from getJsonValues import *; test()'

def test():
  try:
    testGetRequiredValue()
    testMissingRequiredValue()
    testBlankRequiredValue()
    testMalFormedJson()
    testGetOptionalValue()
    testBlankOptionalValue()
    testMissingOptionalValue()
    print ('All tests ran successfully.')
  except:
    print('Houston, we have a problem.')
    raise

def testGetRequiredValue():
  originalPath = '{"itemPath": "./Section[@name=\'Body\'][@id=\'section_07\']",	"FieldsToExtract": []}'
  sniteFieldDefinitions = json.loads(originalPath)
  itemXPath = getJsonValue(sniteFieldDefinitions, 'itemPath')
  assert (itemXPath == sniteFieldDefinitions['itemPath'])

def testMissingRequiredValue():
  sniteFieldDefinitions = json.loads('{"xitemPath": "./Section[@name=\'Body\'][@id=\'section_07\']",	"FieldsToExtract": []}')
  valueErrorEncountered = False
  #itemXPath = getJsonValue(sniteFieldDefinitions, 'itemPath')
  #print(itemXPath)
  try:
    itemXPath = getJsonValue(sniteFieldDefinitions, 'itemPath')
  except ValueError as e:
    valueErrorEncountered = True
  if not valueErrorEncountered:
    print ('Expected error but didn\'t throw one.')

def testBlankRequiredValue():
  valueErrorEncountered = False
  sniteFieldDefinitions = json.loads('{"itemPath": "",	"FieldsToExtract": []}')
  try:
    itemXPath = getJsonValue(sniteFieldDefinitions, 'itemPath')
  except ValueError as e:
    valueErrorEncountered = True
  if not valueErrorEncountered:
    print ('Expected error but didn\'t throw one.')

def testMalFormedJson():
  jsonDecodeErrorEncountered = False
  try:
    sniteFieldDefinitions = json.loads('{x"itemPath": "",	"FieldsToExtract": []}')
  except Exception as e:
    jsonDecodeErrorEncountered = True
  if not jsonDecodeErrorEncountered:
    print ('Expected error but didn\'t throw one.')

def testGetOptionalValue():
  sniteFieldDefinitions = json.loads('{"name": "facet","required": false,"duplicatesAllowed": true,"xpath": "./group[@id=\'object_00080\']/variable[@id=\'object_00080\']","startsWith": "AAT:"}')
  startsWith = getJsonValue(sniteFieldDefinitions, 'startsWith', False)
  assert(startsWith == "AAT:")

def testBlankOptionalValue():
  sniteFieldDefinitions = json.loads('{"name": "facet","required": false,"duplicatesAllowed": true,"xpath": "./group[@id=\'object_00080\']/variable[@id=\'object_00080\']","startsWith": ""}')
  startsWith = getJsonValue(sniteFieldDefinitions, 'startsWith', False)
  assert(startsWith == "")

def testMissingOptionalValue():
  sniteFieldDefinitions = json.loads('{"name": "facet","required": false,"duplicatesAllowed": true,"xpath": "./group[@id=\'object_00080\']/variable[@id=\'object_00080\']"}')
  startsWith = getJsonValue(sniteFieldDefinitions, 'startsWith', False)
  assert(startsWith == "")
