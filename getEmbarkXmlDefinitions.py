#getEmbarkXmlDefinitions.py 2/4/19 sm
""" This module pulls the definition of EmbArk XML fields from a passed JSON variable.
  Here is an example of a valid JSON variable:
  {
  	"itemPath": "./Section[@name='Body'][@id='section_07']",
  	"FieldsToExtract": [
  		{
  			"name": "recordId",
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


def getItemXpath(embarkFieldDefinitions):
  itemXPath = getJsonValues.getJsonValue(embarkFieldDefinitions, 'itemPath')
  return(itemXPath)

def getFieldsDefinition(embarkFieldDefinitions):
  fieldsDefinition = getJsonValues.getJsonValue(embarkFieldDefinitions, 'FieldsToExtract')
  return(fieldsDefinition)

def getFieldName(embarkFieldDefinition):
  fieldsDefinition = getJsonValues.getJsonValue(embarkFieldDefinition, 'name')
  return(fieldsDefinition)

def getFieldRequired(embarkFieldDefinition):
  fieldsDefinition = getJsonValues.getJsonValue(embarkFieldDefinition, 'required')
  return(fieldsDefinition)

def getFieldDuplicatesAllowed(embarkFieldDefinition):
  fieldsDefinition = getJsonValues.getJsonValue(embarkFieldDefinition, 'duplicatesAllowed')
  return(fieldsDefinition)

def getFieldXpath(embarkFieldDefinition):
  fieldsDefinition = getJsonValues.getJsonValue(embarkFieldDefinition, 'xpath')
  return(fieldsDefinition)

def getDoesNotStartWith(embarkFieldDefinition):
  fieldsDefinition = getJsonValues.getJsonValue(embarkFieldDefinition, 'doesNotStartWith', False)
  return(fieldsDefinition)

def getStartsWith(embarkFieldDefinition):
  fieldsDefinition = getJsonValues.getJsonValue(embarkFieldDefinition, 'startsWith', False)
  return(fieldsDefinition)

def getValidation(embarkFieldDefinition):
  fieldsDefinition = getJsonValues.getJsonValue(embarkFieldDefinition, 'validation', False)
  return(fieldsDefinition)

def getConstant(embarkFieldDefinition):
  fieldsDefinition = getJsonValues.getJsonValue(embarkFieldDefinition, 'constant', False)
  return(fieldsDefinition)

#tests
# python3 -c 'from getEmbarkXmlDefinitions import *; test()'

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
    testGetValidation()
    testGetConstant()
    print ('All tests ran successfully.')
  except:
    print('Houston, we have a problem.')
    raise

def testGetItemXpath():
  originalPath = '{"itemPath": "./Section[@name=\'Body\'][@id=\'section_07\']",	"FieldsToExtract": []}'
  embarkFieldDefinitions = json.loads(originalPath)
  itemXPath = getItemXpath(embarkFieldDefinitions)
  assert (itemXPath == embarkFieldDefinitions['itemPath'])

def testGetFieldsDefinition():
  embarkFieldDefinitions = json.loads('{"xitemPath": "./Section[@name=\'Body\'][@id=\'section_07\']",	"FieldsToExtract": [{"name": "recordId", "required": true, "duplicatesAllowed": false, "xpath": "./variable[@id=\'object_00055\']"}]}')
  fieldsDefinitions = getFieldsDefinition(embarkFieldDefinitions)
  assert (fieldsDefinitions == embarkFieldDefinitions['FieldsToExtract'])

def testGetFieldName():
  embarkFieldDefinition = json.loads('{"name": "recordId", "required": true, "duplicatesAllowed": false, "xpath": "./variable[@id=\'object_00055\']"}')
  name = getFieldName(embarkFieldDefinition)
  assert (name == embarkFieldDefinition['name'])

def testGetFieldRequired():
  embarkFieldDefinition = json.loads('{"name": "recordId", "required": true, "duplicatesAllowed": false, "xpath": "./variable[@id=\'object_00055\']"}')
  required = getFieldRequired(embarkFieldDefinition)
  assert (required == embarkFieldDefinition['required'])
  assert(required == True)

def testGetFieldDuplicatesAllowed():
  embarkFieldDefinition = json.loads('{"name": "recordId", "required": true, "duplicatesAllowed": false, "xpath": "./variable[@id=\'object_00055\']"}')
  duplicatesAllowed = getFieldDuplicatesAllowed(embarkFieldDefinition)
  assert (duplicatesAllowed == embarkFieldDefinition['duplicatesAllowed'])
  assert(duplicatesAllowed == False)

def testGetFieldXpath():
  embarkFieldDefinition = json.loads('{"name": "recordId", "required": true, "duplicatesAllowed": false, "xpath": "./variable[@id=\'object_00055\']"}')
  xpath = getFieldXpath(embarkFieldDefinition)
  assert (xpath == embarkFieldDefinition['xpath'])

def testGetDoesNotStartWith():
  embarkFieldDefinition = json.loads('{"name": "recordId", "required": true, "duplicatesAllowed": false, "xpath": "./variable[@id=\'object_00055\']","doesNotStartWith": "AAT:" }')
  doesNotStartWith = getDoesNotStartWith(embarkFieldDefinition)
  assert (doesNotStartWith == embarkFieldDefinition['doesNotStartWith'])
  assert (doesNotStartWith == "AAT:")

def testGetStartsWith():
  embarkFieldDefinition = json.loads('{"name": "recordId", "required": true, "duplicatesAllowed": false, "xpath": "./variable[@id=\'object_00055\']","startsWith": "AAT:" }')
  StartsWith = getStartsWith(embarkFieldDefinition)
  assert (StartsWith == embarkFieldDefinition['startsWith'])
  assert (StartsWith == "AAT:")

def testGetValidation():
  embarkFieldDefinition = json.loads('{"name": "recordId", "required": true, "duplicatesAllowed": false, "xpath": "","constant": "Snite","validation":"validateYYYYMMDD" }')
  validation = getValidation(embarkFieldDefinition)
  print("validation = ", validation)
  assert (validation == embarkFieldDefinition['validation'])

def testGetConstant():
  embarkFieldDefinition = json.loads('{"name": "recordId", "required": true, "duplicatesAllowed": false, "xpath": "","constant": "Snite","validation":"validateYYYYMMDD" }')
  constant = getConstant(embarkFieldDefinition)
  print("constant = ", constant)
  assert (constant == embarkFieldDefinition['constant'])
