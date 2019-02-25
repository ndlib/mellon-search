# test_parse_embark_xml.py 2/19/19 sm
""" test parse_embark_xml.py """

import json
import unittest
from xml.etree.ElementTree import ElementTree

# add parent directory to path
import os
import inspect
import sys
CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PARENTDIR = os.path.dirname(CURRENTDIR)
sys.path.insert(0, PARENTDIR)

from parse_embark_xml import ParseEmbarkXml
import read_embark_fields_json_file
import get_embark_xml_definitions


class Test(unittest.TestCase):
    """ Class for test fixtures """

    def test_read_and_parse(self):
        """ test Read and Parse """
        xmldoc = ElementTree(file='./objects 01_18_19.xml')
        filename = PARENTDIR + "/EmbArkXMLFields.json"
        embark_field_definitions = read_embark_fields_json_file.read_embark_fields_json_file(filename)
        item_xpath = get_embark_xml_definitions.get_item_xpath(embark_field_definitions)
        fields_definition = get_embark_xml_definitions.get_fields_definition(embark_field_definitions)
        for xml_of_embark_item in xmldoc.findall(item_xpath):
            # xml_of_embark_item contains EmbArk xml for one item.
            json_of_embark_item = {}
            section = ParseEmbarkXml(fields_definition)
            json_of_embark_item = section.parse_embark_record(xml_of_embark_item)
            if section.id == "1976.057":
                expected_json = json.loads('{"recordId": "1976.057", "repository": "Snite", "creator": "Paul Wood", "creationDate": "18910101", "displayDate": "1891", "title": "ABSOLUTION UNDER FIRE", "classification": "Painting", "media": "oil on canvas", "displayDimensions": "76 1/2 x 102 x 3 1/4 in. (194.31 x 259.08 x 8.26 cm)", "exhibition": [{"name": "Picturing History", "startDate": "09/01/94", "endDate": "12/01/94"}], "bibliography": [{"value": "Bilby, Joseph G., Remember Fontenoy!, Longstreet House, Highstown, NJ, 1995, 86"}, {"value": "Burger, John, Columbia, Pelowski, Alton J., Knights of Columbus, New Haven, CT, May 2015, 16-18"}, {"value": "Callaghan, James, Civil War, Miller, William J., Christopher M. Curran, Berryville, VA, August 1997, 26-33"}, {"value": "Carey, John E., The Civil War, The Washington Times, Saturday, Sept. 14, 1996, B3-not illustrated"}, {"value": "Clark, Champ, The Civil War, Time Life Books, 1985, 100-101"}, {"value": "Corby, William, Memoirs of Chaplain Life, Kohl, Lawrence Frederick, Fordham University Press, Chicago, 1893, 385-387"}, {"value": "Faherty, S. J., William Barnaby, Catholic Chaplains in Blue and Gray, Jesuit Missouri Province Archives, St. Louis, MO, 1995, unknown"}, {"value": "Faherty, S. J., William Barnaby, U. S Catholic Historian, Jesuit Missouri Province Archives, St. Louis, MO, Summer 1995, unknown"}, {"value": "Mach, Andrew, American Catholic Studies, Van Allen, Rodger, American Catholic Studies"}, {"value": "Morris, Claire, 69th New York & It\'s Place in The Irish Brigade, 2006, 25"}, {"value": "O\'Beirne, Kevin, Military Heritage, Octtober 1999, 40-41"}, {"value": "Rable, George C., Civil War Times, Civil War Times, North Carolina, December 2003, 56-59, 86-88"}, {"value": "Shattuck, Gardiner H., The Sword of the Lord: , Bergen, Doris, University of Notre Dame Press, Notre Dame, IN, 2004, 105-123, illustrated on pg. 113"}, {"value": "Symonds, Craig L., American Heritage History of the Battle of Gettysburg, HarperCollins , North America, 2001, unknown"}], "keyword": [{"value": "confederate"}, {"value": "battle"}, {"value": "civil war"}, {"value": "priest"}, {"value": "battlefield"}, {"value": "irish"}, {"value": "soldier"}, {"value": "conflict"}, {"value": "AAT:<Associated Concepts Facet>:<Associated Concepts>:<religions and religious concepts>:<religious concepts>:<doctrinal concepts>:absolution"}, {"value": "AAT:<Physical Attributes Facet>:<Attributes and Properties>:<attributes and properties>:<attributes and properties by specific type>:<positional attributes>:compass points:north"}, {"value": "AAT:<Styles and Periods Facet>:<Styles and Periods>:<styles and periods by region>:<The Americas>:<American regions>:South American"}, {"value": "AAT:<Activities Facet>:<Events>:events:armed conflicts"}, {"value": "AAT:<Activities Facet>:<Events>:events:armed conflicts:wars"}, {"value": "AAT:<Activities Facet>:<Events>:events:armed conflicts:wars:civil wars"}, {"value": "AAT:<Objects Facet>:Visual and Verbal Communication:<Visual Works (Hierarchy Name)>:<visual works (Guide Term)>:<visual works by form>:<visual works by form: image form>:depictions"}, {"value": "AAT:<Objects Facet>:Visual and Verbal Communication:<Information Forms (Hierarchy Name)>:<information forms (Guide Term)>:<document genres>:<document genres by form>:<document genres for literary works>:poems:<poems by function>:epics"}]}')
                self.assertTrue(expected_json == json_of_embark_item)


def suite():
    """ define test suite """
    return unittest.TestLoader().loadTestsFromTestCase(Test)


if __name__ == '__main__':
    unittest.main()
