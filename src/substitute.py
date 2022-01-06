import argparse
import json
import os

from stix2.v20 import Bundle
import requests


def save_bundle(bundle, path):
    """helper function to write a STIX bundle to file"""
    print(f"{'overwriting' if os.path.exists(path) else 'writing'} {path}... ", end="", flush=True)
    with open(path, "w", encoding="utf-8") as outfile:
        bundle.fp_serialize(outfile, indent=4, sort_keys=True, ensure_ascii=False)
    print("done!")


def substitute(attack_bundle, controls_bundle, mappings_bundle, allow_unmapped=False):
    """substitute the controls bundle and mappings bundle for the mitigations in attack_bundle.
    attack_bundle, controls_bundle and mappings_bundle are of type stix2.Bundle
    allow_unmapped, if true, allows controls in the output bundle if they don't have mappings to ATT&CK techniques
    Returns a new bundle resembling attack_bundle but with mitigations and mitigates relationships
    from controls_bundle and mappings_bundle
    """
    # add attack data which are not mitigations or mitigation relationships
    out_objects = list(filter(
        lambda sdo: not (sdo["type"] == "course-of-action") and not
        (sdo["type"] == "relationship" and sdo["relationship_type"] == "mitigates"),
        attack_bundle.objects))
    if allow_unmapped:  # add all controls
        out_objects += controls_bundle.objects
    else:  # add only controls which have associated mappings
        used_ids = set()
        for mapping in mappings_bundle.objects:
            used_ids.add(mapping["source_ref"])
        out_objects += list(filter(lambda sdo: sdo["id"] in used_ids, controls_bundle.objects))
    # add mappings
    out_objects += mappings_bundle.objects

    return Bundle(*out_objects, allow_custom=True)


def main(controls, mappings, domain, version, allow_unmapped, output):
    if version != "v9.0":
        controls = controls.replace("attack_9_0", f"ATT&CK-{version}")
        mappings = mappings.replace("attack_9_0", f"ATT&CK-{version}")
        output = output.replace("attack_9_0", f"ATT&CK-{version}")

    print("downloading ATT&CK data... ", end="", flush=True)
    url = f"https://raw.githubusercontent.com/mitre/cti/ATT%26CK-{version}/{domain}/{domain}.json"
    attack_data = Bundle(
        requests.get(url, verify=True).json()["objects"],
        allow_custom=True
    )
    print("done")

    print("loading controls framework... ", end="", flush=True)
    with open(controls, "r") as f:
        controls = Bundle(json.load(f)["objects"], allow_custom=True)
    print("done")

    print("loading mappings... ", end="", flush=True)
    with open(mappings, "r") as f:
        mappings = Bundle(json.load(f)["objects"])
    print("done")

    print("substituting... ", end="", flush=True)
    out_bundle = substitute(attack_data, controls, mappings, allow_unmapped)
    print("done")

    save_bundle(out_bundle, output)
