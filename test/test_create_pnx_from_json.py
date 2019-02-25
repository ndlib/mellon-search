#test_create_pnx_from_json.py 2/18/19 sm
""" test create_pnx_from_json.py """

import json
import unittest
from xml.etree import ElementTree

# add parent directory to path
import os
import inspect
import sys
CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PARENTDIR = os.path.dirname(CURRENTDIR)
sys.path.insert(0, PARENTDIR)

from create_pnx_from_json import create_pnx_from_json, create_pnx_from_json_and_write_file \
    , _create_xml_element, _get_json_value, _get_media_and_display, _get_exhibition \
    , _create_search_section, _create_browse_section, _create_sort_section, _create_facet_section \
    , _create_delivery_section

#import read_embark_fields_json_file
#import get_embark_xml_definitions

def get_json_input():
    """ get pre-formed json to make sure testing is uniform """
    json_input = json.loads('{"recordId": "1976.057", "repository": "Snite", "creator": "Paul Wood", "creationDate": "18910101", "displayDate": "1891", "title": "ABSOLUTION UNDER FIRE", "classification": "Painting", "media": "oil on canvas", "displayDimensions": "76 1/2 x 102 x 3 1/4 in. (194.31 x 259.08 x 8.26 cm)", "exhibition": [{"name": "Picturing History", "startDate": "09/01/94", "endDate": "12/01/94"}], "bibliography": [{"value": "Bilby, Joseph G., Remember Fontenoy!, Longstreet House, Highstown, NJ, 1995, 86"}, {"value": "Burger, John, Columbia, Pelowski, Alton J., Knights of Columbus, New Haven, CT, May 2015, 16-18"}, {"value": "Callaghan, James, Civil War, Miller, William J., Christopher M. Curran, Berryville, VA, August 1997, 26-33"}, {"value": "Carey, John E., The Civil War, The Washington Times, Saturday, Sept. 14, 1996, B3-not illustrated"}, {"value": "Clark, Champ, The Civil War, Time Life Books, 1985, 100-101"}, {"value": "Corby, William, Memoirs of Chaplain Life, Kohl, Lawrence Frederick, Fordham University Press, Chicago, 1893, 385-387"}, {"value": "Faherty, S. J., William Barnaby, Catholic Chaplains in Blue and Gray, Jesuit Missouri Province Archives, St. Louis, MO, 1995, unknown"}, {"value": "Faherty, S. J., William Barnaby, U. S Catholic Historian, Jesuit Missouri Province Archives, St. Louis, MO, Summer 1995, unknown"}, {"value": "Mach, Andrew, American Catholic Studies, Van Allen, Rodger, American Catholic Studies"}, {"value": "Morris, Claire, 69th New York & It\'s Place in The Irish Brigade, 2006, 25"}, {"value": "O\'Beirne, Kevin, Military Heritage, Octtober 1999, 40-41"}, {"value": "Rable, George C., Civil War Times, Civil War Times, North Carolina, December 2003, 56-59, 86-88"}, {"value": "Shattuck, Gardiner H., The Sword of the Lord: , Bergen, Doris, University of Notre Dame Press, Notre Dame, IN, 2004, 105-123, illustrated on pg. 113"}, {"value": "Symonds, Craig L., American Heritage History of the Battle of Gettysburg, HarperCollins , North America, 2001, unknown"}], "keyword": [{"value": "confederate"}, {"value": "battle"}, {"value": "civil war"}, {"value": "priest"}, {"value": "battlefield"}, {"value": "irish"}, {"value": "soldier"}, {"value": "conflict"}, {"value": "AAT:<Associated Concepts Facet>:<Associated Concepts>:<religions and religious concepts>:<religious concepts>:<doctrinal concepts>:absolution"}, {"value": "AAT:<Physical Attributes Facet>:<Attributes and Properties>:<attributes and properties>:<attributes and properties by specific type>:<positional attributes>:compass points:north"}, {"value": "AAT:<Styles and Periods Facet>:<Styles and Periods>:<styles and periods by region>:<The Americas>:<American regions>:South American"}, {"value": "AAT:<Activities Facet>:<Events>:events:armed conflicts"}, {"value": "AAT:<Activities Facet>:<Events>:events:armed conflicts:wars"}, {"value": "AAT:<Activities Facet>:<Events>:events:armed conflicts:wars:civil wars"}, {"value": "AAT:<Objects Facet>:Visual and Verbal Communication:<Visual Works (Hierarchy Name)>:<visual works (Guide Term)>:<visual works by form>:<visual works by form: image form>:depictions"}, {"value": "AAT:<Objects Facet>:Visual and Verbal Communication:<Information Forms (Hierarchy Name)>:<information forms (Guide Term)>:<document genres>:<document genres by form>:<document genres for literary works>:poems:<poems by function>:epics"}]}')
    return json_input

