# write_main_csv.py 2/15/19 sm

import os
import csv
import json

def write_main_csv(csv_directory, json_data):
    csv_filename = 'main.csv'
    create_directory(csv_directory)
    with open(csv_directory + '/' + csv_filename, 'w') as main_csv:
        fieldnames = ['Label', 'Description', 'Rights', 'Attribution', 'Sequence_filename', \
            'Sequence_label', 'Sequence_viewing_experience', 'unique_identifier', \
            'Metadata_label', 'Metadata_value']
        writer = csv.DictWriter(main_csv, fieldnames=fieldnames, delimiter=',', \
            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        _write_first_row(writer, json_data)
        _write_metadata_rows(writer, json_data)
    main_csv.close()

def _write_first_row(writer, json_data):
    row = {}
    row['Label'] = json_data['title']
    row['Description'] = json_data['title']
    row['Rights']= '' #note:  We need to have Rights defined
    row['Attribution'] = 'University of Notre Dame::Hesburgh Libraries::General'
    row['Sequence_filename'] = ''
    row['Sequence_label'] = 'Sequence1'
    row['Sequence_viewing_experience'] = 'individuals'
    row['unique_identifier'] = json_data['recordId']
    writer.writerow(row)


def _write_metadata_rows(writer, json_data):
    _create_metadata_row(writer, json_data, 'recordId', 'Accession Number')
    _create_metadata_row(writer, json_data, 'repository', 'Repository')
    _create_metadata_row(writer, json_data, 'creator', 'Creator')
    _create_metadata_row(writer, json_data, 'creationDate', 'Creation Date')
    _create_metadata_row(writer, json_data, 'displayDate', 'Display Date')
    _create_metadata_row(writer, json_data, 'title', 'Title')
    _create_metadata_row(writer, json_data, 'classification', 'Classification')
    _create_metadata_row(writer, json_data, 'media', 'Media')
    _create_metadata_row(writer, json_data, 'displayDimensions', 'Dimensions')
    _create_exhibition_metadata_row(writer, json_data, 'exhibition', 'Exhibition')
    _create_metadata_array_row(writer, json_data, 'relatedObjects', 'Related Objects')
    _create_metadata_array_row(writer, json_data, 'bibliography', 'Bibliography')
    _create_metadata_array_row(writer, json_data, 'keyword', 'Key words')


def _create_metadata_array_row(writer, json_data, node_name, metadata_label):
    metadata_value = ""
    if node_name in json_data:
        for node in json_data[node_name]:
            metadata_value = metadata_value + node['value'] + '\n'
        if metadata_value > "":
            _write_metadata_row(writer, metadata_label, metadata_value)

def _create_exhibition_metadata_row(writer, json_data, node_name, metadata_label):
    metadata_value = ""
    if node_name in json_data:
        for node in json_data[node_name]:
            metadata_value = metadata_value + node['name'] + '(' + node['startDate'] + ' - ' + node['endDate'] + ')\n'
        if metadata_value > "":
            _write_metadata_row(writer, metadata_label, metadata_value)


def _create_metadata_row(writer, json_data, node_name, metadata_label):
    if node_name in json_data:
        _write_metadata_row(writer, metadata_label, json_data[node_name])

def _write_metadata_row(writer, metadata_label, metadata_value):
    row = {}
    row['Metadata_label'] = metadata_label
    row['Metadata_value'] = metadata_value
    writer.writerow(row)

def create_directory(directory):
    try:
        os.makedirs(directory)
    except FileExistsError:
        # directory already exists
        pass


# python3 -c 'from write_main_csv import *; test("mellon_input_directory/1976.057/1976.057.json")'
def test(filename):
    ''' run test to create PNX record for a single item from a single JSON file '''
    try:
        with open(filename, 'r') as input_source:
            json_input = json.load(input_source)
        input_source.close()
    except IOError:
        print('Cannot open ' + filename)
        raise
    except:
        print(filename + ' does not contain valid JSON.')
        raise
    record_id = json_input['recordId']
    csv_directory = "mellon_input_directory/" + record_id
    csv_filename = 'main.csv'
    write_main_csv(csv_directory, json_input)
