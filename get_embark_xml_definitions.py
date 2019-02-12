#get_embark_xml_definitions.py 2/4/19 sm
''' This module pulls the definition of EmbArk XML fields from a passed JSON variable.
    Here is an example of a valid JSON variable:
    {
    	"itemPath": "./Section[@name='Body'][@id='section_07']",
    	"FieldsToExtract": [
    		{
    			"name": "recordId",
    			"required": true,
    			"duplicatesAllowed": false,
    			"xpath": "./variable[@id='object_00055']"
    		},
    		{
    			"name": "creator",
    			"required": false,
    			"duplicatesAllowed": false,
    			"xpath": "./variable[@id='object_00060']"
    		},
    		{
    			"name": "title",
    			"required": true,
    			"duplicatesAllowed": false,
    			"xpath": "./variable[@id='object_00056']"
    		},
    		{
    			"name": "bibliography",
    			"required": false,
    			"duplicatesAllowed": true,
    			"xpath": "./group[@id='object_00003']/variable[@id='object_00003']"
    		},
    		{
    			"name": "keyword",
    			"required": false,
    			"duplicatesAllowed": true,
    			"xpath": "./group[@id='object_00080']/variable[@id='object_00080']",
    			"doesNotStartWith": "AAT:"
    		},
    		{
    			"name": "facet",
    			"required": false,
    			"duplicatesAllowed": true,
    			"xpath": "./group[@id='object_00080']/variable[@id='object_00080']",
    			"startsWith": "AAT:"
    		}
    	]
    }
    ############################ Module documentation ends here ####################################
    '''

import json
import get_json_values


def get_item_xpath(embark_field_definitions):
    ''' Return Item XPath defining Item location in EmbArk XML '''
    return get_json_values.get_json_value(embark_field_definitions, 'itemPath')

def get_fields_definition(embark_field_definitions):
    ''' Return Field Definitions from embark_xml_fields.json '''
    return get_json_values.get_json_value(embark_field_definitions, 'FieldsToExtract')

def get_field_name(embark_field_definition):
    ''' Return name of field '''
    return get_json_values.get_json_value(embark_field_definition, 'name')

def get_field_required(embark_field_definition):
    ''' Return boolean whether field is required or not '''
    return get_json_values.get_json_value(embark_field_definition, 'required')

def get_field_duplicates_allowed(embark_field_definition):
    ''' Return boolean whether duplicates are allowed '''
    return get_json_values.get_json_value(embark_field_definition, 'duplicatesAllowed')

def get_field_xpath(embark_field_definition):
    ''' Return the xpath where we can find this field in EmbArk xml '''
    return get_json_values.get_json_value(embark_field_definition, 'xpath')

def get_does_not_start_with(embark_field_definition):
    ''' Returns string to test Does Not Start With '''
    return get_json_values.get_json_value(embark_field_definition, 'doesNotStartWith', False)

def get_starts_with(embark_field_definition):
    ''' Returns string to test Starts With '''
    return get_json_values.get_json_value(embark_field_definition, 'startsWith', False)

def get_validation_rule(embark_field_definition):
    ''' Returns type of Validation to enforce '''
    return get_json_values.get_json_value(embark_field_definition, 'validation', False)

def get_constant(embark_field_definition):
    ''' Returns constant to include in JSON output (e.g. Repository) '''
    return get_json_values.get_json_value(embark_field_definition, 'constant', False)

#tests
# python3 -c 'from get_embark_xml_definitions import *; test()'

def test():
    ''' Run tests '''
    try:
        _test_get_item_xpath()
        _test_get_fields_definition()
        _test_get_field_name()
        _test_get_field_required()
        _test_get_field_duplicates_allowed()
        _test_get_field_xpath()
        _test_get_does_not_start_with()
        _test_get_starts_with()
        _test_get_validation_rule()
        _test_get_constant()
        print('All tests ran successfully.')
    except:
        print('At least one test failed.')
        raise

