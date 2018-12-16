import configparser
import os

config = configparser.ConfigParser()
CUR_PATH = os.path.dirname(os.path.realpath(__file__))
config.read(os.path.join(CUR_PATH, "properties.ini"))
