#create_pnx_from_json.py 2/6/19 sm
""" This module will transform JSON input into PNX XML output for loading into Primo. """

import os
import xml.etree.ElementTree as ET

def _create_xml_element(element_name, element_text):
    ''' Create XML element including name and text '''
    record = ET.Element(element_name)
    if not element_text is None:
        if element_text > "":
            record.text = element_text
    return record


def _get_json_value(json_input, json_node):
    ''' Get value from Json node, returning empty string if node doesn't exist '''
    return_text = ""
    if json_node in json_input:
        return_text = json_input[json_node]
    return return_text

def _get_media_and_display(json_input):
    ''' Create element by concatenating Media and Display_Dimensions '''
    return_text = ""
    media = _get_json_value(json_input, 'media')
    display_dimensions = _get_json_value(json_input, 'displayDimensions')
    if media > "" and display_dimensions > "":
        return_text = media + ', ' + display_dimensions
    elif media > "":
        return_text = media
    elif display_dimensions > "":
        return_text = display_dimensions
    return return_text


def _get_exhibition(json_input):
    ''' Create element by concatenating exhibition name and dates '''
    return_text = ""
    name = _get_json_value(json_input, 'name')
    start_date = _get_json_value(json_input, 'startDate')
    end_date = _get_json_value(json_input, 'endDate')
    return_text = name
    if start_date > "":
        return_text = return_text + ' (' + start_date + ' - '
        if end_date > "":
            return_text = return_text + end_date
        return_text = return_text + ')'
    return return_text


def _create_display_section(json_input):
    ''' Create Display Section of Primo Record '''
    display = ET.Element("display")
    display.append(_create_xml_element('lds02', _get_json_value(json_input, 'recordId')))
    display.append(_create_xml_element('title', _get_json_value(json_input, 'title')))
    display.append(_create_xml_element('creator', _get_json_value(json_input, 'creator')))
    display.append(_create_xml_element('creationdate', _get_json_value(json_input, 'displayDate')))
    display.append(_create_xml_element('format', _get_media_and_display(json_input)))
    display.append(_create_xml_element('lds09', _get_json_value(json_input, 'classification').lower())) #Lower
    display.append(_create_xml_element('type', _get_json_value(json_input, 'classification').lower())) #Lower
    display.append(_create_xml_element('lsd10', _get_json_value(json_input, 'repository').title())) #Mixed case
    if 'keyword' in json_input:
        for keyword in json_input['keyword']:
            ET.SubElement(display, 'subject').text = keyword['value']
    if 'bibliography' in json_input:
        for bibliography in json_input['bibliography']:
            if bibliography['value'] > "":
                ET.SubElement(display, 'lds01').text = bibliography['value']
    if 'exhibition' in json_input:
        for exhibition_json in json_input['exhibition']:
            if 'name' in exhibition_json:
                display.append(_create_xml_element('contributor', _get_exhibition(exhibition_json)))
    return display

def _create_search_section(json_input):
    ''' Create Search Section of Primo Record '''
    search = ET.Element("search")
    search.append(_create_xml_element('recordid', _get_json_value(json_input, 'recordId')))
    search.append(_create_xml_element('title', _get_json_value(json_input, 'title')))
    search.append(_create_xml_element('creator', _get_json_value(json_input, 'creator')))
    search.append(_create_xml_element('creationdate', _get_json_value(json_input, 'creationDate')))
    search.append(_create_xml_element('general', _get_media_and_display(json_input)))
    search.append(_create_xml_element('lsr09', _get_json_value(json_input, 'classification').lower())) #Lower
    search.append(_create_xml_element('rsrctype', _get_json_value(json_input, 'classification').lower())) #Lower
    search.append(_create_xml_element('scope', _get_json_value(json_input, 'repository').upper())) #Upper
    if 'keyword' in json_input:
        for keyword in json_input['keyword']:
            ET.SubElement(search, 'subject').text = keyword['value']
    if 'exhibition' in json_input:
        for exhibition_json in json_input['exhibition']:
            if 'name' in exhibition_json:
                search.append(_create_xml_element('creatorcontrib', _get_exhibition(exhibition_json)))
    return search