class Test(unittest.TestCase):
    """ Class for test fixtures """

    def test_create_xml_element(self):
        """ test _create_xml_elemen """
        xml = _create_xml_element('element_name', 'element_text')
        self.assertTrue(ElementTree.tostring(xml) == b'<element_name>element_text</element_name>')

    def test_get_json_value(self):
        """ test _get_json_value """
        json_input = get_json_input()
        text = _get_json_value(json_input, 'recordId')
        self.assertTrue(text == '1976.057')

    def test_get_media_and_display(self):
        """ test _get_media_and_display(json_input) """
        json_input = get_json_input()
        text = _get_media_and_display(json_input)
        self.assertTrue(text == 'oil on canvas, 76 1/2 x 102 x 3 1/4 in. (194.31 x 259.08 x 8.26 cm)')

    def test_get_exhibition(self):
        """ test _get_exhibition """
        json_input = get_json_input()
        if 'exhibition' in json_input:
            for exhibition_json in json_input['exhibition']:
                if 'name' in exhibition_json:
                    text = _get_exhibition(exhibition_json)
                    self.assertTrue(text == 'Picturing History (09/01/94 - 12/01/94)')

    def test_create_search_section(self):
        """ test _create_search_section """
        json_input = get_json_input()
        xml = _create_search_section(json_input)
        expected_results = b'<search><recordid>1976.057</recordid><title>ABSOLUTION UNDER FIRE</title><creator>Paul Wood</creator><creationdate>18910101</creationdate><general>oil on canvas, 76 1/2 x 102 x 3 1/4 in. (194.31 x 259.08 x 8.26 cm)</general><lsr09>painting</lsr09><rsrctype>painting</rsrctype><scope>SNITE</scope><subject>confederate</subject><subject>battle</subject><subject>civil war</subject><subject>priest</subject><subject>battlefield</subject><subject>irish</subject><subject>soldier</subject><subject>conflict</subject><subject>AAT:&lt;Associated Concepts Facet&gt;:&lt;Associated Concepts&gt;:&lt;religions and religious concepts&gt;:&lt;religious concepts&gt;:&lt;doctrinal concepts&gt;:absolution</subject><subject>AAT:&lt;Physical Attributes Facet&gt;:&lt;Attributes and Properties&gt;:&lt;attributes and properties&gt;:&lt;attributes and properties by specific type&gt;:&lt;positional attributes&gt;:compass points:north</subject><subject>AAT:&lt;Styles and Periods Facet&gt;:&lt;Styles and Periods&gt;:&lt;styles and periods by region&gt;:&lt;The Americas&gt;:&lt;American regions&gt;:South American</subject><subject>AAT:&lt;Activities Facet&gt;:&lt;Events&gt;:events:armed conflicts</subject><subject>AAT:&lt;Activities Facet&gt;:&lt;Events&gt;:events:armed conflicts:wars</subject><subject>AAT:&lt;Activities Facet&gt;:&lt;Events&gt;:events:armed conflicts:wars:civil wars</subject><subject>AAT:&lt;Objects Facet&gt;:Visual and Verbal Communication:&lt;Visual Works (Hierarchy Name)&gt;:&lt;visual works (Guide Term)&gt;:&lt;visual works by form&gt;:&lt;visual works by form: image form&gt;:depictions</subject><subject>AAT:&lt;Objects Facet&gt;:Visual and Verbal Communication:&lt;Information Forms (Hierarchy Name)&gt;:&lt;information forms (Guide Term)&gt;:&lt;document genres&gt;:&lt;document genres by form&gt;:&lt;document genres for literary works&gt;:poems:&lt;poems by function&gt;:epics</subject><creatorcontrib>Picturing History (09/01/94 - 12/01/94)</creatorcontrib></search>'
        self.assertTrue(ElementTree.tostring(xml) == expected_results)

    def test_create_browse_section(self):
        """ test _create_browse_section """
        json_input = get_json_input()
        xml = _create_browse_section(json_input)
        expected_results = b'<browse><title>ABSOLUTION UNDER FIRE</title><author>Paul Wood</author><institution>SNITE</institution></browse>'
        self.assertTrue(ElementTree.tostring(xml) == expected_results)

    def test_create_sort_section(self):
        """ test _create_sort_section """
        json_input = get_json_input()
        xml = _create_sort_section(json_input)
        expected_results = b'<sort><title>ABSOLUTION UNDER FIRE</title><author>Paul Wood</author><creationdate>18910101</creationdate></sort>'
        self.assertTrue(ElementTree.tostring(xml) == expected_results)

    def test_create_facet_section(self):
        """ test _create_facet_section """
        json_input = get_json_input()
        xml = _create_facet_section(json_input)
        #print(ElementTree.tostring(xml))
        expected_results = b'<facet><creatorcontrib>Paul Wood</creatorcontrib><lfc09>painting</lfc09><rsrctype>painting</rsrctype><library>SNITE</library><creationdate>18910101</creationdate><topic>confederate</topic><topic>battle</topic><topic>civil war</topic><topic>priest</topic><topic>battlefield</topic><topic>irish</topic><topic>soldier</topic><topic>conflict</topic><topic>AAT:&lt;Associated Concepts Facet&gt;:&lt;Associated Concepts&gt;:&lt;religions and religious concepts&gt;:&lt;religious concepts&gt;:&lt;doctrinal concepts&gt;:absolution</topic><topic>AAT:&lt;Physical Attributes Facet&gt;:&lt;Attributes and Properties&gt;:&lt;attributes and properties&gt;:&lt;attributes and properties by specific type&gt;:&lt;positional attributes&gt;:compass points:north</topic><topic>AAT:&lt;Styles and Periods Facet&gt;:&lt;Styles and Periods&gt;:&lt;styles and periods by region&gt;:&lt;The Americas&gt;:&lt;American regions&gt;:South American</topic><topic>AAT:&lt;Activities Facet&gt;:&lt;Events&gt;:events:armed conflicts</topic><topic>AAT:&lt;Activities Facet&gt;:&lt;Events&gt;:events:armed conflicts:wars</topic><topic>AAT:&lt;Activities Facet&gt;:&lt;Events&gt;:events:armed conflicts:wars:civil wars</topic><topic>AAT:&lt;Objects Facet&gt;:Visual and Verbal Communication:&lt;Visual Works (Hierarchy Name)&gt;:&lt;visual works (Guide Term)&gt;:&lt;visual works by form&gt;:&lt;visual works by form: image form&gt;:depictions</topic><topic>AAT:&lt;Objects Facet&gt;:Visual and Verbal Communication:&lt;Information Forms (Hierarchy Name)&gt;:&lt;information forms (Guide Term)&gt;:&lt;document genres&gt;:&lt;document genres by form&gt;:&lt;document genres for literary works&gt;:poems:&lt;poems by function&gt;:epics</topic></facet>'
        self.assertTrue(ElementTree.tostring(xml) == expected_results)

    def test_create_delivery_section(self):
        """ test _create_delivery_section """
        json_input = get_json_input()
        xml = _create_delivery_section(json_input)
        expected_results = b'<delivery><delcategory>Physical Item</delcategory><institution>SNITE</institution></delivery>'
        #print(ElementTree.tostring(xml))
        self.assertTrue(ElementTree.tostring(xml) == expected_results)



    def test_create_pnx_from_json(self):
        """ run test to create PNX record for a single item from a single JSON file """
        json_input = get_json_input()
        xml_tree = create_pnx_from_json(json_input)
        expected_results = b'<records><record xmlns="http://www.exlibrisgroup.com/xsd/primo/primo_nm_bib" xmlns:sear="http://www.exlibrisgroup.com/xsd/jaguar/search"><id>1976.057</id><display><lds02>1976.057</lds02><title>ABSOLUTION UNDER FIRE</title><creator>Paul Wood</creator><creationdate>1891</creationdate><format>oil on canvas, 76 1/2 x 102 x 3 1/4 in. (194.31 x 259.08 x 8.26 cm)</format><lds09>painting</lds09><type>painting</type><lsd10>Snite</lsd10><subject>confederate</subject><subject>battle</subject><subject>civil war</subject><subject>priest</subject><subject>battlefield</subject><subject>irish</subject><subject>soldier</subject><subject>conflict</subject><subject>AAT:&lt;Associated Concepts Facet&gt;:&lt;Associated Concepts&gt;:&lt;religions and religious concepts&gt;:&lt;religious concepts&gt;:&lt;doctrinal concepts&gt;:absolution</subject><subject>AAT:&lt;Physical Attributes Facet&gt;:&lt;Attributes and Properties&gt;:&lt;attributes and properties&gt;:&lt;attributes and properties by specific type&gt;:&lt;positional attributes&gt;:compass points:north</subject><subject>AAT:&lt;Styles and Periods Facet&gt;:&lt;Styles and Periods&gt;:&lt;styles and periods by region&gt;:&lt;The Americas&gt;:&lt;American regions&gt;:South American</subject><subject>AAT:&lt;Activities Facet&gt;:&lt;Events&gt;:events:armed conflicts</subject><subject>AAT:&lt;Activities Facet&gt;:&lt;Events&gt;:events:armed conflicts:wars</subject><subject>AAT:&lt;Activities Facet&gt;:&lt;Events&gt;:events:armed conflicts:wars:civil wars</subject><subject>AAT:&lt;Objects Facet&gt;:Visual and Verbal Communication:&lt;Visual Works (Hierarchy Name)&gt;:&lt;visual works (Guide Term)&gt;:&lt;visual works by form&gt;:&lt;visual works by form: image form&gt;:depictions</subject><subject>AAT:&lt;Objects Facet&gt;:Visual and Verbal Communication:&lt;Information Forms (Hierarchy Name)&gt;:&lt;information forms (Guide Term)&gt;:&lt;document genres&gt;:&lt;document genres by form&gt;:&lt;document genres for literary works&gt;:poems:&lt;poems by function&gt;:epics</subject><lds01>Bilby, Joseph G., Remember Fontenoy!, Longstreet House, Highstown, NJ, 1995, 86</lds01><lds01>Burger, John, Columbia, Pelowski, Alton J., Knights of Columbus, New Haven, CT, May 2015, 16-18</lds01><lds01>Callaghan, James, Civil War, Miller, William J., Christopher M. Curran, Berryville, VA, August 1997, 26-33</lds01><lds01>Carey, John E., The Civil War, The Washington Times, Saturday, Sept. 14, 1996, B3-not illustrated</lds01><lds01>Clark, Champ, The Civil War, Time Life Books, 1985, 100-101</lds01><lds01>Corby, William, Memoirs of Chaplain Life, Kohl, Lawrence Frederick, Fordham University Press, Chicago, 1893, 385-387</lds01><lds01>Faherty, S. J., William Barnaby, Catholic Chaplains in Blue and Gray, Jesuit Missouri Province Archives, St. Louis, MO, 1995, unknown</lds01><lds01>Faherty, S. J., William Barnaby, U. S Catholic Historian, Jesuit Missouri Province Archives, St. Louis, MO, Summer 1995, unknown</lds01><lds01>Mach, Andrew, American Catholic Studies, Van Allen, Rodger, American Catholic Studies</lds01><lds01>Morris, Claire, 69th New York &amp; It\'s Place in The Irish Brigade, 2006, 25</lds01><lds01>O\'Beirne, Kevin, Military Heritage, Octtober 1999, 40-41</lds01><lds01>Rable, George C., Civil War Times, Civil War Times, North Carolina, December 2003, 56-59, 86-88</lds01><lds01>Shattuck, Gardiner H., The Sword of the Lord: , Bergen, Doris, University of Notre Dame Press, Notre Dame, IN, 2004, 105-123, illustrated on pg. 113</lds01><lds01>Symonds, Craig L., American Heritage History of the Battle of Gettysburg, HarperCollins , North America, 2001, unknown</lds01><contributor>Picturing History (09/01/94 - 12/01/94)</contributor></display><search><recordid>1976.057</recordid><title>ABSOLUTION UNDER FIRE</title><creator>Paul Wood</creator><creationdate>18910101</creationdate><general>oil on canvas, 76 1/2 x 102 x 3 1/4 in. (194.31 x 259.08 x 8.26 cm)</general><lsr09>painting</lsr09><rsrctype>painting</rsrctype><scope>SNITE</scope><subject>confederate</subject><subject>battle</subject><subject>civil war</subject><subject>priest</subject><subject>battlefield</subject><subject>irish</subject><subject>soldier</subject><subject>conflict</subject><subject>AAT:&lt;Associated Concepts Facet&gt;:&lt;Associated Concepts&gt;:&lt;religions and religious concepts&gt;:&lt;religious concepts&gt;:&lt;doctrinal concepts&gt;:absolution</subject><subject>AAT:&lt;Physical Attributes Facet&gt;:&lt;Attributes and Properties&gt;:&lt;attributes and properties&gt;:&lt;attributes and properties by specific type&gt;:&lt;positional attributes&gt;:compass points:north</subject><subject>AAT:&lt;Styles and Periods Facet&gt;:&lt;Styles and Periods&gt;:&lt;styles and periods by region&gt;:&lt;The Americas&gt;:&lt;American regions&gt;:South American</subject><subject>AAT:&lt;Activities Facet&gt;:&lt;Events&gt;:events:armed conflicts</subject><subject>AAT:&lt;Activities Facet&gt;:&lt;Events&gt;:events:armed conflicts:wars</subject><subject>AAT:&lt;Activities Facet&gt;:&lt;Events&gt;:events:armed conflicts:wars:civil wars</subject><subject>AAT:&lt;Objects Facet&gt;:Visual and Verbal Communication:&lt;Visual Works (Hierarchy Name)&gt;:&lt;visual works (Guide Term)&gt;:&lt;visual works by form&gt;:&lt;visual works by form: image form&gt;:depictions</subject><subject>AAT:&lt;Objects Facet&gt;:Visual and Verbal Communication:&lt;Information Forms (Hierarchy Name)&gt;:&lt;information forms (Guide Term)&gt;:&lt;document genres&gt;:&lt;document genres by form&gt;:&lt;document genres for literary works&gt;:poems:&lt;poems by function&gt;:epics</subject><creatorcontrib>Picturing History (09/01/94 - 12/01/94)</creatorcontrib></search><browse><title>ABSOLUTION UNDER FIRE</title><author>Paul Wood</author><institution>SNITE</institution></browse><sort><title>ABSOLUTION UNDER FIRE</title><author>Paul Wood</author><creationdate>18910101</creationdate></sort><facet><creatorcontrib>Paul Wood</creatorcontrib><lfc09>painting</lfc09><rsrctype>painting</rsrctype><library>SNITE</library><creationdate>18910101</creationdate><topic>confederate</topic><topic>battle</topic><topic>civil war</topic><topic>priest</topic><topic>battlefield</topic><topic>irish</topic><topic>soldier</topic><topic>conflict</topic><topic>AAT:&lt;Associated Concepts Facet&gt;:&lt;Associated Concepts&gt;:&lt;religions and religious concepts&gt;:&lt;religious concepts&gt;:&lt;doctrinal concepts&gt;:absolution</topic><topic>AAT:&lt;Physical Attributes Facet&gt;:&lt;Attributes and Properties&gt;:&lt;attributes and properties&gt;:&lt;attributes and properties by specific type&gt;:&lt;positional attributes&gt;:compass points:north</topic><topic>AAT:&lt;Styles and Periods Facet&gt;:&lt;Styles and Periods&gt;:&lt;styles and periods by region&gt;:&lt;The Americas&gt;:&lt;American regions&gt;:South American</topic><topic>AAT:&lt;Activities Facet&gt;:&lt;Events&gt;:events:armed conflicts</topic><topic>AAT:&lt;Activities Facet&gt;:&lt;Events&gt;:events:armed conflicts:wars</topic><topic>AAT:&lt;Activities Facet&gt;:&lt;Events&gt;:events:armed conflicts:wars:civil wars</topic><topic>AAT:&lt;Objects Facet&gt;:Visual and Verbal Communication:&lt;Visual Works (Hierarchy Name)&gt;:&lt;visual works (Guide Term)&gt;:&lt;visual works by form&gt;:&lt;visual works by form: image form&gt;:depictions</topic><topic>AAT:&lt;Objects Facet&gt;:Visual and Verbal Communication:&lt;Information Forms (Hierarchy Name)&gt;:&lt;information forms (Guide Term)&gt;:&lt;document genres&gt;:&lt;document genres by form&gt;:&lt;document genres for literary works&gt;:poems:&lt;poems by function&gt;:epics</topic></facet><delivery><delcategory>Physical Item</delcategory><institution>SNITE</institution></delivery></record></records>\n'
        #print(ElementTree.tostring(xml_tree.getroot()))
        self.assertTrue(ElementTree.tostring(xml_tree.getroot()) == expected_results)


    def test_create_pnx_from_json_and_write_file(self):
        """ run test to create PNX record for a single item from a single JSON file """
        json_input = get_json_input()
        xml_created = create_pnx_from_json(json_input)
        xml_written = create_pnx_from_json_and_write_file('pnx', json_input)
        self.assertTrue(ElementTree.tostring(xml_created.getroot()) == ElementTree.tostring(xml_written.getroot()))


def suite():
    """ define test suite """
    return unittest.TestLoader().loadTestsFromTestCase(Test)


if __name__ == '__main__':
    unittest.main()
