# write_main_csv.py 2/15/19 sm
""" Write main.csv as starting point for Mellon Manifest Pipeline """

import os
import csv


def write_main_csv(csv_directory, json_data):
    """ write main.csv """
    csv_filename = 'main.csv'
    create_directory(csv_directory)
    with open(csv_directory + '/' + csv_filename, 'w') as main_csv:
        fieldnames = ['Label', 'Description', 'License', 'Attribution',
                      'Sequence_filename', 'Sequence_label',
                      'Sequence_viewing_experience', 'unique_identifier',
                      'Metadata_label', 'Metadata_value']
        writer = csv.DictWriter(main_csv, fieldnames=fieldnames, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerow(_create_first_row(json_data))
        writer.writerows(_create_metadata_rows(json_data))
    main_csv.close()


def _create_first_row(json_data):
    """ create values for first row of main.csv """
    usage_license = '<a href="http://rightsstatements.org/vocab/NoC-US/1.0/"' \
        + ' target="_blank">No Copyright - United States</a>'
    attribution = 'University of Notre Dame::Hesburgh Libraries::General'
    row = {}
    row['Label'] = json_data['title']
    row['Description'] = json_data['title']
    row['License'] = usage_license
    row['Attribution'] = attribution
    row['Sequence_filename'] = ''
    row['Sequence_label'] = 'Sequence1'
    row['Sequence_viewing_experience'] = 'individuals'
    row['unique_identifier'] = json_data['recordId']
    return row


def _create_metadata_rows(json_data):
    """ write metadata rows to main.csv """
    rows = {}
    rows = []
    rows.append(_create_metadata_row(json_data, 'recordId',
                                     'Accession Number'))
    rows.append(_create_metadata_row(json_data, 'repository', 'Repository'))
    rows.append(_create_metadata_row(json_data, 'creator', 'Creator'))
    rows.append(_create_metadata_row(json_data, 'creationDate',
                                     'Creation Date'))
    rows.append(_create_metadata_row(json_data, 'displayDate',
                                     'Display Date'))
    rows.append(_create_metadata_row(json_data, 'title', 'Title'))
    rows.append(_create_metadata_row(json_data, 'classification',
                                     'Classification'))
    rows.append(_create_metadata_row(json_data, 'media', 'Media'))
    rows.append(_create_metadata_row(json_data, 'displayDimensions',
                                     'Dimensions'))
    rows.append(_create_exhibition_metadata_row(json_data, 'exhibition',
                                                'Exhibition'))
    rows.append(_create_metadata_array_row(json_data, 'relatedObjects',
                                           'Related Objects'))
    rows.append(_create_metadata_array_row(json_data, 'bibliography',
                                           'Bibliography'))
    rows.append(_create_metadata_array_row(json_data, 'keyword', 'Key words'))
    return rows


def _create_metadata_array_row(json_data, node_name, metadata_label):
    """ create records for metadata that can occur multiple times """
    metadata_value = ""
    row = {}
    if node_name in json_data:
        for node in json_data[node_name]:
            metadata_value = metadata_value + node['value'] + '\n'
        if metadata_value > "":
            row = _create_metadata_row_from_string(metadata_label,
                                                   metadata_value)
    return row


def _create_exhibition_metadata_row(json_data, node_name, metadata_label):
    """ create exhibition records for metadata """
    metadata_value = ""
    row = {}
    if node_name in json_data:
        for node in json_data[node_name]:
            metadata_value = metadata_value + node['name'] + '(' \
                + node['startDate'] + ' - ' + node['endDate'] + ')\n'
        if metadata_value > "":
            row = _create_metadata_row_from_string(metadata_label,
                                                   metadata_value)
    return row


def _create_metadata_row_from_string(element_label, element_string):
    """ create row of metadata to write """
    row = {}
    row['Metadata_label'] = element_label
    row['Metadata_value'] = element_string
    return row


def _create_metadata_row(json_data, node_name, metadata_label):
    """ create row of metadata to write """
    row = {}
    if node_name in json_data:
        row['Metadata_label'] = metadata_label
        row['Metadata_value'] = json_data[node_name]
    return row


def create_directory(directory):
    """ create directory if it does not exist """
    if not os.path.exists(directory):
        os.makedirs(directory)
