#test_write_main_csv.py 2/18/19 sm
""" test write_main_csv.py """

import json
import unittest
import csv

# add parent directory to path
import os
import inspect
import sys
CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PARENTDIR = os.path.dirname(CURRENTDIR)
sys.path.insert(0, PARENTDIR)

# this adds the current directory to the path if needed
#sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# import what I need from the parent directory
from write_main_csv import _create_first_row, _create_metadata_row, _create_metadata_row_from_string, \
    _create_exhibition_metadata_row, _create_metadata_array_row, _create_metadata_rows, write_main_csv

def get_json_input():
    """ get pre-formed json to make sure testing is uniform """
    json_input = json.loads('{"recordId": "1976.057", "repository": "Snite", "creator": "Paul Wood", "creationDate": "18910101", "displayDate": "1891", "title": "ABSOLUTION UNDER FIRE", "classification": "Painting", "media": "oil on canvas", "displayDimensions": "76 1/2 x 102 x 3 1/4 in. (194.31 x 259.08 x 8.26 cm)", "exhibition": [{"name": "Picturing History", "startDate": "09/01/94", "endDate": "12/01/94"}], "bibliography": [{"value": "Bilby, Joseph G., Remember Fontenoy!, Longstreet House, Highstown, NJ, 1995, 86"}, {"value": "Burger, John, Columbia, Pelowski, Alton J., Knights of Columbus, New Haven, CT, May 2015, 16-18"}, {"value": "Callaghan, James, Civil War, Miller, William J., Christopher M. Curran, Berryville, VA, August 1997, 26-33"}, {"value": "Carey, John E., The Civil War, The Washington Times, Saturday, Sept. 14, 1996, B3-not illustrated"}, {"value": "Clark, Champ, The Civil War, Time Life Books, 1985, 100-101"}, {"value": "Corby, William, Memoirs of Chaplain Life, Kohl, Lawrence Frederick, Fordham University Press, Chicago, 1893, 385-387"}, {"value": "Faherty, S. J., William Barnaby, Catholic Chaplains in Blue and Gray, Jesuit Missouri Province Archives, St. Louis, MO, 1995, unknown"}, {"value": "Faherty, S. J., William Barnaby, U. S Catholic Historian, Jesuit Missouri Province Archives, St. Louis, MO, Summer 1995, unknown"}, {"value": "Mach, Andrew, American Catholic Studies, Van Allen, Rodger, American Catholic Studies"}, {"value": "Morris, Claire, 69th New York & It\'s Place in The Irish Brigade, 2006, 25"}, {"value": "O\'Beirne, Kevin, Military Heritage, Octtober 1999, 40-41"}, {"value": "Rable, George C., Civil War Times, Civil War Times, North Carolina, December 2003, 56-59, 86-88"}, {"value": "Shattuck, Gardiner H., The Sword of the Lord: , Bergen, Doris, University of Notre Dame Press, Notre Dame, IN, 2004, 105-123, illustrated on pg. 113"}, {"value": "Symonds, Craig L., American Heritage History of the Battle of Gettysburg, HarperCollins , North America, 2001, unknown"}], "keyword": [{"value": "confederate"}, {"value": "battle"}, {"value": "civil war"}, {"value": "priest"}, {"value": "battlefield"}, {"value": "irish"}, {"value": "soldier"}, {"value": "conflict"}, {"value": "AAT:<Associated Concepts Facet>:<Associated Concepts>:<religions and religious concepts>:<religious concepts>:<doctrinal concepts>:absolution"}, {"value": "AAT:<Physical Attributes Facet>:<Attributes and Properties>:<attributes and properties>:<attributes and properties by specific type>:<positional attributes>:compass points:north"}, {"value": "AAT:<Styles and Periods Facet>:<Styles and Periods>:<styles and periods by region>:<The Americas>:<American regions>:South American"}, {"value": "AAT:<Activities Facet>:<Events>:events:armed conflicts"}, {"value": "AAT:<Activities Facet>:<Events>:events:armed conflicts:wars"}, {"value": "AAT:<Activities Facet>:<Events>:events:armed conflicts:wars:civil wars"}, {"value": "AAT:<Objects Facet>:Visual and Verbal Communication:<Visual Works (Hierarchy Name)>:<visual works (Guide Term)>:<visual works by form>:<visual works by form: image form>:depictions"}, {"value": "AAT:<Objects Facet>:Visual and Verbal Communication:<Information Forms (Hierarchy Name)>:<information forms (Guide Term)>:<document genres>:<document genres by form>:<document genres for literary works>:poems:<poems by function>:epics"}]}')
    return json_input


