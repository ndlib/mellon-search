# get_existing_pnx_record.py  3/7/19
""" Retrieves xml of existing pnx record """

# import sys
import re
from urllib import request, error
from xml.etree.ElementTree import fromstring


def get_pnx_given_filename(pnx_filename="./sample.xml"):
    """ read pnx record as a string from a file """
    pnx_string = ""
    try:
        with open(pnx_filename, "r") as input_file:
            pnx_string = input_file.read()
    except FileNotFoundError:
        # print('File Not Found calling get_pnx_given_filename')
        raise
    pnx_as_xml = _convert_pnx_string_to_xml(pnx_string)
    return(pnx_as_xml)


def get_pnx_xml_given_docid(docid):
    """ Retrieves pnx xml given an existing unique docid."""
    # sample docid: ndu_aleph000909884 or ils-000909884
    # change url to here: https://a1fc3ld3d7.execute-api.us-east-1.amazonaws.com/dev/ then follow with   primo/v1...
    docid = _correct_docid_for_primo_search(docid)
    root_pnx_url = 'https://a1fc3ld3d7.execute-api.us-east-1.amazonaws.com/dev/'
    pnx_url = root_pnx_url + 'primo/v1/search/xml/L/' \
        + docid + '?lang=eng&adaptor=Local%20Search%20Engine&showPnx=true&inst=NDU' \
        + '&sandbox=1'  # force to use production server for search
    pnx_string = ""
    # print(pnxurl)
    try:
        pnx_string = request.urlopen(pnx_url).read()
        # print('pnx was read')
        pnx_string = pnx_string.decode("utf-8")  # convert from byte object to str
        # print('string was converted')
    except error.HTTPError:
        print('cannot retrieve xml from url in get_pnx_xml_given_docid ')
        raise
    pnx_as_xml = _convert_pnx_string_to_xml(pnx_string)
    return pnx_as_xml


def _correct_docid_for_primo_search(docid):
    """ Correct Doc ID based on patterns """
    # for items currently stored in Primo under ndu_aleph, manifest prefix is "ils-".
    docid = re.sub('ils-', 'ndu_aleph', docid)  # If "ils-" is supplied, translate to "ndu_aleph" to find in Primo
    return docid


def _convert_pnx_string_to_xml(pnx_string):
    pnx_string_without_namespace = _strip_namespace_from_pnx_string(pnx_string)
    pnx_string_without_newlines = _strip_newlines_from_pnx_string(pnx_string_without_namespace)
    pnx_as_xml = _convert_string_to_xml(pnx_string_without_newlines)
    return(pnx_as_xml)


def _strip_namespace_from_pnx_string(pnx_string):
    """ The original pnx record contains namespaces, which cause problems for ElementTree, so we must strip them """
    pnx_string_without_namespace = re.sub(' xmlns="[^"]+"', '', pnx_string)  # , count=2)
    return(pnx_string_without_namespace)


def _strip_newlines_from_pnx_string(pnx_string):
    """ The original pnx record contains "\n", which cause problems for ElementTree, so we must strip them """
    pnx_string_without_newlines = re.sub('\n', '', pnx_string)
    return(pnx_string_without_newlines)


def _convert_string_to_xml(pnx_string):
    """ Convert string to XML so we can manipulate it further. """
    pnx_as_xml = fromstring(pnx_string)
    return(pnx_as_xml)


# if __name__ == "__main__":
#     pnx_filename = ''
#     print(len(sys.argv))
#     if len(sys.argv) >= 1:
#         pnx_filename = ''.join(sys.argv[1])
#     if pnx_filename > '':
#         get_pnx_xml_given_docid(pnx_filename)
