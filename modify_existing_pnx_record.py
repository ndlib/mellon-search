# modify_existing_pnx_record.py  3/7/19
""" Modifies existing pnx record to remove irrelevant info and replace repository  """

# import sys
import re
from xml.etree.ElementTree import ElementTree, Element, SubElement  # , tostring
from get_thumbnail_from_manifest import get_thumbnail_from_manifest


def _create_xml_element(element_name, element_text):
    """ Create XML element including name and text """
    record = Element(element_name)
    if element_text is not None:
        if element_text > "":
            record.text = element_text
    return record


def modify_existing_pnx_record(pnx_xml, repository, unique_identifier):
    """ Modifies PNX record for re-insertion for use by Mellon"""
    pnx_xml = _strip_control_section_from_pnx(pnx_xml)
    pnx_xml = _strip_dedup_section_from_pnx(pnx_xml)
    pnx_xml = _strip_frbr_section_from_pnx(pnx_xml)
    _add_repository_to_display(pnx_xml, repository)
    _add_repository_to_search(pnx_xml, repository)
    _add_repository_to_facet(pnx_xml, repository)
    _add_thumbnail_to_links(pnx_xml, unique_identifier)
    final_new_pnx_xml = _enclose_pnx_in_new_root_node(pnx_xml, unique_identifier)
    # print(tostring(final_new_pnx_xml.getroot()))
    return(final_new_pnx_xml)


def _add_repository_to_display(pnx_xml, repository):
    for display_section in pnx_xml.findall('display'):
        # remove existing nodes to be replaced
        # for lds10_section in display_section.findall('lds10'):
        #     display_section.remove(lds10_section)
        # add new node
        display_section.append(_create_xml_element('lds10', repository.title()))
    return


def _add_repository_to_search(pnx_xml, repository):
    # search_section = ElementTree.Element("search")
    for search_section in pnx_xml.findall('search'):
        # remove existing nodes to be replaced
        # for scope_node in search_section.findall('scope'):
        #     search_section.remove(scope_node)
        # for lsr01_node in search_section.findall('lsr01'):
        #     search_section.remove(lsr01_node)
        # add new nodes
        search_section.append(_create_xml_element('scope', repository.upper()))
        search_section.append(_create_xml_element('lsr01', repository.upper()))
    return


def _add_repository_to_facet(pnx_xml, repository):
    for facet_section in pnx_xml.findall('facet'):
        # remove existing nodes to be replaced
        # for library_section in facet_section.findall('library'):
        #     facet_section.remove(library_section)
        # add new node
        facet_section.append(_create_xml_element('library', repository.upper()))
    return


def _add_thumbnail_to_links(pnx_xml, unique_identifier):
    # for items currently stored in Primo under "ndu_aleph", translate prefix to "ils-" to find manifest
    unique_identifier = _correct_docid_for_manifest_search(unique_identifier)
    url = get_thumbnail_from_manifest(unique_identifier)
    if url > '':
        for links_section in pnx_xml.findall('links'):
            for thumbnail_section in links_section.findall('thumbnail'):
                if thumbnail_section.text.startswith('$$Uhttps://image-service'):
                    links_section.remove(thumbnail_section)  # if a thumbnail to the image server exists, remove it
            links_section.append(_create_xml_element('thumbnail', '$$U' + url))
    return


def _correct_docid_for_manifest_search(docid):
    """ Correct Doc ID based on patterns """
    # for items currently stored in Primo under ndu_aleph, manifest prefix is "ils-".
    docid = re.sub('ndu_aleph', 'ils-', docid)  # If "ndu_aleph" is supplied, translate to "ils-" to find Manifest
    return docid


def _strip_control_section_from_pnx(pnx_xml):
    """ We must strip the control section from a PNX record before re-inserting it """
    for control_section in pnx_xml.findall('control'):
        pnx_xml.remove(control_section)
    return(pnx_xml)


def _strip_dedup_section_from_pnx(pnx_xml):
    """ We must strip the dedup section from a PNX record before re-inserting it """
    for dedup_section in pnx_xml.findall('dedup'):
        pnx_xml.remove(dedup_section)
    return(pnx_xml)


def _strip_frbr_section_from_pnx(pnx_xml):
    """ We must strip the frbr section from a PNX record before re-inserting it """
    for frbr_section in pnx_xml.findall('frbr'):
        pnx_xml.remove(frbr_section)
    return(pnx_xml)


def get_unique_identifier_from_original_pnx(pnx_xml):
    unique_identifier = ""
    for control_section in pnx_xml.findall('control'):
        for recordid_node in control_section.findall('recordid'):
            unique_identifier = recordid_node.text
    if unique_identifier == '':
        for display_section in pnx_xml.findall('display'):
            for lds02_node in display_section.findall('lds02'):
                unique_identifier = lds02_node.text
    return unique_identifier


def _enclose_pnx_in_new_root_node(pnx_xml, unique_identifier):
    root = Element("records")
    SubElement(pnx_xml, 'id').text = unique_identifier
    root.append(pnx_xml)
    new_pnx_tree = ElementTree(root)
    return new_pnx_tree
