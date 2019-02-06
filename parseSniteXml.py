# parseSniteXml.py 2/5/19 sm
""" This module will accept JSON field definitions and will use those definitions to retrieve
  data from Snite XML (also passed). """

from xml.etree.ElementTree import fromstring, ElementTree, tostring
import getSniteXmlDefinitions
import readSniteFieldsJSONFile


def _starts_with_ok (text, startsWith):
  if (startsWith == "") or text.startswith(startsWith):
    return(True)
  else:
    return(False)

def _does_not_start_with_ok (text, doesNotStartWith):
  if (doesNotStartWith == "") or not text.startswith(doesNotStartWith):
    return(True)
  #if not text.startswith(doesNotStartWith):
  #  return(True)
  else:
    return(False)

class parseSniteXml():
  def __init__(self, fieldsDefinition):
    self.result_json = {}
    self.fieldsDefinition = fieldsDefinition
    self.error = []
    self.id = ""


  def parseSniteRecord ( self, sniteItemXML):
    fieldsDefinition = self.fieldsDefinition
    # Initialize output record at beginning of each Snite Item
    self.output={}
    node={}
    for field in fieldsDefinition:
      node = self._get_individual_field (field, sniteItemXML)
      #print(node)
      self.output.update(node)
    return (self.output)


  def _get_individual_field(self, field, sniteItemXML):
    jsonForThisField={}
    # Extract information from Snite Field Definitions JSON
    xpath = ""
    name = getSniteXmlDefinitions.getFieldName(field)
    required = getSniteXmlDefinitions.getFieldRequired(field)
    duplicatesAllowed = getSniteXmlDefinitions.getFieldDuplicatesAllowed(field)
    xpath = getSniteXmlDefinitions.getFieldXpath(field)
    doesNotStartWith = getSniteXmlDefinitions.getDoesNotStartWith(field)
    startsWith = getSniteXmlDefinitions.getStartsWith(field)
    if name == 'exhibition': #stupid special case for exhibitions
      jsonForThisField = self._get_exhibition_information(sniteItemXML, name, required, xpath, startsWith, doesNotStartWith)
    elif duplicatesAllowed :
      jsonForThisField = self._get_multiple (sniteItemXML, name, required, xpath, startsWith, doesNotStartWith)
    else :
      jsonForThisField = self._get_singlton (sniteItemXML, name, required, xpath, startsWith, doesNotStartWith)

    return (jsonForThisField)


  def _get_singlton (self, sniteItemXML, name, required, xpath, startsWith, doesNotStartWith):
    singleNode = {}
    valueFound=""
    try:
      valueFound = sniteItemXML.find(xpath).text
      if not required and valueFound is None:
        valueFound = ''
      singleNode[name] = valueFound
      if name == 'recordid':
        self.id = valueFound
    except:
      if required:
        print (name + ' is required, but ' + xpath + ' was not found')
        #print (tostring(sniteItemXML))
    #print (singleNode)
    return (singleNode)


  def _get_multiple (self, sniteItemXML, name, required, xpath, startsWith, doesNotStartWith):
    multipleNode = {}
    multipleNode[name] = []
    for item in sniteItemXML.findall(xpath):
      this_item = {}
      if _starts_with_ok(item.text, startsWith) and _does_not_start_with_ok (item.text, doesNotStartWith):
        this_item["value"] = item.text
        multipleNode[name].append(this_item)
    return (multipleNode)


  def _get_exhibition_information(self, sniteItemXML, name, required, xpath, startsWith, doesNotStartWith):
    #This is to accommodate the special (crazy) data format which represents exhibitions
    exhibitionNode = {}
    exhibitionNode[name] = []
    exhibitionIterator = -1
    for item in sniteItemXML.findall(xpath):
      this_item = {}
      exhibitionIterator += 1
      if _starts_with_ok(item.text, startsWith) and _does_not_start_with_ok (item.text, doesNotStartWith):
        this_item["name"] = item.text # Capture the name of the exhibit
        dateGroupIterator = -1
        for startDateGroup in sniteItemXML.findall('./group[@id=\'object_00001\']'):
          #note:  first group record is StartDate, second group record is EndDate (although both are called StartDate)
          dateGroupIterator += 1
          individualDateIterator = -1
          if dateGroupIterator == 0: #StartDate
            for startDate in startDateGroup.findall('./variable[@id=\'object_00001\']'):
              individualDateIterator += 1
              if individualDateIterator == exhibitionIterator:
                this_item["startDate"] = startDate.text
          else: #EndDate (Note: the XML calls End_Date by the name of Start_Date.  End_Date is the second occurance of Start_Date.)
            for endDate in startDateGroup.findall('./variable[@id=\'object_00001\']'):
              individualDateIterator += 1
              if individualDateIterator == exhibitionIterator:
                this_item["endDate"] = endDate.text
        exhibitionNode[name].append(this_item)
    return (exhibitionNode)


  def _validate_record_count (self, sniteItemXML, name, required, duplicatesAllowed, xpath):
    errorText = ""
    elementCount = len(sniteItemXML.findall(xpath))
    if elementCount == 0 and required :
      errorText = 'Required field ' + name + ' is missing.  Unable to process record.'
      raise ValueError(errorText)
    if elementCount > 1 and not duplicatesAllowed :
      errorText = 'By definition, ' + name + ' may only occur once in a record, but we found it ' + elementCount + ' times.  Unable to process record.'
      raise ValueError(errorText)
    assert ((elementCount == 1 and not duplicatesAllowed) or (duplicatesAllowed))
    return(errorText)

#Add tests
# python3 -c 'from parseSniteXml import *; test()'
def test():
  testStartsWith()
  testReadAndParse()

def testReadAndParse():
  xmldoc = ElementTree(file='objects 01_18_19.xml')
  filename = "./SniteXMLFields.json"
  sniteFieldDefinitions = readSniteFieldsJSONFile.readAndValidateSniteFieldDefinitionsFile (filename)
  itemXPath = getSniteXmlDefinitions.getItemXpath(sniteFieldDefinitions)
  fieldsDefinition = getSniteXmlDefinitions.getFieldsDefinition(sniteFieldDefinitions)
  for xmlOfSniteItem in xmldoc.findall(itemXPath):
  # xmlOfSniteItem contains EmbArk xml for one item.
    jsonOfSniteItem = {}
    section = parseSniteXml(fieldsDefinition)
    jsonOfSniteItem = section.parseSniteRecord(xmlOfSniteItem)
    #print(jsonOfSniteItem)
    print(section.id)

def testStartsWith():
  assert(_starts_with_ok ('abc123', 'abc') == True)
  assert(_starts_with_ok ('abc123', '123') == False)
  assert(_starts_with_ok ('abc123', '') == True)
  assert(_does_not_start_with_ok ('abc123','') == True)
  assert(_does_not_start_with_ok ('abc123','123') == True)
  assert(_does_not_start_with_ok ('abc123','abc') == False)

# eventually pass argument for filename
