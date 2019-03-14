# write_pnx_file.py
""" Write the PNX xml to disk """

from file_system_utilities import create_directory
# from xml.etree.ElementTree import ElementTree


def write_pnx_file(pnx_directory, filename, xml_tree):
    """ write pnx xml to file """
    #     tree = ET.ElementTree(root)
    create_directory(pnx_directory)
    xml_tree.write(pnx_directory + '/' + filename)
    # note:  xml_delcaration and encoding is not required.
    # Use following command to add the declaration to the top of the XML file
    #    xml_tree.write(
    #        pnx_directory + '/' + filename,
    #        xml_declaration=True,
    #        encoding="utf-8",
    #        method="xml")
