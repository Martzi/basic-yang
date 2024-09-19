from rclpy.node import Node
from std_msgs.msg import String

import re
import rclpy
import subprocess
from lxml import etree
import xml.etree.ElementTree as ET

class instance_validator(Node):
    def __init__(self):
        super().__init__('urdf_validator_node')
        self.subscription = self.create_subscription(String, '/system_description', self.robot_description_callback, 10)
        self.get_logger().info("init done")
        return

    def yang_content_extract(self, robot_description):
        
        yang_xml_data = str()

        tree = etree.fromstring(robot_description)    
        etree.strip_tags(tree, etree.Comment)
        # urdf_nocomment = etree.tostring(tree)

        # parsed_xml = parseString(urdf_nocomment)
        # xml_pretty_str = parsed_xml.toprettyxml()

        # use first 2 lines (xml tag + namespaces) to start with
        # lines = xml_pretty_str.splitlines()
        # urdf_first_two_lines = ' '.join(lines[:2])

        # # load namespace into yang content to start with
        # yang_xml_data = urdf_first_two_lines ##### HA kell az első 2 sor
        # yang_xml_data = '<networks xmlns="urn:ietf:params:xml:ns:yang:ietf-network">'

        # Use a regular expression to find all content between <yang> and </yang> tags
        # matches = re.findall(r'<network>(.*?)</network>', robot_description, re.DOTALL)
        matches = re.findall(r'(<network\b[^>]*>.*?</network>)', robot_description, re.DOTALL)

        for match in matches:
            yang_xml_data = yang_xml_data + '' + match

        self.get_logger().info(f"robot_description: {robot_description}")

        remove_kinematics_pattern = r'<(link|joint)[^>]*>.*?</\1>'

        remove_robot_tags_pattern = r'</?robot[^>]*>'

        cleaned_content = re.sub(remove_kinematics_pattern, '', yang_xml_data, flags=re.DOTALL)
        cleaned_content = re.sub(remove_robot_tags_pattern, '', cleaned_content)
        # frame the content tags manually
        cleaned_content = '<?xml version="1.0" ?><networks xmlns="urn:ietf:params:xml:ns:yang:ietf-network">' + cleaned_content
        cleaned_content += '</networks>' # HA kell az első 2 sor akkor ez is 

        print(cleaned_content)
        return cleaned_content


    
    def write_to_file(self, data, filename):
        with open(filename, "w") as f:
            f.write(data)
        self.get_logger().info(f"is written to file: {filename}")

        return
    
    def robot_description_callback(self, msg):
        
        yang_xml_instance = "src/yang-modules/yang_content.xml"
        robot_description = msg.data  # self.get_logger().info(f"original robot description topic content: \n{robot_description}")
        yang_xml_data = str()
        yang_xml_data = self.yang_content_extract(robot_description)

        # register namespace! kell https://stackoverflow.com/questions/54439309/how-to-preserve-namespaces-when-parsing-xml-via-elementtree-in-python
        ET.register_namespace('al', 'urn:ietf:params:xml:ns:yang:application-layer')
        ET.register_namespace('nl', 'urn:ietf:params:xml:ns:yang:network-layer')
        ET.register_namespace('dl', 'urn:ietf:params:xml:ns:yang:device-layer')
        ET.register_namespace('nw', 'urn:ietf:params:xml:ns:yang:ietf-network')
        ET.register_namespace('nt', 'urn:ietf:params:xml:ns:yang:ietf-network-topology')
        ET.register_namespace('eth', 'urn:ietf:params:xml:ns:yang:ethernet-port')
        ET.register_namespace('usb', 'urn:ietf:params:xml:ns:yang:usb-port')

        xml_doc = ET.fromstring(yang_xml_data)

        tree = ET.ElementTree(xml_doc)
        ET.indent(tree, space='  ', level=0)
        tree.write(yang_xml_instance, encoding="utf-8")
        self.get_logger().info("YANG content of system model description is saved!")
        
        # yang validation with yanglint cli because python wrapper install failed
        command = [
            "yanglint", "-ii", "-t", "data", "-s", "-p", 
            "src/yang-modules/standard-modules/ietf-network-topology@2018-02-26.yang", 
            "src/yang-modules/standard-modules/ietf-network@2018-02-26.yang", 
            "src/yang-modules/topology/ethernet-port@2024-09-09.yang", 
            "src/yang-modules/topology/usb-port@2024-09-09.yang",
            "src/yang-modules/topology/device-layer@2024-09-10.yang",
            "src/yang-modules/topology/network-layer@2024-07-24.yang",
            "src/yang-modules/yang_content.xml"
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.stderr == '':
            self.get_logger().info("[yanglint] YANG instance data validation is successful!")
        else:
            self.get_logger().error(f"[yanglint] {result.stderr}")

        return

def main(args=None):
    rclpy.init(args=args)
    robot_description_subscriber = instance_validator()
    rclpy.spin(robot_description_subscriber)
    robot_description_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()