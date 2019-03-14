# recreate_pnx_record.py
""" Given an identifier, get a PNX record, modify it as needed, and output replacement """

import sys
from urllib import error
from get_existing_pnx_record import get_pnx_xml_given_docid  # , get_pnx_given_filename
from modify_existing_pnx_record import modify_existing_pnx_record, get_unique_identifier_from_original_pnx
from write_pnx_file import write_pnx_file
from file_system_utilities import create_directory


def recreate_pnx_record(primo_doc_id):
    """ Create a new PNX record given an existing PNX record """
    repository = 'snite'
    # pnx_xml = get_pnx_given_filename(pnx_filename)
    try:
        pnx_xml = get_pnx_xml_given_docid(primo_doc_id)
    except error.HTTPError:
        print('HTTPError encountered')
        pass  # if we didn't get a valid pnx entry, we can't do anything with it
    else:
        unique_identifier = get_unique_identifier_from_original_pnx(pnx_xml)
        # print('unique_identifier = ', unique_identifier)
        corrected_pnx_xml = modify_existing_pnx_record(pnx_xml, repository, unique_identifier)
        pnx_directory = 'pnx'
        create_directory(pnx_directory)
        write_pnx_file(pnx_directory, unique_identifier + '.xml', corrected_pnx_xml)


if __name__ == "__main__":
    primo_doc_id = ''
    if len(sys.argv) >= 1:
        primo_doc_id = ''.join(sys.argv[1])
    if primo_doc_id > '':
        recreate_pnx_record(primo_doc_id)
