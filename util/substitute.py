import stix2
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

def substitute(attackbundle, controlsbundle, mappingsbundle):
    """substitute the controls bundle and mappings bundle for the mitigations in attackbundle. 
    All arguments are of type stix2.Bundle
    Returns a new bundle resembling attackbundle but with mitigations and mitigates relationships from controlsbundle and mappingsbundle
    """
    outobjects = list(filter(lambda sdo: not (sdo["type"] == "course-of-action") and not (sdo["type"] == "relationship" and sdo["relationship_type"] == "mitigates"), attackbundle.objects))
    outobjects += controlsbundle.objects
    outobjects += mappingsbundle.objects

    return stix2.Bundle(*outobjects, spec_version="2.0", allow_custom=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="substitute the mitigations in ATT&CK with a controls framework")
    parser.add_argument("-controls",
                        dest="controls",
                        help="filepath to the stix bundle representing the control framework",
                        default=os.path.join("..", "frameworks", "nist800-53-r4", "data", "800-53-r4-controls.json"))
    parser.add_argument("-mappings",
                        dest="mappings",
                        help="filepath to the stix bundle mapping the controls to ATT&CK",
                        default=os.path.join("..", "frameworks", "nist800-53-r4", "data", "800-53-r4-mappings.json"))
    parser.add_argument("-domain",
                        choices=["enterprise-attack", "mobile-attack", "pre-attack"],
                        help="the domain of ATT&CK to substitute",
                        default="enterprise-attack")
    parser.add_argument("-output",
                        help="filepath to write the output stix bundle to",
                        default=os.path.join("..", "frameworks", "nist800-53-r4", "data", "enterprise-nist-800-53-rev4.json"))

    args = parser.parse_args()

    print("downloading ATT&CK data... ", end="", flush=True)
    attackdata = stix2.Bundle(
        requests.get(f"https://raw.githubusercontent.com/mitre/cti/subtechniques/{args.domain}/{args.domain}.json", verify=False).json()["objects"], 
        spec_version="2.0",
        allow_custom=True)
    print("done")
    print("loading controls framework... ", end="", flush=True)
    with open(args.controls, "r") as f:
        controls = stix2.Bundle(json.load(f)["objects"], spec_version="2.0")

    print("done")
    print("loading mappings... ", end="", flush=True)
    with open(args.mappings, "r") as f:
        mappings = stix2.Bundle(json.load(f)["objects"], spec_version="2.0")

    print("done")

    print("substituting... ", end="", flush=True)
    outbundle = substitute(attackdata, controls, mappings)
    print("done")

    save_bundle(outbundle, args.output)