class Test(unittest.TestCase):
    """ Class for test fixtures """

    def test_create_first_row(self):
        """ test _create_first_row """
        json_data = get_json_input()
        row = _create_first_row(json_data)
        expected_json = json.loads('{"Label": "ABSOLUTION UNDER FIRE", "Description": "ABSOLUTION UNDER FIRE", "License": "<a href=\\"http://rightsstatements.org/vocab/NoC-US/1.0/\\" target=\\"_blank\\">No Copyright - United States</a>", "Attribution": "University of Notre Dame::Hesburgh Libraries::General", "Sequence_filename": "", "Sequence_label": "Sequence1", "Sequence_viewing_experience": "individuals", "unique_identifier": "1976.057"}')
        self.assertTrue(row == expected_json)

    def test_create_metadata_row(self):
        """ test create_metadata_row """
        json_data = get_json_input()
        row = _create_metadata_row(json_data, 'recordId', 'Accession Number')
        self.assertTrue(row == json.loads('{"Metadata_label": "Accession Number", "Metadata_value": "1976.057"}'))

    def test_create_metadata_row_from_string(self):
        """ test _create_metadata_row_from_string """
        row = _create_metadata_row_from_string('element_label', 'element_string')
        self.assertTrue(row == json.loads('{"Metadata_label": "element_label", "Metadata_value": "element_string"}'))

    def test_create_exhibition_metadata_row(self):
        """ test _create_exhibition_metadata_row """
        json_data = get_json_input()
        row = _create_exhibition_metadata_row(json_data, 'exhibition', 'Exhibition')
        self.assertTrue(row == json.loads('{"Metadata_label": "Exhibition", "Metadata_value": "Picturing History(09/01/94 - 12/01/94)\\n"}'))

    def test_create_metadata_array_row(self):
        """ test _create_metadata_array_row(json_data, 'bibliography', 'Bibliography') """
        json_data = get_json_input()
        row = _create_metadata_array_row(json_data, 'bibliography', 'Bibliography')
        expected_row = json.loads('{"Metadata_label": "Bibliography", "Metadata_value": "Bilby, Joseph G., Remember Fontenoy!, Longstreet House, Highstown, NJ, 1995, 86\\nBurger, John, Columbia, Pelowski, Alton J., Knights of Columbus, New Haven, CT, May 2015, 16-18\\nCallaghan, James, Civil War, Miller, William J., Christopher M. Curran, Berryville, VA, August 1997, 26-33\\nCarey, John E., The Civil War, The Washington Times, Saturday, Sept. 14, 1996, B3-not illustrated\\nClark, Champ, The Civil War, Time Life Books, 1985, 100-101\\nCorby, William, Memoirs of Chaplain Life, Kohl, Lawrence Frederick, Fordham University Press, Chicago, 1893, 385-387\\nFaherty, S. J., William Barnaby, Catholic Chaplains in Blue and Gray, Jesuit Missouri Province Archives, St. Louis, MO, 1995, unknown\\nFaherty, S. J., William Barnaby, U. S Catholic Historian, Jesuit Missouri Province Archives, St. Louis, MO, Summer 1995, unknown\\nMach, Andrew, American Catholic Studies, Van Allen, Rodger, American Catholic Studies\\nMorris, Claire, 69th New York & It\'s Place in The Irish Brigade, 2006, 25\\nO\'Beirne, Kevin, Military Heritage, Octtober 1999, 40-41\\nRable, George C., Civil War Times, Civil War Times, North Carolina, December 2003, 56-59, 86-88\\nShattuck, Gardiner H., The Sword of the Lord: , Bergen, Doris, University of Notre Dame Press, Notre Dame, IN, 2004, 105-123, illustrated on pg. 113\\nSymonds, Craig L., American Heritage History of the Battle of Gettysburg, HarperCollins , North America, 2001, unknown\\n"}')
        self.assertTrue(row == expected_row)

    def test__create_metadata_rows(self):
        """ test _create_metadata_rows """
        json_data = get_json_input()
        rows = _create_metadata_rows(json_data)
        expected_rows = [{'Metadata_label': 'Accession Number', 'Metadata_value': '1976.057'}, {'Metadata_label': 'Repository', 'Metadata_value': 'Snite'}, {'Metadata_label': 'Creator', 'Metadata_value': 'Paul Wood'}, {'Metadata_label': 'Creation Date', 'Metadata_value': '18910101'}, {'Metadata_label': 'Display Date', 'Metadata_value': '1891'}, {'Metadata_label': 'Title', 'Metadata_value': 'ABSOLUTION UNDER FIRE'}, {'Metadata_label': 'Classification', 'Metadata_value': 'Painting'}, {'Metadata_label': 'Media', 'Metadata_value': 'oil on canvas'}, {'Metadata_label': 'Dimensions', 'Metadata_value': '76 1/2 x 102 x 3 1/4 in. (194.31 x 259.08 x 8.26 cm)'}, {'Metadata_label': 'Exhibition', 'Metadata_value': 'Picturing History(09/01/94 - 12/01/94)\n'}, {}, {'Metadata_label': 'Bibliography', 'Metadata_value': "Bilby, Joseph G., Remember Fontenoy!, Longstreet House, Highstown, NJ, 1995, 86\nBurger, John, Columbia, Pelowski, Alton J., Knights of Columbus, New Haven, CT, May 2015, 16-18\nCallaghan, James, Civil War, Miller, William J., Christopher M. Curran, Berryville, VA, August 1997, 26-33\nCarey, John E., The Civil War, The Washington Times, Saturday, Sept. 14, 1996, B3-not illustrated\nClark, Champ, The Civil War, Time Life Books, 1985, 100-101\nCorby, William, Memoirs of Chaplain Life, Kohl, Lawrence Frederick, Fordham University Press, Chicago, 1893, 385-387\nFaherty, S. J., William Barnaby, Catholic Chaplains in Blue and Gray, Jesuit Missouri Province Archives, St. Louis, MO, 1995, unknown\nFaherty, S. J., William Barnaby, U. S Catholic Historian, Jesuit Missouri Province Archives, St. Louis, MO, Summer 1995, unknown\nMach, Andrew, American Catholic Studies, Van Allen, Rodger, American Catholic Studies\nMorris, Claire, 69th New York & It's Place in The Irish Brigade, 2006, 25\nO'Beirne, Kevin, Military Heritage, Octtober 1999, 40-41\nRable, George C., Civil War Times, Civil War Times, North Carolina, December 2003, 56-59, 86-88\nShattuck, Gardiner H., The Sword of the Lord: , Bergen, Doris, University of Notre Dame Press, Notre Dame, IN, 2004, 105-123, illustrated on pg. 113\nSymonds, Craig L., American Heritage History of the Battle of Gettysburg, HarperCollins , North America, 2001, unknown\n"}, {'Metadata_label': 'Key words', 'Metadata_value': 'confederate\nbattle\ncivil war\npriest\nbattlefield\nirish\nsoldier\nconflict\nAAT:<Associated Concepts Facet>:<Associated Concepts>:<religions and religious concepts>:<religious concepts>:<doctrinal concepts>:absolution\nAAT:<Physical Attributes Facet>:<Attributes and Properties>:<attributes and properties>:<attributes and properties by specific type>:<positional attributes>:compass points:north\nAAT:<Styles and Periods Facet>:<Styles and Periods>:<styles and periods by region>:<The Americas>:<American regions>:South American\nAAT:<Activities Facet>:<Events>:events:armed conflicts\nAAT:<Activities Facet>:<Events>:events:armed conflicts:wars\nAAT:<Activities Facet>:<Events>:events:armed conflicts:wars:civil wars\nAAT:<Objects Facet>:Visual and Verbal Communication:<Visual Works (Hierarchy Name)>:<visual works (Guide Term)>:<visual works by form>:<visual works by form: image form>:depictions\nAAT:<Objects Facet>:Visual and Verbal Communication:<Information Forms (Hierarchy Name)>:<information forms (Guide Term)>:<document genres>:<document genres by form>:<document genres for literary works>:poems:<poems by function>:epics\n'}]
        self.assertTrue(rows == expected_rows)

    def testwrite_main_csv(self):
        """ test write_main_csv """
        json_data = get_json_input()
        write_main_csv('.', json_data)
        #read file
        lines = {}
        with open('./main.csv', 'r') as read_file:
            reader = csv.reader(read_file)
            lines = list(reader)
        expected_results = [['Label', 'Description', 'License', 'Attribution', 'Sequence_filename', 'Sequence_label', 'Sequence_viewing_experience', 'unique_identifier', 'Metadata_label', 'Metadata_value'], ['ABSOLUTION UNDER FIRE', 'ABSOLUTION UNDER FIRE', '<a href="http://rightsstatements.org/vocab/NoC-US/1.0/" target="_blank">No Copyright - United States</a>', 'University of Notre Dame::Hesburgh Libraries::General', '', 'Sequence1', 'individuals', '1976.057', '', ''], ['', '', '', '', '', '', '', '', 'Accession Number', '1976.057'], ['', '', '', '', '', '', '', '', 'Repository', 'Snite'], ['', '', '', '', '', '', '', '', 'Creator', 'Paul Wood'], ['', '', '', '', '', '', '', '', 'Creation Date', '18910101'], ['', '', '', '', '', '', '', '', 'Display Date', '1891'], ['', '', '', '', '', '', '', '', 'Title', 'ABSOLUTION UNDER FIRE'], ['', '', '', '', '', '', '', '', 'Classification', 'Painting'], ['', '', '', '', '', '', '', '', 'Media', 'oil on canvas'], ['', '', '', '', '', '', '', '', 'Dimensions', '76 1/2 x 102 x 3 1/4 in. (194.31 x 259.08 x 8.26 cm)'], ['', '', '', '', '', '', '', '', 'Exhibition', 'Picturing History(09/01/94 - 12/01/94)\n'], ['', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', 'Bibliography', "Bilby, Joseph G., Remember Fontenoy!, Longstreet House, Highstown, NJ, 1995, 86\nBurger, John, Columbia, Pelowski, Alton J., Knights of Columbus, New Haven, CT, May 2015, 16-18\nCallaghan, James, Civil War, Miller, William J., Christopher M. Curran, Berryville, VA, August 1997, 26-33\nCarey, John E., The Civil War, The Washington Times, Saturday, Sept. 14, 1996, B3-not illustrated\nClark, Champ, The Civil War, Time Life Books, 1985, 100-101\nCorby, William, Memoirs of Chaplain Life, Kohl, Lawrence Frederick, Fordham University Press, Chicago, 1893, 385-387\nFaherty, S. J., William Barnaby, Catholic Chaplains in Blue and Gray, Jesuit Missouri Province Archives, St. Louis, MO, 1995, unknown\nFaherty, S. J., William Barnaby, U. S Catholic Historian, Jesuit Missouri Province Archives, St. Louis, MO, Summer 1995, unknown\nMach, Andrew, American Catholic Studies, Van Allen, Rodger, American Catholic Studies\nMorris, Claire, 69th New York & It's Place in The Irish Brigade, 2006, 25\nO'Beirne, Kevin, Military Heritage, Octtober 1999, 40-41\nRable, George C., Civil War Times, Civil War Times, North Carolina, December 2003, 56-59, 86-88\nShattuck, Gardiner H., The Sword of the Lord: , Bergen, Doris, University of Notre Dame Press, Notre Dame, IN, 2004, 105-123, illustrated on pg. 113\nSymonds, Craig L., American Heritage History of the Battle of Gettysburg, HarperCollins , North America, 2001, unknown\n"], ['', '', '', '', '', '', '', '', 'Key words', 'confederate\nbattle\ncivil war\npriest\nbattlefield\nirish\nsoldier\nconflict\nAAT:<Associated Concepts Facet>:<Associated Concepts>:<religions and religious concepts>:<religious concepts>:<doctrinal concepts>:absolution\nAAT:<Physical Attributes Facet>:<Attributes and Properties>:<attributes and properties>:<attributes and properties by specific type>:<positional attributes>:compass points:north\nAAT:<Styles and Periods Facet>:<Styles and Periods>:<styles and periods by region>:<The Americas>:<American regions>:South American\nAAT:<Activities Facet>:<Events>:events:armed conflicts\nAAT:<Activities Facet>:<Events>:events:armed conflicts:wars\nAAT:<Activities Facet>:<Events>:events:armed conflicts:wars:civil wars\nAAT:<Objects Facet>:Visual and Verbal Communication:<Visual Works (Hierarchy Name)>:<visual works (Guide Term)>:<visual works by form>:<visual works by form: image form>:depictions\nAAT:<Objects Facet>:Visual and Verbal Communication:<Information Forms (Hierarchy Name)>:<information forms (Guide Term)>:<document genres>:<document genres by form>:<document genres for literary works>:poems:<poems by function>:epics\n']]
        self.assertTrue(lines == expected_results)


def suite():
    """ define test suite """
    return unittest.TestLoader().loadTestsFromTestCase(Test)


if __name__ == '__main__':
    unittest.main()
