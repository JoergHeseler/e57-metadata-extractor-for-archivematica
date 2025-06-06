# Title: e57-metadata-extractor
# Version: 1.0.0
# Publisher: NFDI4Culture
# Publication date: May 15, 2025
# Author: Joerg Heseler
# License: CC BY-SA 4.0

import json
import os
import hashlib
from datetime import datetime
import platform
import subprocess
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom

def safe_cdata_chunks(text):
    """Zerlegt einen Text so, dass er sicher in CDATA-Abschnitten verwendet werden kann"""
    # CDATA end sequence: ]]>
    # To avoid this, we split the text at every point where this sequence occurs
  
    parts = text.split("]]>")
    chunks = []

    for i, part in enumerate(parts):
        chunks.append(('>' if i > 0 else '') + part + (']]' if i < len(parts) - 1 else ''))
        # print('PART', i, '------ : ', chunks[-1])

    return chunks

def get_e57xmldump_path_from_arguments():
    for arg in sys.argv:
        if arg.lower().startswith("--e57xmldump-path="):
            return arg.split("=", 1)[1].rstrip('/\\')
    return '/usr/share'

def get_target_file_name_from_arguments():
    for arg in sys.argv:
        if arg.startswith("--file-full-name="):
            return arg.split("=", 1)[1]
    return sys.argv[1]

def calculate_checksum(file_path, algorithm='sha256'):
    hash_func = hashlib.new(algorithm)
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            hash_func.update(chunk)
    return hash_func.hexdigest()

class E57ValidatorException(Exception):
    pass

def parse_e57xmldump_data(target):
    try:
        validator_file_path = get_e57xmldump_path_from_arguments() + os.sep + 'e57xmldump.exe'
        args = [validator_file_path, target]
        if platform.system() != 'Windows':
            args.insert(0, 'wine')
        return subprocess.check_output(args).decode("utf8")
    except FileNotFoundError:
        raise E57ValidatorException("e57xmldump not found. Use --e57xmldump-path= to specify its path.")
    except subprocess.CalledProcessError as e:
        return str(e.stdout)

def extract_e57_metadata(file_path):
    e57_output = parse_e57xmldump_data(file_path)
    e57_xml_output_root = ET.fromstring(e57_output)

    # File metadata
    file_size = os.path.getsize(file_path)
    creation_date = datetime.utcfromtimestamp(os.path.getctime(file_path)).isoformat()
    modification_date = datetime.utcfromtimestamp(os.path.getmtime(file_path)).isoformat()
    checksum = calculate_checksum(file_path)
    
    # Create XML tree with namespace and schema location
    ET.register_namespace('', "http://nfdi4culture.de/e57-metadata-extractor1") # Register default namespace
    root = ET.Element('E57MetadataExtractor', {
        'xmlns': "http://nfdi4culture.de/e57-metadata-extractor1",
        'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
        'xsi:schemaLocation': "http://nfdi4culture.de/e57-metadata-extractor1 https://raw.githubusercontent.com/JoergHeseler/e57-metadata-extractor-for-archivematica/refs/heads/main/src/e57-metadata-extractor.xsd"
    })

    # Create XML tree
    ns = {'e57':'http://www.astm.org/COMMIT/E57/2010-e57-v1.0'}
    ET.SubElement(root, 'formatName').text = 'E57 (' + e57_xml_output_root.find('e57:formatName', ns).text + ')' #'ASTM E57 3D Imaging Data File'
    version_minor = e57_xml_output_root.find('e57:versionMinor', ns)
    if version_minor.text is not None:
        version_minor = version_minor.text
    else:
        version_minor = '0'
    ET.SubElement(root, 'formatVersion').text = e57_xml_output_root.find('e57:versionMajor', ns).text + '.' + version_minor
    ET.SubElement(root, 'size').text = str(file_size)
    ET.SubElement(root, 'SHA256Checksum').text = checksum
    ET.SubElement(root, 'creationDate').text = creation_date
    ET.SubElement(root, 'modificationDate').text = modification_date
    ET.SubElement(root, 'library').text = e57_xml_output_root.find('e57:e57LibraryVersion', ns).text
    ET.SubElement(root, 'scanCount').text = str(len(e57_xml_output_root.find('e57:data3D', ns).findall('e57:vectorChild', ns)))
    total_points_count = 0
    for d3d in e57_xml_output_root.findall('e57:data3D', ns):
        for vc in d3d.findall('e57:vectorChild', ns):
            for p in vc.findall('e57:points', ns):
                total_points_count += int(p.attrib['recordCount'])
    has_colored_scans = False
    try:
        for d3d in e57_xml_output_root.findall('e57:data3D', ns):
            for vc in d3d.findall('e57:vectorChild', ns):
                for cl in vc.findall('e57:colorLimits', ns):
                    if (cl.find('e57:colorRedMinimum', ns).text != cl.find('e57:colorRedMaximum', ns).text) or (cl.find('e57:colorGreenMinimum', ns).text != cl.find('e57:colorGreenMaximum', ns).text) or (cl.find('e57:colorBlueMinimum', ns).text != cl.find('e57:colorBlueMaximum', ns).text):
                        has_colored_scans = True
    except AttributeError:
        pass
    ET.SubElement(root, 'hasColoredScans').text = 'true' if has_colored_scans else 'false'
    ET.SubElement(root, 'totalPointCount').text = str(total_points_count)
    ET.SubElement(root, 'imageCount').text = str(len(e57_xml_output_root.find('e57:images2D', ns)))
    
    # Convert ElementTree to minidom document for CDATA support
    xml_str = ET.tostring(root, encoding='utf-8')
    dom = minidom.parseString(xml_str)
    
    # Add CDATA section for rawE57ValidatorOutput
    raw_output = dom.createElement('rawE57XmlDumpOutput')
    for chunk in safe_cdata_chunks(e57_output.strip()):
        cdata_section = dom.createCDATASection(chunk)
        raw_output.appendChild(cdata_section)
    dom.documentElement.appendChild(raw_output)
    
    # Print formatted XML with CDATA
    print(dom.toprettyxml(indent="    "))


if __name__ == '__main__':
# Main
    target = get_target_file_name_from_arguments()
    if not target:
        print("No argument with --file-full-name= found.", file=sys.stderr)
    else:
        sys.exit(extract_e57_metadata(target))
