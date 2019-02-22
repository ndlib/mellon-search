# parse_embark_xml.py 2/5/19 sm
""" This module will accept JSON field definitions and will use those definitions to retrieve
    data from EmbArk XML (also passed). """

import get_individual_field_from_embark_xml

class ParseEmbarkXml():
    ''' Class does heavy lifting translating XML to JSON '''
    def __init__(self, fields_definition):
        ''' Initialize fields_definition only once for local use later '''
        self.result_json = {}
        self.fields_definition = fields_definition
        self.id = ""
        self.output = {}


    def parse_embark_record(self, embark_item_xml):
        ''' This translates information from EmbArk XML representing an
            individual museum item to JSON '''
        fields_definition = self.fields_definition
        self.output = {} # reinitialize output record at beginning of each EmbArk Item
        node = {}
        for field in fields_definition:
            get_embark_field_instance = get_individual_field_from_embark_xml.GetEmbarkField(field)
            node = get_embark_field_instance.get_json_representation_of_field(embark_item_xml)
            if 'recordId' in node:
                self.id = node['recordId']
            self.output.update(node)
        return self.output
