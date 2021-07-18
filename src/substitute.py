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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="substitute the mitigations in ATT&CK with a controls framework")
    parser.add_argument("-controls",
                        dest="controls",
                        help="filepath to the stix bundle representing the control framework",
                        default=os.path.join("..", "frameworks", "nist800-53-r5",
                                             "stix", "nist800-53-r5-controls.json"))
    parser.add_argument("-mappings",
                        dest="mappings",
                        help="filepath to the stix bundle mapping the controls to ATT&CK",
                        default=os.path.join("..", "frameworks", "nist800-53-r5",
                                             "stix", "nist800-53-r5-mappings.json"))
    parser.add_argument("-domain",
                        choices=["enterprise-attack", "mobile-attack", "pre-attack"],
                        help="the domain of ATT&CK to substitute",
                        default="enterprise-attack")
    parser.add_argument("-version",
                        dest="version",
                        help="which ATT&CK version to use",
                        default="v9.0")
    parser.add_argument("--allow-unmapped",
                        dest="allow_unmapped",
                        action="store_true",
                        help="if flag is present, output bundle will include controls that don't map to techniques. "
                             "By default only controls that have technique mappings will be included",
                        default=False)
    parser.add_argument("-output",
                        help="filepath to write the output stix bundle to",
                        default=os.path.join("..", "frameworks", "nist800-53-r5",
                                             "stix", "nist800-53-r5-enterprise-attack.json"))

    args = parser.parse_args()

    print("downloading ATT&CK data... ", end="", flush=True)
    url = f"https://raw.githubusercontent.com/mitre/cti/ATT%26CK-{args.version}/{args.domain}/{args.domain}.json"
    attack_data = Bundle(
        requests.get(url, verify=True).json()["objects"],
        allow_custom=True
    )
    print("done")

    print("loading controls framework... ", end="", flush=True)
    with open(args.controls, "r") as f:
        controls = Bundle(json.load(f)["objects"], allow_custom=True)
    print("done")

    print("loading mappings... ", end="", flush=True)
    with open(args.mappings, "r") as f:
        mappings = Bundle(json.load(f)["objects"])
    print("done")

    print("substituting... ", end="", flush=True)
    out_bundle = substitute(attack_data, controls, mappings, args.allow_unmapped)
    print("done")

    save_bundle(out_bundle, args.output)
