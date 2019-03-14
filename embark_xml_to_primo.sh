# embark_xml_to_primo.sh #2/15/19 sm
#!/bin/bash

# usage:  ./embark_xml_to_primo.sh "example/objects 01_18_19.xml"
echo "First arg: $1"
python3 create_json_items_from_embark_xml.py '$1'
./copy_pnx_to_Primo.sh
