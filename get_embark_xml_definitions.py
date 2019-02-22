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

def get_field_default(embark_field_definition):
    ''' Return the default value to use if value not present in EmbArk xml '''
    return get_json_values.get_json_value(embark_field_definition, 'default', False)

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