def _test_get_item_xpath():
    '''test retrieving known item xpath'''
    original_path = '{"itemPath": "./Section[@name=\'Body\'][@id=\'section_07\']",	"FieldsToExtract": []}'
    embark_field_definitions = json.loads(original_path)
    item_xpath = get_item_xpath(embark_field_definitions)
    assert item_xpath == embark_field_definitions['itemPath']

def _test_get_fields_definition():
    ''' test retrieving known fields definition '''
    embark_field_definitions = json.loads('{"xitemPath": "./Section[@name=\'Body\'][@id=\'section_07\']",	"FieldsToExtract": [{"name": "recordId", "required": true, "duplicatesAllowed": false, "xpath": "./variable[@id=\'object_00055\']"}]}')
    fields_definitions = get_fields_definition(embark_field_definitions)
    assert fields_definitions == embark_field_definitions['FieldsToExtract']

def _test_get_field_name():
    ''' test retrieving known field name '''
    embark_field_definition = json.loads('{"name": "recordId", "required": true, "duplicatesAllowed": false, "xpath": "./variable[@id=\'object_00055\']"}')
    name = get_field_name(embark_field_definition)
    assert name == embark_field_definition['name']

def _test_get_field_required():
    ''' test retrieving known field required '''
    embark_field_definition = json.loads('{"name": "recordId", "required": true, "duplicatesAllowed": false, "xpath": "./variable[@id=\'object_00055\']"}')
    required = get_field_required(embark_field_definition)
    assert required == embark_field_definition['required']
    assert required

def _test_get_field_duplicates_allowed():
    ''' test retrieving known Duplicates Allowed '''
    embark_field_definition = json.loads('{"name": "recordId", "required": true, "duplicatesAllowed": false, "xpath": "./variable[@id=\'object_00055\']"}')
    duplicates_allowed = get_field_duplicates_allowed(embark_field_definition)
    assert duplicates_allowed == embark_field_definition['duplicatesAllowed']
    assert not duplicates_allowed

def _test_get_field_xpath():
    ''' test retrieving known field xpath '''
    embark_field_definition = json.loads('{"name": "recordId", "required": true, "duplicatesAllowed": false, "xpath": "./variable[@id=\'object_00055\']"}')
    xpath = get_field_xpath(embark_field_definition)
    assert xpath == embark_field_definition['xpath']

def _test_get_does_not_start_with():
    ''' test retrieving known Does Not Start With '''
    embark_field_definition = json.loads('{"duplicatesAllowed": false, "xpath": "./variable[@id=\'object_00055\']","doesNotStartWith": "AAT:" }')
    does_not_start_with = get_does_not_start_with(embark_field_definition)
    assert does_not_start_with == embark_field_definition['doesNotStartWith']
    assert does_not_start_with == "AAT:"

def _test_get_starts_with():
    ''' test retrieving known Starts With '''
    embark_field_definition = json.loads('{"required": true, "duplicatesAllowed": false, "xpath": "./variable[@id=\'object_00055\']","startsWith": "AAT:" }')
    starts_with = get_starts_with(embark_field_definition)
    assert starts_with == embark_field_definition['startsWith']
    assert starts_with == "AAT:"

def _test_get_validation_rule():
    ''' test retrieving known Validation rule '''
    embark_field_definition = json.loads('{"required": true, "duplicatesAllowed": false, "xpath": "","constant": "Snite","validation":"validateYYYYMMDD" }')
    validation = get_validation_rule(embark_field_definition)
    assert validation == embark_field_definition['validation']

def _test_get_constant():
    ''' test retrieving known Constant '''
    embark_field_definition = json.loads('{"required": true, "duplicatesAllowed": false, "xpath": "","constant": "Snite","validation":"validateYYYYMMDD" }')
    constant = get_constant(embark_field_definition)
    assert constant == embark_field_definition['constant']
