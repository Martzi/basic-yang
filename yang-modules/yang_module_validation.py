import lxml.etree as ET
import xmltodict
import os
import json
from pyangbind.lib.serialise import pybindJSONDecoder
from bindings import application_layer, device_layer, network_layer, ietf_network_topology, ietf_network
from pyangbind.lib.pybindJSON import dumps

def validate_xml_with_yang(xml_instance_data):
    try:
        xml_doc = ET.parse(xml_instance_data)
        print("XML instance data is well-formed.")
    except ET.XMLSyntaxError as e:
        print(f"XML Syntax Error: {e}")
        return False

    # Convert XML to JSON
    xml_root = xml_doc.getroot()
    print("xml_root: ", xml_root)
    xml_str = ET.tostring(xml_root, encoding='unicode')
    print("xml_str: ", xml_str)
    xml_dict = xmltodict.parse(xml_str)
    # xml_dict = json.loads(json.dumps(ET.fromstring(xml_str)))
    print("xml_dict: ", xml_dict)
    json_data = json.dumps(xml_dict, indent=2)
    print("json_data: ", json_data)

    # Validate against YANG models
    models = [ietf_network(), device_layer(), network_layer(), ietf_network_topology(), ietf_network(), application_layer()]
    for model in models:
        print("model: ", model)
        try:
            pybindJSONDecoder.load_ietf_json(xml_dict, None, None, obj=model)
            print(f"Validation against {model} successful.")
        except Exception as e:
            print(f"Validation against {model} failed: {e}")
            return False

    print("Validation logic implemented.")
    return True

if __name__ == "__main__":
    # Path to the XML instance data file
    xml_instance_data = "instance-data.xml"

    # Perform validation
    is_valid = validate_xml_with_yang(xml_instance_data)
    if is_valid:
        print("The XML instance data is valid according to the YANG models.")
    else:
        print("The XML instance data is not valid according to the YANG models.")