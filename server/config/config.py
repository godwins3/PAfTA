from configparser import ConfigParser
import os


def gmail_config(filename=os.path.dirname(os.path.abspath(__file__)) + '/files/config.ini', section='gmail'):
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)
    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db

def mongo_config(filename=os.path.dirname(os.path.abspath(__file__)) + '/files/config.ini', section='mongo'):
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db

def twilio_config(filename=os.path.dirname(os.path.abspath(__file__)) + '/files/config.ini', section='twilio'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db

from configparser import ConfigParser
import os
from datetime import datetime


def secret_config(filename=os.path.dirname(os.path.abspath(__file__)) + '/files/config.ini', section='tok'):
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:

        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db


def quickgen_secret_config(filename=os.path.dirname(os.path.abspath(__file__)) + '/files/config.ini', section='quickgen'):
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:

        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db


def client_id_config(filename=os.path.dirname(os.path.abspath(__file__)) + '/files/config.ini', section='google_client_id'):
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:

        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db

