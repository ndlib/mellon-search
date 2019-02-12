# mellon-search
This project translates a referenced EmbArk XML file, possibly containing many EmbArk items,
    into a separate JSON file for each item.

    Each JSON file is then used to create a PNX record to be imported into Primo.


To run, pass in the filename to be processed.  For example:
python3 -c 'from create_json_items_from_embark_xml import *; create_json_items_from_embark_xml("example/objects 01_18_19.xml")'



Modules:
createJsonItemFromEmbArkXml
    This is the first module in a series of modules to create JSON (and PNX) given EmbArk input
    Calls: get_embark_xml_definitions
        read_embark_fields_json_file
        parse_embark_xml
        create_pnx_from_json

create_pnx_from_json.py
    This module will transform JSON input into PNX XML output for loading into Primo.

parse_embark_xml.py
    This module will accept JSON field definitions and will use those definitions to retrieve
        data from EmbArk XML passed.
    Calls: read_embark_fields_json_file
        get_valid_date
        get_individual_field_from_embark_xml

get_individual_field_from_embark_xml
    This module will accept an individual JSON field definition and will use that definition to retrieve
        data from EmbArk XML (also passed).

get_valid_date
    This module tries to clean up messy dates, returning a valid date string (not time) or nothing at all

read_embark_fields_json_file
    This module will read and validate the JSON that defines the EmbArk XML.
    Calls: get_embark_xml_definitions

get_embark_xml_definitions
    This module pulls the definition of EmbArk XML fields from a passed JSON variable.
    Calls: get_json_values

get_json_values
    This module deals with extracting a JSON value from a JSON variable.
        If a value is required, it must exist and must not be blank.
        If an error is encountered, we raise a ValueError.