def _create_browse_section(json_input):
    ''' Create Browse Section of Primo Record '''
    browse = ET.Element("browse")
    browse.append(_create_xml_element('title', _get_json_value(json_input, 'title')))
    browse.append(_create_xml_element('author', _get_json_value(json_input, 'creator')))
    browse.append(_create_xml_element('institution', _get_json_value(json_input, 'repository').upper())) #Upper
    return browse

def _create_sort_section(json_input):
    ''' Create Sort Section of Primo Record '''
    sort = ET.Element("sort")
    sort.append(_create_xml_element('title', _get_json_value(json_input, 'title')))
    sort.append(_create_xml_element('author', _get_json_value(json_input, 'creator')))
    sort.append(_create_xml_element('creationdate', _get_json_value(json_input, 'creationDate')))
    return sort

def _create_facet_section(json_input):
    ''' Create Facet Section of Primo Record '''
    facet = ET.Element("facet")
    facet.append(_create_xml_element('creatorcontrib', _get_json_value(json_input, 'creator')))
    facet.append(_create_xml_element('lfc09', _get_json_value(json_input, 'classification').lower())) #Lower
    facet.append(_create_xml_element('rsrctype', _get_json_value(json_input, 'classification').lower())) #Lower
    facet.append(_create_xml_element('library', _get_json_value(json_input, 'repository').upper())) #Upper
    facet.append(_create_xml_element('creationdate', _get_json_value(json_input, 'creationDate')))
    if 'keyword' in json_input:
        for keyword in json_input['keyword']:
            ET.SubElement(facet, 'topic').text = keyword['value']
    return facet

def _create_delivery_section(json_input):
    ''' Create Delivery Section of Primo Record '''
    delivery = ET.Element("delivery")
    delivery.append(_create_xml_element('delcategory', 'Physical Item'))
    delivery.append(_create_xml_element('institution', _get_json_value(json_input, 'repository').upper())) #Upper
    return delivery

def create_pnx_from_json(json_input):
    ''' Create PNX Record for Primo '''
    root = ET.Element("records")
    record = ET.Element("record")
    record.attrib["xmlns"] = "http://www.exlibrisgroup.com/xsd/primo/primo_nm_bib"
    record.attrib["xmlns:sear"] = "http://www.exlibrisgroup.com/xsd/jaguar/search"
    ET.SubElement(record, 'id').text = json_input['recordId']
    record.append(_create_display_section(json_input))
    record.append(_create_search_section(json_input))
    record.append(_create_browse_section(json_input))
    record.append(_create_sort_section(json_input))
    record.append(_create_facet_section(json_input))
    record.append(_create_delivery_section(json_input))
    root.append(record)
    root.tail = '\n' #make sure there is a new line character after the last node
    tree = ET.ElementTree(root)
    return tree

def write_pnx(pnx_directory, filename, xml_tree):
    ''' write pnx xml to file '''
    create_directory(pnx_directory)
    #note:  xml_delcaration and encoding is required to add the required declaration to the top of the XML file
    xml_tree.write(pnx_directory + '/' + filename,
                   xml_declaration=True,
                   encoding="utf-8",
                   method="xml"
                   )

def create_pnx_from_json_and_write_file(pnx_directory, json_input):
    ''' create pnx and write to file '''
    xml_tree = create_pnx_from_json(json_input)
    if pnx_directory == "":
        pnx_directory = 'pnx'
    filename = json_input['recordId'] + '.xml'
    write_pnx(pnx_directory, filename, xml_tree)
    return xml_tree # return only for testing purposes


def create_directory(directory):
    ''' create directory if it does not already exist '''
    try:
        os.makedirs(directory)
    except FileExistsError:
        # directory already exists
        pass
