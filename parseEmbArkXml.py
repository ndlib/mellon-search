# parseEmbArkXml.py 2/5/19 sm
""" This module will accept JSON field definitions and will use those definitions to retrieve
  data from EmbArk XML (also passed). """

from xml.etree.ElementTree import fromstring, ElementTree, tostring
import getEmbarkXmlDefinitions
import readEmbArkFieldsJSONFile
import getValidDate

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

class parseEmbArkXml():
  def __init__(self, fieldsDefinition):
    self.result_json = {}
    self.fieldsDefinition = fieldsDefinition
    self.error = []
    self.id = ""


  def parseEmbArkRecord ( self, embarkItemXML):
    fieldsDefinition = self.fieldsDefinition
    # Initialize output record at beginning of each EmbArk Item
    self.output={}
    #self.output['repository']="Snite" #Save the fact this record represents an item in the Snite Museum
    node={}
    for field in fieldsDefinition:
      node = self._get_individual_field (field, embarkItemXML)
      #print(node)
      self.output.update(node)
    return (self.output)


  def _get_individual_field(self, field, embarkItemXML):
    jsonForThisField={}
    # Extract information from EmbArk Field Definitions JSON
    xpath = ""
    name = getEmbarkXmlDefinitions.getFieldName(field)
    required = getEmbarkXmlDefinitions.getFieldRequired(field)
    duplicatesAllowed = getEmbarkXmlDefinitions.getFieldDuplicatesAllowed(field)
    xpath = getEmbarkXmlDefinitions.getFieldXpath(field)
    doesNotStartWith = getEmbarkXmlDefinitions.getDoesNotStartWith(field)
    startsWith = getEmbarkXmlDefinitions.getStartsWith(field)
    validation = getEmbarkXmlDefinitions.getValidation(field)
    constant = getEmbarkXmlDefinitions.getConstant(field)
    if constant > "":
      jsonForThisField[name]= constant
      #print (jsonForThisField)
    elif name == 'exhibition': #stupid special case for exhibitions
      jsonForThisField = self._get_exhibition_information(embarkItemXML, name, required, xpath, startsWith, doesNotStartWith, validation)
    elif duplicatesAllowed :
      jsonForThisField = self._get_multiple (embarkItemXML, name, required, xpath, startsWith, doesNotStartWith, validation)
    else :
      jsonForThisField = self._get_singlton (embarkItemXML, name, required, xpath, startsWith, doesNotStartWith, validation)

    return (jsonForThisField)


  def _get_singlton (self, embarkItemXML, name, required, xpath, startsWith, doesNotStartWith, validation):
    singleNode = {}
    valueFound=""
    try:
      valueFound = embarkItemXML.find(xpath).text
      if not required and valueFound is None:
        valueFound = ''
      if validation == 'validateYYYYMMDD' and valueFound > '':
        valueFound = getValidDate.getValidYYYYMMDDDate(valueFound)
      singleNode[name] = valueFound
      if name == 'recordId':
        self.id = valueFound
    except:
      if required:
        print (name + ' is required, but ' + xpath + ' was not found')
        #print (tostring(embarkItemXML))
    #print (singleNode)
    return (singleNode)


  def _get_multiple (self, embarkItemXML, name, required, xpath, startsWith, doesNotStartWith, validation):
    multipleNode = {}
    multipleNode[name] = []
    for item in embarkItemXML.findall(xpath):
      this_item = {}
      if _starts_with_ok(item.text, startsWith) and _does_not_start_with_ok (item.text, doesNotStartWith):
        this_item["value"] = item.text
        multipleNode[name].append(this_item)
    return (multipleNode)


  def _get_exhibition_information(self, embarkItemXML, name, required, xpath, startsWith, doesNotStartWith, validation):
    #This is to accommodate the special (crazy) data format which represents exhibitions
    exhibitionNode = {}
    exhibitionNode[name] = []
    exhibitionIterator = -1
    for item in embarkItemXML.findall(xpath):
      this_item = {}
      exhibitionIterator += 1
      if _starts_with_ok(item.text, startsWith) and _does_not_start_with_ok (item.text, doesNotStartWith):
        this_item["name"] = item.text # Capture the name of the exhibit
        dateGroupIterator = -1
        for startDateGroup in embarkItemXML.findall('./group[@id=\'object_00001\']'):
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


  def _validate_record_count (self, embarkItemXML, name, required, duplicatesAllowed, xpath):
    errorText = ""
    elementCount = len(embarkItemXML.findall(xpath))
    if elementCount == 0 and required :
      errorText = 'Required field ' + name + ' is missing.  Unable to process record.'
      raise ValueError(errorText)
    if elementCount > 1 and not duplicatesAllowed :
      errorText = 'By definition, ' + name + ' may only occur once in a record, but we found it ' + elementCount + ' times.  Unable to process record.'
      raise ValueError(errorText)
    assert ((elementCount == 1 and not duplicatesAllowed) or (duplicatesAllowed))
    return(errorText)

#Add tests
# python3 -c 'from parseEmbArkXml import *; test()'
def test():
  testStartsWith()
  testReadAndParse()

def testReadAndParse():
  xmldoc = ElementTree(file='example/objects 01_18_19.xml')
  filename = "./EmbArkXMLFields.json"
  embArkFieldDefinitions = readEmbArkFieldsJSONFile.readAndValidateEmbArkFieldDefinitionsFile (filename)
  itemXPath = getEmbarkXmlDefinitions.getItemXpath(embArkFieldDefinitions)
  fieldsDefinition = getEmbarkXmlDefinitions.getFieldsDefinition(embArkFieldDefinitions)
  for xmlOfEmbArkItem in xmldoc.findall(itemXPath):
  # xmlOfEmbArkItem contains EmbArk xml for one item.
    jsonOfEmbArkItem = {}
    section = parseEmbArkXml(fieldsDefinition)
    jsonOfEmbArkItem = section.parseEmbArkRecord(xmlOfEmbArkItem)
    #print(jsonOfEmbArkItem)
    print(section.id)

def testStartsWith():
  assert(_starts_with_ok ('abc123', 'abc') == True)
  assert(_starts_with_ok ('abc123', '123') == False)
  assert(_starts_with_ok ('abc123', '') == True)
  assert(_does_not_start_with_ok ('abc123','') == True)
  assert(_does_not_start_with_ok ('abc123','123') == True)
  assert(_does_not_start_with_ok ('abc123','abc') == False)

# eventually pass argument for filename
