# parse_embark_xml.py 2/5/19 sm
"""Get data from EmbArk given JSON definitions."""

from get_individual_field_from_embark_xml import GetEmbarkField


class ParseEmbarkXml(object):
    """ Class does heavy lifting translating XML to JSON """
    def __init__(self, fields_definition):
        """ Initialize fields_definition only once for local use later """
        self.result_json = {}
        self.fields_definition = fields_definition
        self.id = ""
        self.output = {}

    def parse_embark_record(self, embark_item_xml):
        """ This translates information from EmbArk XML representing an
            individual museum item to JSON """
        fields_definition = self.fields_definition
        self.output = {}  # reset at beginning of each EmbArk Item
        node = {}
        for field in fields_definition:
            get_embark_field_instance = GetEmbarkField(field)
            node = get_embark_field_instance.get_json_representation_of_field(
                embark_item_xml)
            if 'recordId' in node:
                self.id = node['recordId']
            self.output.update(node)
        return self.output
