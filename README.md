# mellon-search
This translates a referenced EmbArk XML file, possibly containing many EmbArk items,
    into a separate JSON file for each item.
Each JSON file is then used to create a PNX record to be imported into Primo.

To invoke, pass in the filename to be processed.  For example:
python3 -c 'from create_json_items_from_ebmark_xml import *; create_json_items_from_ebmark_xml("example/objects 01_18_19.xml")'


Modules:
create_json_items_from_ebmark_xml is the highest level module.

o - createJsonItemFromEmbArkXml
    This is the first module in a series of modules to create JSON (and PNX) given EmbArk input
    Calls: get_embark_xml_definitions
        read_embark_fields_json_file
        parse_embark_xml
        create_pnx_from_json

x - create_pnx_from_json.py
    This module will transform JSON input into PNX XML output for loading into Primo.

x - parse_embark_xml.py
    This module will accept JSON field definitions and will use those definitions to retrieve
        data from EmbArk XML passed.
    Calls: read_embark_fields_json_file
        get_valid_date

x - get_valid_date
    This module tries to clean up messy dates, returning a valid date string (not time) or nothing at all

x - read_embark_fields_json_file
    This module will read and validate the JSON that defines the EmbArk XML.
    Calls: get_embark_xml_definitions

x - get_embark_xml_definitions
    This module pulls the definition of EmbArk XML fields from a passed JSON variable.
    Calls: get_json_values

x - get_json_values
    This module deals with extracting a JSON value from a JSON variable.
        If a value is required, it must exist and must not be blank.
        If an error is encountered, we raise a ValueError.
