#test_get_individual_field_from_embark_xml.py 2/18/19 sm
""" test get_individual_field_from_embark_xml.py """

import json
import unittest
from xml.etree.ElementTree import ElementTree, fromstring

# add parent directory to path
import os
import inspect
import sys
CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PARENTDIR = os.path.dirname(CURRENTDIR)
sys.path.insert(0, PARENTDIR)

from get_individual_field_from_embark_xml import GetEmbarkField, _starts_with_ok, _does_not_start_with_ok

class Test(unittest.TestCase):
    """ Class for test fixtures """

    def get_xml_doc(self):
        """ Need to load xml internally to control contents for testing """
        xmldoc_element = fromstring('<?xml version="1.0" encoding="utf-8" standalone="yes"?>\
      <Section name="Body" id="section_07">\
        <variable name="[Object]Display Title" id="object_00056">ABSOLUTION UNDER FIRE</variable>\
        <variable name="[Object]Display Artist" id="object_00060">Paul Wood</variable>\
        <variable id="Field_36"/>\
        <variable name="[Object]Creation Date" id="object_00062">1891 - 1891</variable>\
        <variable name="[Object]Date Display">1891</variable>\
        <variable name="[Object]Media and Support" id="object_00061">oil on canvas</variable>\
        <group name="[Dimensions]Extent" id="object_00013">\
          <variable name="[Dimensions]Extent" id="object_00013"/>\
          <variable name="[Dimensions]Extent" id="object_00013"/>\
        </group>\
        <variable name="[Object]Display Dimensions" id="object_00063">76 1/2 x 102 x 3 1/4 in. (194.31 x 259.08 x 8.26 cm)</variable>\
        <variable name="[Object]Accession Number" id="object_00055">1976.057</variable>\
        <group name="atTemp2" id="object_00003">\
          <variable name="atTemp2" id="object_00003">Bilby, Joseph G., Remember Fontenoy!, Longstreet House, Highstown, NJ, 1995, 86</variable>\
          <variable name="atTemp2" id="object_00003">Burger, John, Columbia, Pelowski, Alton J., Knights of Columbus, New Haven, CT, May 2015, 16-18</variable>\
          <variable name="atTemp2" id="object_00003">Callaghan, James, Civil War, Miller, William J., Christopher M. Curran, Berryville, VA, August 1997, 26-33</variable>\
          <variable name="atTemp2" id="object_00003">Carey, John E., The Civil War, The Washington Times, Saturday, Sept. 14, 1996, B3-not illustrated</variable>\
          <variable name="atTemp2" id="object_00003">Clark, Champ, The Civil War, Time Life Books, 1985, 100-101</variable>\
          <variable name="atTemp2" id="object_00003">Corby, William, Memoirs of Chaplain Life, Kohl, Lawrence Frederick, Fordham University Press, Chicago, 1893, 385-387</variable>\
          <variable name="atTemp2" id="object_00003">Faherty, S. J., William Barnaby, Catholic Chaplains in Blue and Gray, Jesuit Missouri Province Archives, St. Louis, MO, 1995, unknown</variable>\
          <variable name="atTemp2" id="object_00003">Faherty, S. J., William Barnaby, U. S Catholic Historian, Jesuit Missouri Province Archives, St. Louis, MO, Summer 1995, unknown</variable>\
          <variable name="atTemp2" id="object_00003">Mach, Andrew, American Catholic Studies, Van Allen, Rodger, American Catholic Studies</variable>\
          <variable name="atTemp2" id="object_00003">Morris, Claire, 69th New York &amp; It\'s Place in The Irish Brigade, 2006, 25</variable>\
          <variable name="atTemp2" id="object_00003">O\'Beirne, Kevin, Military Heritage, Octtober 1999, 40-41</variable>\
          <variable name="atTemp2" id="object_00003">Rable, George C., Civil War Times, Civil War Times, North Carolina, December 2003, 56-59, 86-88</variable>\
          <variable name="atTemp2" id="object_00003">Shattuck, Gardiner H., The Sword of the Lord: , Bergen, Doris, University of Notre Dame Press, Notre Dame, IN, 2004, 105-123, illustrated on pg. 113</variable>\
          <variable name="atTemp2" id="object_00003">Symonds, Craig L., American Heritage History of the Battle of Gettysburg, HarperCollins , North America, 2001, unknown</variable>\
        </group>\
        <group name="[Exhibitions]Exhibition_Name" id="object_00002">\
          <variable name="[Exhibitions]Exhibition_Name" id="object_00002">Picturing History</variable>\
        </group>\
        <group name="[Exhibitions]Start_Date" id="object_00001">\
          <variable name="[Exhibitions]Start_Date" id="object_00001">09/01/94</variable>\
        </group>\
        <group name="[Exhibitions]Start_Date" id="object_00001">\
          <variable name="[Exhibitions]Start_Date" id="object_00001">12/01/94</variable>\
        </group>\
        <group name="KeyWord Path" id="object_00080">\
          <variable name="KeyWord Path" id="object_00080">confederate</variable>\
          <variable name="KeyWord Path" id="object_00080">battle</variable>\
          <variable name="KeyWord Path" id="object_00080">civil war</variable>\
          <variable name="KeyWord Path" id="object_00080">priest</variable>\
          <variable name="KeyWord Path" id="object_00080">battlefield</variable>\
          <variable name="KeyWord Path" id="object_00080">irish</variable>\
          <variable name="KeyWord Path" id="object_00080">soldier</variable>\
          <variable name="KeyWord Path" id="object_00080">conflict</variable>\
          <variable name="KeyWord Path" id="object_00080">AAT:&lt;Associated Concepts Facet&gt;:&lt;Associated Concepts&gt;:&lt;religions and religious concepts&gt;:&lt;religious concepts&gt;:&lt;doctrinal concepts&gt;:absolution</variable>\
          <variable name="KeyWord Path" id="object_00080">AAT:&lt;Physical Attributes Facet&gt;:&lt;Attributes and Properties&gt;:&lt;attributes and properties&gt;:&lt;attributes and properties by specific type&gt;:&lt;positional attributes&gt;:compass points:north</variable>\
          <variable name="KeyWord Path" id="object_00080">AAT:&lt;Styles and Periods Facet&gt;:&lt;Styles and Periods&gt;:&lt;styles and periods by region&gt;:&lt;The Americas&gt;:&lt;American regions&gt;:South American</variable>\
          <variable name="KeyWord Path" id="object_00080">AAT:&lt;Activities Facet&gt;:&lt;Events&gt;:events:armed conflicts</variable>\
          <variable name="KeyWord Path" id="object_00080">AAT:&lt;Activities Facet&gt;:&lt;Events&gt;:events:armed conflicts:wars</variable>\
          <variable name="KeyWord Path" id="object_00080">AAT:&lt;Activities Facet&gt;:&lt;Events&gt;:events:armed conflicts:wars:civil wars</variable>\
          <variable name="KeyWord Path" id="object_00080">AAT:&lt;Objects Facet&gt;:Visual and Verbal Communication:&lt;Visual Works (Hierarchy Name)&gt;:&lt;visual works (Guide Term)&gt;:&lt;visual works by form&gt;:&lt;visual works by form: image form&gt;:depictions</variable>\
          <variable name="KeyWord Path" id="object_00080">AAT:&lt;Objects Facet&gt;:Visual and Verbal Communication:&lt;Information Forms (Hierarchy Name)&gt;:&lt;information forms (Guide Term)&gt;:&lt;document genres&gt;:&lt;document genres by form&gt;:&lt;document genres for literary works&gt;:poems:&lt;poems by function&gt;:epics</variable>\
        </group>\
      </Section>\
')
        xmldoc = ElementTree(xmldoc_element)
        return xmldoc


    def test_read_record_id(self):
        """ test Read and Parse """
        xml_of_embark_item = self.get_xml_doc()
        json_of_embark_field = {}
        field_definition = json.loads('{"name": "recordId","required": true,"duplicatesAllowed": false,"xpath": "./variable[@id=\'object_00055\']"}')
        field = GetEmbarkField(field_definition)
        json_of_embark_field = field.get_json_representation_of_field(xml_of_embark_item)
        self.assertTrue(json.loads('{"recordId": "1976.057"}') == json_of_embark_field)

    def test_read_constant(self):
        """ test Read and Parse """
        xml_of_embark_item = self.get_xml_doc()
        json_of_embark_field = {}
        field_definition = json.loads('{"name": "repository","required": false,"duplicatesAllowed": false,"xpath": "required, but not used here.","constant": "Snite"}')
        field = GetEmbarkField(field_definition)
        json_of_embark_field = field.get_json_representation_of_field(xml_of_embark_item)
        self.assertTrue(json.loads('{"repository": "Snite"}') == json_of_embark_field)

    def test_read_creator(self):
        """ test Read and Parse """
        xml_of_embark_item = self.get_xml_doc()
        json_of_embark_field = {}
        field_definition = json.loads('{"name": "creator","required": false,"duplicatesAllowed": false,"xpath": "./variable[@id=\'object_00060\']"}')
        field = GetEmbarkField(field_definition)
        json_of_embark_field = field.get_json_representation_of_field(xml_of_embark_item)
        self.assertTrue(json.loads('{"creator": "Paul Wood"}') == json_of_embark_field)

    def test_read_creation_date(self):
        """ test Read and Parse """
        xml_of_embark_item = self.get_xml_doc()
        json_of_embark_field = {}
        field_definition = json.loads('{"name": "creationDate","required": false,"duplicatesAllowed": false,"xpath": "./variable[@id=\'object_00062\']","validation": "validateYYYYMMDD"}')
        field = GetEmbarkField(field_definition)
        json_of_embark_field = field.get_json_representation_of_field(xml_of_embark_item)
        self.assertTrue(json.loads('{"creationDate": "18910101"}') == json_of_embark_field)

    def test_read_exhibition(self):
        """ test Read and Parse """
        xml_of_embark_item = self.get_xml_doc()
        json_of_embark_field = {}
        field_definition = json.loads('{"name": "exhibition","required": false,"duplicatesAllowed": true,"xpath": "./group[@id=\'object_00002\']/variable[@id=\'object_00002\']"}')
        field = GetEmbarkField(field_definition)
        json_of_embark_field = field.get_json_representation_of_field(xml_of_embark_item)
        self.assertTrue(json.loads('{"exhibition": [{"name": "Picturing History", "startDate": "09/01/94", "endDate": "12/01/94"}]}') == json_of_embark_field)

    def test_read_keyword(self):
        """ test keyword """
        xml_of_embark_item = self.get_xml_doc()
        json_of_embark_field = {}
        field_definition = json.loads('{"name": "keyword","required": false,"duplicatesAllowed": true,"xpath": "./group[@id=\'object_00080\']/variable[@id=\'object_00080\']"}')
        field = GetEmbarkField(field_definition)
        json_of_embark_field = field.get_json_representation_of_field(xml_of_embark_item)
        for keyword in json_of_embark_field['keyword']:
            value = keyword['value']
            self.assertTrue(value == 'confederate')
            break

    def test_read_default(self):
        """ test default """
        xml_of_embark_item = self.get_xml_doc()
        json_of_embark_field = {}
        field_definition = json.loads('{"name": "classification","required": false,"duplicatesAllowed": false,"xpath": "./variable[@name=\'[Object]Class 2\']","default": "painting"}')
        field = GetEmbarkField(field_definition)
        json_of_embark_field = field.get_json_representation_of_field(xml_of_embark_item)
        self.assertTrue(json.loads('{"classification": "painting"}') == json_of_embark_field)

    def test_try_to_throw_required_value_missing_error(self):
        """ test default """
        xml_of_embark_item = self.get_xml_doc()
        json_of_embark_field = {}
        field_definition = json.loads('{"name": "classification","required": true,"duplicatesAllowed": false,"xpath": "./variable[@name=\'[Object]Class 2\']"}')
        field = GetEmbarkField(field_definition)
        self.assertRaises(ValueError, field.get_json_representation_of_field, xml_of_embark_item)
        #json_of_embark_field = field.get_json_representation_of_field(xml_of_embark_item)
        #self.assertTrue(json.loads('{"classification": "painting"}') == json_of_embark_field)
        #now switch field definition to include default, and return "painting"
        field_definition = json.loads('{"name": "classification","required": true,"duplicatesAllowed": false,"xpath": "./variable[@name=\'[Object]Class 2\']","default": "painting"}')
        field.load_json_field_definition(field_definition)
        json_of_embark_field = field.get_json_representation_of_field(xml_of_embark_item)
        self.assertTrue(json.loads('{"classification": "painting"}') == json_of_embark_field)

    def test_starts_with(self):
        """ Test Starts With and Does Not Start With routines """
        self.assertTrue(_starts_with_ok('abc123', 'abc'))
        self.assertTrue(not _starts_with_ok('abc123', '123'))
        self.assertTrue(_starts_with_ok('abc123', ''))
        self.assertTrue(_does_not_start_with_ok('abc123', ''))
        self.assertTrue(_does_not_start_with_ok('abc123', '123'))
        self.assertTrue(not _does_not_start_with_ok('abc123', 'abc'))


def suite():
    """ define test suite """
    return unittest.TestLoader().loadTestsFromTestCase(Test)


if __name__ == '__main__':
    unittest.main()
