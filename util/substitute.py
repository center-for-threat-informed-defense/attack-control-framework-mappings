from stix2.v20 import Bundle
import argparse
import os
import requests
import json

def save_bundle(bundle, path):
    """helper function to write a STIX bundle to a file
    faster than memorystore util function"""

    print(f"{'overwriting' if os.path.exists(path) else 'writing'} {path}... ", end="", flush=True)
    strbundle = bundle.serialize(pretty=False, include_optional_defaults=False, ensure_ascii=False)
    with open(path, "w") as outfile:
        json.dump(json.loads(strbundle), outfile, indent=4, sort_keys=True)
    print("done!")

def substitute(attackbundle, controlsbundle, mappingsbundle, allowunmapped=False):
    """substitute the controls bundle and mappings bundle for the mitigations in attackbundle. 
    attackbundle, controlsbundle and mappingsbundle are of type stix2.Bundle
    allowunmapped, if true, allows controls in the output bundle if they don't have mappings to ATT&CK techniques
    Returns a new bundle resembling attackbundle but with mitigations and mitigates relationships from controlsbundle and mappingsbundle
    """
    # add attack data which are not mitigations or mitigation relationships
    outobjects = list(filter(lambda sdo: not (sdo["type"] == "course-of-action") and not (sdo["type"] == "relationship" and sdo["relationship_type"] == "mitigates"), attackbundle.objects))
    if allowunmapped: # add all controls
        outobjects += controlsbundle.objects
    else: # add only controls which have associated mappings
        used_ids = set()
        for mapping in mappingsbundle.objects:
            used_ids.add(mapping["source_ref"])
        outobjects += list(filter(lambda sdo: sdo["id"] in used_ids, controlsbundle.objects))
    # add mappings
    outobjects += mappingsbundle.objects

    return Bundle(*outobjects, allow_custom=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="substitute the mitigations in ATT&CK with a controls framework")
    parser.add_argument("-controls",
                        dest="controls",
                        help="filepath to the stix bundle representing the control framework",
                        default=os.path.join("..", "frameworks", "nist800-53-r5", "stix", "nist800-53-r5-controls.json"))
    parser.add_argument("-mappings",
                        dest="mappings",
                        help="filepath to the stix bundle mapping the controls to ATT&CK",
                        default=os.path.join("..", "frameworks", "nist800-53-r5", "stix", "nist800-53-r5-mappings.json"))
    parser.add_argument("-domain",
                        choices=["enterprise-attack", "mobile-attack", "pre-attack"],
                        help="the domain of ATT&CK to substitute",
                        default="enterprise-attack")
    parser.add_argument("-version",
                        dest="version",
                        help="which ATT&CK version to use",
                        default="v7.0-beta")
    parser.add_argument("--allow-unmapped",
                        dest="allowunmapped",
                        action="store_true",
                        help="if flag is present, output bundle will include controls that don't map to techniques. By default only controls that have technique mappings will be included",
                        default=False)
    parser.add_argument("-output",
                        help="filepath to write the output stix bundle to",
                        default=os.path.join("..", "frameworks", "nist800-53-r5", "stix", "nist800-53-r5-enterprise-attack.json"))

    args = parser.parse_args()

    print("downloading ATT&CK data... ", end="", flush=True)
    attackdata = Bundle(
        requests.get(f"https://raw.githubusercontent.com/mitre/cti/ATT%26CK-{args.version}/{args.domain}/{args.domain}.json").json()["objects"], 
        allow_custom=True)
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
    outbundle = substitute(attackdata, controls, mappings, args.allowunmapped)
    print("done")

    save_bundle(outbundle, args.output)