import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch_ros.actions import Node

import xacro


def load_file(package_name, file_path):
    package_path = get_package_share_directory(package_name)
    absolute_file_path = os.path.join(package_path, file_path)
    try:
        with open(absolute_file_path, 'r') as file:
            return file.read()
    except EnvironmentError:
        # parent of IOError, OSError *and* WindowsError where available
        return None


def generate_launch_description():
    # moveit_cpp.yaml is passed by filename for now since it's node specific
    # rrbot_gazebo = os.path.join(
    #     get_package_share_directory('example_config'),
    #     'config',
    #     'example_config_connections.sdf')

    # print(rrbot_gazebo)


    config_description_path = os.path.join(
        get_package_share_directory('example_config'))

    xacro_file = os.path.join(config_description_path,
                              'urdf',
                              'system_config.urdf.xacro')

    doc = xacro.parse(open(xacro_file))
    xacro.process_doc(doc)
    system_description_config = doc.toxml()
    robot_description = {'robot_description': system_description_config}

    robot_description_semantic_config = load_file('example_config',
                                                  os.path.join('config', 'example_config_connections.srdf'))
    robot_description_semantic = {'robot_description_semantic': robot_description_semantic_config}


    # RViz
    rviz_config_file = os.path.join(
        get_package_share_directory('example_config'), 'config', 'rviz_config.rviz')
    rviz_node = Node(package='rviz2',
                     executable='rviz2',
                     name='rviz2',
                     output='log',
                     arguments=['-d', rviz_config_file],
                     parameters=[robot_description,
                                 robot_description_semantic])

    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )

    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'rrbot'],
                        output='screen')

    # Static TF
    static_tf = Node(package='tf2_ros',
                     executable='static_transform_publisher',
                     name='static_transform_publisher',
                     output='log',
                     arguments=['0.0', '0.0', '0.0', '0.0', '0.0', '0.0', 'world', 'nuc_0_joint'])

    return LaunchDescription([
      node_robot_state_publisher,
    #   static_tf,
    #   spawn_entity,
      rviz_node
    ])