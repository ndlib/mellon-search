#getSniteXmlDefinitions.py 2/4/19 sm
""" This module pulls the definition of Snite XML fields from a passed JSON variable.
  Here is an example of a valid JSON variable:
  {
  	"itemPath": "./Section[@name='Body'][@id='section_07']",
  	"FieldsToExtract": [
  		{
  			"name": "recordid",
  			"required": true,
  			"duplicatesAllowed": false,
  			"xpath": "./variable[@id='object_00055']"
  		},
  		{
  			"name": "creator",
  			"required": false,
  			"duplicatesAllowed": false,
  			"xpath": "./variable[@id='object_00060']"
  		},
  		{
  			"name": "title",
  			"required": true,
  			"duplicatesAllowed": false,
  			"xpath": "./variable[@id='object_00056']"
  		},
  		{
  			"name": "bibliography",
  			"required": false,
  			"duplicatesAllowed": true,
  			"xpath": "./group[@id='object_00003']/variable[@id='object_00003']"
  		},
  		{
  			"name": "keyword",
  			"required": false,
  			"duplicatesAllowed": true,
  			"xpath": "./group[@id='object_00080']/variable[@id='object_00080']",
  			"doesNotStartWith": "AAT:"
  		},
  		{
  			"name": "facet",
  			"required": false,
  			"duplicatesAllowed": true,
  			"xpath": "./group[@id='object_00080']/variable[@id='object_00080']",
  			"startsWith": "AAT:"
  		}
  	]
  }
  ############################ Module documentation ends here ####################################
  """

import json
import getJsonValues


def getItemXpath(sniteFieldDefinitions):
  itemXPath = getJsonValues.getJsonValue(sniteFieldDefinitions, 'itemPath')
  return(itemXPath)

def getFieldsDefinition(sniteFieldDefinitions):
  fieldsDefinition = getJsonValues.getJsonValue(sniteFieldDefinitions, 'FieldsToExtract')
  return(fieldsDefinition)

def getFieldName(sniteFieldDefinition):
  fieldsDefinition = getJsonValues.getJsonValue(sniteFieldDefinition, 'name')
  return(fieldsDefinition)

def getFieldRequired(sniteFieldDefinition):
  fieldsDefinition = getJsonValues.getJsonValue(sniteFieldDefinition, 'required')
  return(fieldsDefinition)

def getFieldDuplicatesAllowed(sniteFieldDefinition):
  fieldsDefinition = getJsonValues.getJsonValue(sniteFieldDefinition, 'duplicatesAllowed')
  return(fieldsDefinition)

def getFieldXpath(sniteFieldDefinition):
  fieldsDefinition = getJsonValues.getJsonValue(sniteFieldDefinition, 'xpath')
  return(fieldsDefinition)

def getDoesNotStartWith(sniteFieldDefinition):
  fieldsDefinition = getJsonValues.getJsonValue(sniteFieldDefinition, 'doesNotStartWith', False)
  return(fieldsDefinition)

def getStartsWith(sniteFieldDefinition):
  fieldsDefinition = getJsonValues.getJsonValue(sniteFieldDefinition, 'startsWith', False)
  return(fieldsDefinition)


#tests
# python3 -c 'from getSniteXmlDefinitions import *; test()'

def test():
  try:
    testGetItemXpath()
    testGetFieldsDefinition()
    testGetFieldName()
    testGetFieldRequired()
    testGetFieldDuplicatesAllowed()
    testGetFieldXpath()
    testGetDoesNotStartWith()
    testGetStartsWith()
    print ('All tests ran successfully.')
  except:
    print('Houston, we have a problem.')
    raise

def testGetItemXpath():
  originalPath = '{"itemPath": "./Section[@name=\'Body\'][@id=\'section_07\']",	"FieldsToExtract": []}'
  sniteFieldDefinitions = json.loads(originalPath)
  itemXPath = getItemXpath(sniteFieldDefinitions)
  assert (itemXPath == sniteFieldDefinitions['itemPath'])

def testGetFieldsDefinition():
  sniteFieldDefinitions = json.loads('{"xitemPath": "./Section[@name=\'Body\'][@id=\'section_07\']",	"FieldsToExtract": [{"name": "recordid", "required": true, "duplicatesAllowed": false, "xpath": "./variable[@id=\'object_00055\']"}]}')
  fieldsDefinitions = getFieldsDefinition(sniteFieldDefinitions)
  assert (fieldsDefinitions == sniteFieldDefinitions['FieldsToExtract'])

def testGetFieldName():
  sniteFieldDefinition = json.loads('{"name": "recordid", "required": true, "duplicatesAllowed": false, "xpath": "./variable[@id=\'object_00055\']"}')
  name = getFieldName(sniteFieldDefinition)
  assert (name == sniteFieldDefinition['name'])

def testGetFieldRequired():
  sniteFieldDefinition = json.loads('{"name": "recordid", "required": true, "duplicatesAllowed": false, "xpath": "./variable[@id=\'object_00055\']"}')
  required = getFieldRequired(sniteFieldDefinition)
  assert (required == sniteFieldDefinition['required'])
  assert(required == True)

def testGetFieldDuplicatesAllowed():
  sniteFieldDefinition = json.loads('{"name": "recordid", "required": true, "duplicatesAllowed": false, "xpath": "./variable[@id=\'object_00055\']"}')
  duplicatesAllowed = getFieldDuplicatesAllowed(sniteFieldDefinition)
  assert (duplicatesAllowed == sniteFieldDefinition['duplicatesAllowed'])
  assert(duplicatesAllowed == False)

def testGetFieldXpath():
  sniteFieldDefinition = json.loads('{"name": "recordid", "required": true, "duplicatesAllowed": false, "xpath": "./variable[@id=\'object_00055\']"}')
  xpath = getFieldXpath(sniteFieldDefinition)
  assert (xpath == sniteFieldDefinition['xpath'])

def testGetDoesNotStartWith():
  sniteFieldDefinition = json.loads('{"name": "recordid", "required": true, "duplicatesAllowed": false, "xpath": "./variable[@id=\'object_00055\']","doesNotStartWith": "AAT:" }')
  doesNotStartWith = getDoesNotStartWith(sniteFieldDefinition)
  assert (doesNotStartWith == sniteFieldDefinition['doesNotStartWith'])
  assert (doesNotStartWith == "AAT:")

def testGetStartsWith():
  sniteFieldDefinition = json.loads('{"name": "recordid", "required": true, "duplicatesAllowed": false, "xpath": "./variable[@id=\'object_00055\']","startsWith": "AAT:" }')
  StartsWith = getStartsWith(sniteFieldDefinition)
  assert (StartsWith == sniteFieldDefinition['startsWith'])
  assert (StartsWith == "AAT:")
