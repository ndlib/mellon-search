# parseEmbArkXml.py 2/5/19 sm
""" This module will accept JSON field definitions and will use those definitions to retrieve
    data from EmbArk XML (also passed). """

from xml.etree.ElementTree import ElementTree
import getEmbarkXmlDefinitions
import readEmbArkFieldsJSONFile
import getValidDate

def _starts_with_ok(text, startsWith):
    ''' This returns True if text starts with the string (if any) in startsWith.    Else False '''
    if (startsWith == "") or text.startswith(startsWith):
        return True
    return False

def _does_not_start_with_ok(text, doesNotStartWith):
    ''' This returns True if text does not start with the string (if any) in startsWith.
        Else return False '''
    if (doesNotStartWith == "") or not text.startswith(doesNotStartWith):
        return True
    return False

class parseEmbArkXml():
    ''' Class does heavy lifting translating XML to JSON '''
    def __init__(self, fieldsDefinition):
        ''' Initialize fieldsDefinition only once for local use later '''
        self.result_json = {}
        self.fieldsDefinition = fieldsDefinition
        self.error = []
        self.id = ""
        self.output = {}


    def parseEmbArkRecord(self, embarkItemXML):
        ''' This translates information from EmbArk XML representing an
            individual museum item to JSON '''
        fieldsDefinition = self.fieldsDefinition
        self.output = {} # reinitialize output record at beginning of each EmbArk Item
        node = {}
        try:
            for field in fieldsDefinition:
                node = self._get_individual_field(field, embarkItemXML)
                self.output.update(node)
        except ValueError as e:
            self.output = {} #Blank out output if an error was encountered
            errorNode = {}
            errorNode["ValueError"] = e
            self.error.append(errorNode)
            raise
        return self.output


    def _get_individual_field(self, field, embarkItemXML):
        ''' This retrieves an individual field (possibly as an array)
            from EmbArk XML and saves to JSON '''
        jsonForThisField = {}
        try:
            # First, Extract definition of EmbArk XML from EmbArk Field Definitions JSON
            xpath = ""
            name = getEmbarkXmlDefinitions.getFieldName(field)
            required = getEmbarkXmlDefinitions.getFieldRequired(field)
            duplicatesAllowed = getEmbarkXmlDefinitions.getFieldDuplicatesAllowed(field)
            xpath = getEmbarkXmlDefinitions.getFieldXpath(field)
            doesNotStartWith = getEmbarkXmlDefinitions.getDoesNotStartWith(field)
            startsWith = getEmbarkXmlDefinitions.getStartsWith(field)
            validation = getEmbarkXmlDefinitions.getValidation(field)
            constant = getEmbarkXmlDefinitions.getConstant(field)
            if constant > "": # Use this for "repository", which doesn't exist in XML
                jsonForThisField[name] = constant
            elif name == 'exhibition': # exhibitions have highly unusual XML format
                jsonForThisField = self._get_exhibition_information(embarkItemXML, name, \
                    xpath, startsWith, doesNotStartWith)
            else:
                jsonForThisField = self._get_node(embarkItemXML, name, required, \
                    duplicatesAllowed, xpath, startsWith, doesNotStartWith, validation)
        except ValueError:
            raise
        return jsonForThisField

    def _get_node(self, embarkItemXML, name, required, duplicatesAllowed, xpath, \
            startsWith, doesNotStartWith, validation):
        ''' This retrieves an individual value (or array) from XML
            , optionally validates it, and saves to JSON '''
        node = {}
        self._validate_record_count(embarkItemXML, name, required, xpath)
        for item in embarkItemXML.findall(xpath):
            this_item = {}
            valueFound = ""
            if _starts_with_ok(item.text, startsWith) \
                and _does_not_start_with_ok(item.text, doesNotStartWith):
                valueFound = item.text
            if validation == 'validateYYYYMMDD' and valueFound > '':
                valueFound = getValidDate.getValidYYYYMMDDDate(valueFound)
            if name == 'recordId':
                self.id = valueFound
            if duplicatesAllowed:
                this_item["value"] = valueFound
                if name not in node:
                    node[name] = []
                node[name].append(this_item)
            else:
                this_item[name] = valueFound
                node = this_item
                break #if duplicates are not allowed, only accept first occurrence
        return node


    def _get_exhibition_information(self, embarkItemXML, name, xpath, \
            startsWith, doesNotStartWith):
        ''' This is to accommodate the special (crazy) data format which represents exhibitions '''
        exhibitionNode = {}
        exhibitionNode[name] = []
        exhibitionIterator = -1
        for item in embarkItemXML.findall(xpath):
            this_item = {}
            exhibitionIterator += 1
            if _starts_with_ok(item.text, startsWith) \
                and _does_not_start_with_ok(item.text, doesNotStartWith):
                this_item["name"] = item.text # Capture the name of the exhibit
                dateGroupIterator = -1
                for startDateGroup in embarkItemXML.findall('./group[@id=\'object_00001\']'):
                    #note:    first group record is StartDate
                    #second group record is EndDate (although both are called StartDate)
                    dateGroupIterator += 1
                    individualDateIterator = -1
                    if dateGroupIterator == 0: #StartDate
                        for startDate in startDateGroup.findall('./variable[@id=\'object_00001\']'):
                            individualDateIterator += 1
                            if individualDateIterator == exhibitionIterator:
                                this_item["startDate"] = startDate.text
                    else: #EndDate (Note: the XML calls End_Date by the name of Start_Date.
                        #End_Date is the second occurance of Start_Date.)
                        for endDate in startDateGroup.findall('./variable[@id=\'object_00001\']'):
                            individualDateIterator += 1
                            if individualDateIterator == exhibitionIterator:
                                this_item["endDate"] = endDate.text
                exhibitionNode[name].append(this_item)
        return exhibitionNode


    def _validate_record_count(self, embarkItemXML, name, required, xpath):
        ''' This ensures required fields exist '''
        errorText = ""
        error = {}
        elementCount = len(embarkItemXML.findall(xpath))
        if elementCount == 0 and required:
            errorText = 'Required field ' + name + ' is missing.    Unable to process record ' \
                + self.id
            error["ValueError"] = errorText
            raise ValueError(errorText)
        return error


# Tests
# python3 -c 'from parseEmbArkXml import *; test("example/objects 01_18_19.xml")'
def test(filename='example/objects 01_18_19.xml'):
    ''' Run all tests for this module '''
    testStartsWith()
    testReadAndParse(filename)

def testReadAndParse(filename):
    ''' test Read and Parse '''
    xmldoc = ElementTree(file=filename)
    filename = "./EmbArkXMLFields.json"
    embArkFieldDefinitions = readEmbArkFieldsJSONFile.readAndValidateEmbArkFieldDefinitionsFile(filename)
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
    ''' Test Starts With and Does Not Start With routines '''
    assert _starts_with_ok('abc123', 'abc')
    assert not _starts_with_ok('abc123', '123')
    assert _starts_with_ok('abc123', '')
    assert _does_not_start_with_ok('abc123', '')
    assert _does_not_start_with_ok('abc123', '123')
    assert not _does_not_start_with_ok('abc123', 'abc')
