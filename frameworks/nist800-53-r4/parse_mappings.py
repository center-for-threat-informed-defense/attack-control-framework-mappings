import stix2
from tqdm import tqdm
import requests
import pandas as pd
import re
import itertools
import json
import os

def dict_regex_lookup(thedict, regexstr):
    """return all values in the dict where the key matches the regex. Params are the dict, and a string to be used as regex"""
    # add anchor characters if they're not explicitly specified to prevent T1001 from matching T1001.001
    if not regexstr.endswith("$"): regexstr = regexstr + "$"
    if not regexstr.startswith("^"): regexstr = "^" + regexstr
    try:
        regex = re.compile(regexstr)
    except Exception as err: 
        print("cannot compile regex", regexstr, "because of", err)
        exit()
    values = []
    for key in thedict:
        if regex.match(key): values.append(thedict[key])
    return values

def parse_mappings(mappingspath, controls, relationship_ids={}):
    """parse the NIST800-53 revision 4 mappings and return a STIX bundle 
    of relationships mapping the controls to ATT&CK
    :param mappingspath the filepath to the mappings TSV file
    :param controls a stix2.Bundle represneting the controls framework
    :param relationship_ids is a dict of format {relationship-source-id---relationship-target-id: relationship-id} which maps relationships to desired STIX IDs
    """

    print("reading framework config...", end="", flush=True)
    # load the mapping config
    with open(os.path.join("data", "config.json"), "r") as f:
        config = json.load(f)
        version = config["attack_version"]
        domain = config["attack_domain"]
    print("done")

    tqdmformat = "{desc}: {percentage:3.0f}% |{bar}| {elapsed}<{remaining}{postfix}"

    # load ATT&CK STIX data
    print("downloading ATT&CK data... ", end="", flush=True)
    attackdata = requests.get(f"https://raw.githubusercontent.com/mitre/cti/ATT%26CK-{version}/{domain}/{domain}.json", verify=False).json()["objects"]
    print("done")

    # build mapping of attack ID to stixID
    attackID_to_stixID = {}
    for attackobject in tqdm(attackdata, desc="parsing ATT&CK data", bar_format=tqdmformat):
        if not attackobject["type"] == "relationship":
            # skip objects without IDs
            if not "external_references" in attackobject: continue
            # skip deprecated and revoked objects
            if "revoked" in attackobject and attackobject["revoked"]: continue
            if "x_mitre_deprecated" in attackobject and attackobject["x_mitre_deprecated"]: continue
            # map attackID to stixID
            attackID_to_stixID[attackobject["external_references"][0]["external_id"]] = attackobject["id"]
    
    # build mapping of control ID to stixID
    controlID_to_stixID = {}
    for sdo in tqdm(controls.objects, desc="parsing controls", bar_format=tqdmformat):
        if sdo.type == "course-of-action": # only do mitigations
            controlID_to_stixID[sdo["external_references"][0]["external_id"]] = sdo["id"]

    # build mapping relationships
    relationships = []
    mappings_df = pd.read_csv(mappingspath, sep="\t", keep_default_na=False, header=0)
    for index, row in tqdm(list(mappings_df.iterrows()), desc="parsing mappings", bar_format=tqdmformat):
        # create list of control STIX IDs matching this row
        fromIDs = dict_regex_lookup(controlID_to_stixID, row["controlID"])
        # create list of technique STIX IDs matching this row
        toIDs = dict_regex_lookup(attackID_to_stixID, row["techniqueID"])
        # only have a description if the row does
        description = row["description"] if row["description"] else None
        
        if not fromIDs:
            print("error looking up controlID", row["controlID"])
        if not toIDs:
            print("error looking up techniqueID", row["techniqueID"])
        if not fromIDs or not toIDs:
            exit()

        # combinatorics of every from to every to
        for fromID in fromIDs:
            for toID in toIDs:
                joined_id = f"{fromID}---{toID}"
                # build the mapping relationship
                relationships.append(stix2.Relationship(
                    id=relationship_ids[joined_id] if joined_id in relationship_ids else None,
                    source_ref=fromID,
                    target_ref=toID,
                    relationship_type="mitigates",
                    description=description
                ))

    # construct and return the bundle of relationships
    return stix2.Bundle(relationships, spec_version="2.0")