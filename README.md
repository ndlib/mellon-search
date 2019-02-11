# mellon-search
This translates a referenced EmbArk XML file, possibly containing many EmbArk items,
    into a separate JSON file for each item.
Each JSON file is then used to create a PNX record to be imported into Primo.

To invoke, pass in the filename to be processed.  For example:
python3 -c 'from createJsonItemFromEbmArkXml import *; createJsonItemFromEbmArkXml("example/objects 01_18_19.xml")'


Modules:
createJsonItemFromEbmArkXml is the highest level module.

getEmbarkXmlDefinitions calls get_json_values

get_json_values
    This module deals with extracting a JSON value from a JSON variable.
        If a value is required, it must exist and must not be blank.
        If an error is encountered, we raise a ValueError.
