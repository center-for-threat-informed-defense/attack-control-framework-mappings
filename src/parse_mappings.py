import re

from colorama import Fore
from stix2.v20 import Bundle, Relationship
from tqdm import tqdm
import pandas as pd


def dict_regex_lookup(the_dict, regex_str):
    """return all values in the dict where the key matches the regex.
    Params are the dict, and a string to be used as regex"""
    # add anchor characters if they're not explicitly specified to prevent T1001 from matching T1001.001
    regex_str = regex_str.strip()
    if not regex_str.endswith("$"):
        regex_str = regex_str + "$"
    if not regex_str.startswith("^"):
        regex_str = "^" + regex_str
    try:
        regex = re.compile(regex_str)
    except Exception as err:
        print(Fore.RED + "ERROR: cannot compile regex", regex_str, "because of", err, Fore.RESET)
        exit()
    values = []
    for key in the_dict:
        if regex.match(key):
            if "(" in key or ")" in key:
                continue
            values.append(the_dict[key])
    return values


def parse_mappings(mappings_path, controls, relationship_ids, attack_data):
    """parse the NIST800-53 revision 4 mappings and return a STIX bundle
    of relationships mapping the controls to ATT&CK

    :param mappings_path: the filepath to the mappings TSV file
    :param controls: a stix2.Bundle representing the controls framework
    :param relationship_ids: is a dict of format {relationship-source-id---relationship-target-id: relationship-id}
                             which maps relationships to desired STIX IDs
    :param attack_data: ATT&CK content
    """
    tqdm_format = "{desc}: {percentage:3.0f}% |{bar}| {elapsed}<{remaining}{postfix}"

    # build mapping of attack ID to stixID
    attack_id_to_stix_id = {}
    for attack_object in tqdm(attack_data, desc="parsing ATT&CK data", bar_format=tqdm_format):
        if not attack_object["type"] == "relationship":
            # skip objects without IDs
            if not attack_object.get("external_references"):
                continue
            # skip deprecated and revoked objects
            # Note: False is the default value if the property is not present
            if attack_object.get("revoked", False):
                continue
            # Note: False is the default value if the property is not present
            if attack_object.get("x_mitre_deprecated", False):
                continue
            # map attackID to stixID
            attack_id_to_stix_id[attack_object["external_references"][0]["external_id"]] = attack_object["id"]

    # build mapping of control ID to stixID
    control_id_to_stix_id = {}
    for sdo in tqdm(controls.objects, desc="parsing controls", bar_format=tqdm_format):
        if sdo.type == "course-of-action":  # only do mitigations
            control_id_to_stix_id[sdo["external_references"][0]["external_id"]] = sdo["id"]

    # build mapping relationships
    relationships = {}
    mappings_df = pd.read_csv(mappings_path, sep="\t", keep_default_na=False, header=0)
    for index, row in tqdm(list(mappings_df.iterrows()), desc="parsing mappings", bar_format=tqdm_format):
        # create list of control STIX IDs matching this row
        from_ids = dict_regex_lookup(control_id_to_stix_id, row["controlID"])
        # create list of technique STIX IDs matching this row
        to_ids = dict_regex_lookup(attack_id_to_stix_id, row["techniqueID"])
        # only have a description if the row does
        # description = row["description"] if row["description"] else None

        if not from_ids:
            print(Fore.RED + "ERROR: cannot find controlID", row["controlID"], Fore.RESET)
            print(f"{row=}")
        if not to_ids:
            print(Fore.RED + "ERROR: cannot find techniqueID", row["techniqueID"], Fore.RESET)
            print(f"{row=}")
        if not from_ids or not to_ids:
            exit()

        # combinatorics of every from to every to
        for from_id in from_ids:
            for to_id in to_ids:
                joined_id = f"{from_id}---{to_id}"
                # build the mapping relationship
                r = Relationship(
                    id=relationship_ids[joined_id] if joined_id in relationship_ids else None,
                    source_ref=from_id,
                    target_ref=to_id,
                    relationship_type="mitigates",
                )
                if joined_id not in relationships:
                    relationships[joined_id] = r

    # construct and return the bundle of relationships
    return Bundle(*relationships.values())
