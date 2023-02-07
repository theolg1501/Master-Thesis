import numpy as np
import sys
from pathlib import Path
import click
import util
from collections import namedtuple
import pprint
from xml.etree import ElementTree as ET


def read(xml_file):
    """
        Parse the cameras.xml given a file name
        Args:
            xml_file (str): xml file path
        """
    xml = xml_file
    doc = ET.parse(xml_file)
    root = doc.getroot()
    for sensor in root.findall('./sensors/sensor'):
        print(sensor)

    return xml


read('doc.xml')
