#!/usr/bin/env python
#
# Data load and dump functions for different data types

import yaml
import json

class YamlData:
    def __init__(self):
        pass

    def dump_yaml(self, datastream):
        try:
            ydata = yaml.dump(datastream)
            return ydata
        except Exception as yamldumpfailed:
            print(f"YAML Dump failed:\n\t{yamldumpfailed}")
            return 0

    def load_yaml(self, datastream):
        try:
            ydata = yaml.load(datastream)
            return ydata
        except Exception as yamlloadfailed:
            print(f"YAML Load failed:\n\t{yamlloadfailed}")
            return 0

class JsonData:
    def __init__(self):
        pass

    def dump_json(self, datastream):
        try:
            jdata = json.dump(datastream)
            return jdata
        except Exception as jsondumpfail:
            print(f"JSON Dump failed:\n\t{jsondumpfail}")
            return 0

    def load_json(self, datastream):
        try:
            jdata = json.load(datastream)
            return jdata
        except Exception as jsonloadfail:
            print(f"JSON Load failed:\n\t{jsonloadfail}")
            return 0
