# Purpose: Create a layer for MITRE's ATT&CK Navigator based on existing coverage of attack techniques.

# Resources
# https://mitre-attack.github.io/attack-navigator/
# https://github.com/mitre-attack/attack-scripts/blob/master/scripts/layers/samples/heatmap.py
# https://thispointer.com/python-read-csv-into-a-list-of-lists-or-tuples-or-dictionaries-import-csv-to-list/

# Steps/Components are
# 1. Have baselayer.json
# 2. have source.csv
# 3. run script against source.csv to make newlayer.json
# 4. Import newlayer.json and baselayer.json into ATT&CK Navigator
# 5. Use Create Layer from other layers 
#   domain: enterprise
#   score expresssion: a+b
#   gradient: base layer
#   coloring: new layer
#   states: base layer
#   filters: base layer
#   legend: base layer

# Sample techniques.csv:
# techniqueID,signatures
# T1595,1
# T1595.002,1
# T1133,2
# T1047,2
# T1542,2
# T1542.005,2
# T1021,1


import argparse
import csv
import json


def generate(csv_file):
    """parse the input csv file and return a layer dict with techniques with scores set to signature count"""
    # Create List of Dictionaries from CSV
    my_techniques = []

    from csv import DictReader
    # open file in read mode
    with open(csv_file, 'r', encoding='utf-8-sig') as csv:
        # pass the file object to DictReader() to get the DictReader object
        dict_reader = DictReader(csv)
        # get a list of dictionaries from dct_reader
        my_techniques = list(dict_reader)
        # print list of dict i.e. rows
        #for my_technique in my_techniques:
        #    print(my_technique)

    # parse techniques into layer format
    techniques_list = []
    for my_technique in my_techniques:
        techniques_list.append({
            "techniqueID": my_technique['techniqueID'],
            "score": int(my_technique['signatures']),
            "enabled": "true"
        })

    # return the techniques in a layer dict
    layer = {
        "name": "{}".format(csv_file),
        "versions": {
            "attack": "10",
            "navigator": "4.5.4",
            "layer": "4.2"
        },
        "domain": "enterprise-attack",
        "description": "Layer generated from {}".format(csv_file),
        "filters": {
            "platforms": [
                "Linux",
                "macOS",
                "Windows",
                "Azure AD",
                "Office 365",
                "SaaS",
                "IaaS",
                "Google Workspace",
                "PRE",
                "Network",
                "Containers"
            ]
        },
        "sorting": 3, # descending order of score
        "layout": {
            "layout": "side",
            "aggregateFunction": "average",
            "showID": "false",
            "showName": "true",
            "showAggregateScores": "false",
            "countUnscored": "false"
        },
        "hideDisabled": "true",
        "techniques": techniques_list,
        "gradient": {
            "colors": [
                "#8ec843",
                "#8ec843"
            ],
            "minValue": 0,
            "maxValue": 1000
        },
        "legendItems": [],
        "metadata": [],
        "showTacticRowBackground": "false",
        "tacticRowBackground": "#dddddd",
        "selectTechniquesAcrossTactics": "false",
        "selectSubtechniquesWithParent": "false"
    }

    
    # return the techniques in a layer dict
    return layer


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Generates a MITRE ATT&CK Navigator layer based on a CSV of \"techinqueID\" and count of \"signatures\"."
    )
    parser.add_argument("--input",
        type=str,
        default=None,
        required=True,
        help="Input csv filepath."
    )
    parser.add_argument("--output",
        type=str,
        default="layer.json",
        help="Output json filepath."
    )
    args = parser.parse_args()
    
    # get the layer
    layer = generate(args.input)    
    
    # write the layerfile
    with open(args.output, "w") as f:
        print("writing", args.output)
        f.write(json.dumps(layer, indent=4))
