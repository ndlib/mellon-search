# get_individual_field_from_embark_xml.py 2/12/19 sm
""" Retrieve data from EmbArk given JSON field definition """

from __future__ import print_function

from get_embark_xml_definitions import get_field_name, \
    get_field_required, get_field_duplicates_allowed, get_field_xpath, \
    get_field_default, get_does_not_start_with, get_starts_with, \
    get_validation_rule, get_constant
from get_valid_date import get_valid_yyyymmdd_date


def _starts_with_ok(text, starts_with):
    """ Returns True if text starts with the string (if any) in starts_with
        Else return False """
    if (starts_with == "") or text.startswith(starts_with):
        return True
    return False


def _does_not_start_with_ok(text, does_not_start_with):
    """ This returns True if text does not start with the string (if any)
        in startsWith Else return False """
    if (does_not_start_with == "") or not text.startswith(does_not_start_with):
        return True
    return False


def _strip_aat(text):
    return_text = ''
    text_array = text.split(':')
    if text_array:
        return_text = text_array[len(text_array) - 1]
    return return_text


class GetEmbarkField(object):
    """ Class does heavy lifting translating XML to JSON """

    def __init__(self, field_definition):
        """ Initialize fields_definition only once for local use later """
        self.result_json = {}
        self.field_definition = field_definition
        self.error = []
        self.output = {}
        self.field = {}
        self.field['name'] = get_field_name(field_definition)
        self.field['required'] = get_field_required(field_definition)
        self.field['duplicates_allowed'] = get_field_duplicates_allowed(
            field_definition)
        self.field['xpath'] = get_field_xpath(field_definition)
        self.field['default'] = get_field_default(field_definition)
        self.field['does_not_start_with'] = get_does_not_start_with(
            field_definition)
        self.field['starts_with'] = get_starts_with(field_definition)
        self.field['validation'] = get_validation_rule(field_definition)
        self.field['constant'] = get_constant(field_definition)

    def load_json_field_definition(self, field_definition):
        """ This allows the user to move to pass a new field definition """
        self.__init__(field_definition)

    def get_json_representation_of_field(self, embark_item_xml):
        """ This retrieves an individual field (possibly as an array)
            from EmbArk XML and saves to JSON """
        json_for_this_field = {}
        try:
            if self.field['constant'] > "":
                # Use this for "repository", which doesn't exist in XML
                json_for_this_field[self.field['name']] = self.field['constant']
            elif self.field['name'] == 'exhibition':
                # exhibitions have highly unusual XML format
                json_for_this_field = self._get_exhibition_information(embark_item_xml)
            else:
                json_for_this_field = self._get_node(embark_item_xml)
            if json_for_this_field == {} and self.field['default'] > "":
                json_for_this_field[self.field['name']] = self.field['default']
            if json_for_this_field == {} and self.field['required']:
                error_text = 'Required field ' + self.field['name'] + ' is missing.    Unable to process record '
                raise ValueError(error_text)
        except ValueError:
            # print('get_json_represetation_of_field encountered an error.')
            json_for_this_field = {}
            raise
        return json_for_this_field

    def _get_node(self, embark_item_xml):
        """ This retrieves an individual value (or array) from XML
            , optionally validates it, and saves to JSON """
        node = {}
        for item in embark_item_xml.findall(self.field['xpath']):
            this_item = {}
            value_found = ""
            if _starts_with_ok(item.text, self.field['starts_with']) \
                    and _does_not_start_with_ok(item.text, self.field['does_not_start_with']):
                value_found = item.text
            if self.field['validation'] == 'validateYYYYMMDD' and value_found > '':
                value_found = get_valid_yyyymmdd_date(value_found)
            if isinstance(value_found, str) and value_found > '' and value_found.startswith('AAT:'):
                value_found = _strip_aat(value_found)
            if self.field['duplicates_allowed']:
                this_item["value"] = value_found
                if self.field['name'] not in node:
                    node[self.field['name']] = []
                node[self.field['name']].append(this_item)
            else:
                if value_found is not None:
                    this_item[self.field['name']] = value_found
                    node = this_item
                break  # if duplicates are not allowed, only accept first item
        return node

    def _get_exhibition_information(self, embark_item_xml):
        """ This accommodates the special Exhibitions data format """
        # Note:  Temporary until we get better Embark exhibition information
        exhibition_node = {}
        exhibition_node[self.field['name']] = []
        exhibition_iterator = -1
        for item in embark_item_xml.findall(self.field['xpath']):
            this_item = {}
            exhibition_iterator += 1
            this_item["name"] = item.text  # Capture the name of the exhibit
            date_group_iterator = -1
            for start_date_group in embark_item_xml.findall('./group[@id=\'object_00001\']'):
                date_group_iterator += 1
                individual_date_iterator = -1
                if date_group_iterator == 0:  # start_date
                    for start_date in start_date_group.findall('./variable[@id=\'object_00001\']'):
                        individual_date_iterator += 1
                        if individual_date_iterator == exhibition_iterator:
                            this_item["startDate"] = start_date.text
                else:  # EndDate is the second occurance of Start_Date node.)
                    for end_date in start_date_group.findall('./variable[@id=\'object_00001\']'):
                        individual_date_iterator += 1
                        if individual_date_iterator == exhibition_iterator:
                            this_item["endDate"] = end_date.text
            exhibition_node[self.field['name']].append(this_item)
        return exhibition_node
