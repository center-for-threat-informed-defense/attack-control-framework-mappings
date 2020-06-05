import stix2
import argparse
import os
import json
from parse_controls import parse_controls
from parse_mappings import parse_mappings

def save_bundle(bundle, path):
    """helper function to write a STIX bundle to a file
    faster than memorystore util function"""

    print(f"{'overwriting' if os.path.exists(path) else 'writing'} {path}... ", end="", flush=True)
    strbundle = bundle.serialize(pretty=False, include_optional_defaults=False, ensure_ascii=False)
    with open(path, "w") as outfile:
        json.dump(json.loads(strbundle), outfile, indent=4, sort_keys=True)
    print("done!")

def main(incontrols=os.path.join("data", "nist800-53-r4-controls.tsv"), 
         inmappings=os.path.join("data", "nist800-53-r4-mappings.tsv"),
         outcontrols=os.path.join("data", "nist800-53-r4-controls.json"),
         outmappings=os.path.join("data", "nist800-53-r4-controls.json"),
         attackdata="https://raw.githubusercontent.com/mitre/cti/subtechniques/enterprise-attack/enterprise-attack.json"):
    """
    parse the NIST 800-53 revision 4 controls and ATT&CK mappings into STIX2.0 bundles
    arguments:
        incontrols - tsv file of NIST 800-53 revision 4 controls
        inmappings - tsv file mapping NIST 800-53 revision 4 controls to ATT&CK
        outcontrols - output STIX bundle file for the controls. If this file already exists, the STIX IDs within will be reused in the replacing file so that they don't change between consecutive executions of this script.
        outmappings - output STIX bundle file for the mappings.
        attackdata - URL of the attack STIX bundle to use when looking up mapping IDs
    returns (outcontrols, outmappings)
    """

    # build control ID helper lookups so that STIX IDs don't get replaced on each rebuild
    control_ids = {}
    control_relationship_ids = {}
    if os.path.exists(outcontrols):
        # parse idMappings from existing output so that IDs don't change when regenerated
        with open(outcontrols, "r") as f:
            bundle = json.load(f)
        for sdo in bundle["objects"]:
            if not sdo["type"] == "relationship":
                fromID = sdo["external_references"][0]["external_id"]
                toID = sdo["id"]
                control_ids[fromID] = toID
            else:
                # parse relationships
                fromIDs = f"{sdo['source_ref']}---{sdo['target_ref']}"
                toID = sdo["id"]
                control_relationship_ids[fromIDs] = toID
    
    # build controls in STIX
    controls = parse_controls(
        incontrols,
        control_ids,
        control_relationship_ids
    )

    # build mapping ID helper lookup so that STIX IDs don't get replaced on each rebuild
    mapping_relationship_ids = {}
    if os.path.exists(outmappings):
        with open(outmappings, "r") as f:
            bundle = json.load(f)
        for sdo in bundle["objects"]:
            fromIDs = f"{sdo['source_ref']}---{sdo['target_ref']}"
            toID = sdo["id"]
            mapping_relationship_ids[fromIDs] = toID
    
    # build mappings in STIX
    mappings = parse_mappings(
        inmappings,
        controls,
        attackdata,
        mapping_relationship_ids
    )

    save_bundle(controls, outcontrols)
    save_bundle(mappings, outmappings)

    return outcontrols, outmappings

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="parse the NIST 800-53 revision 4 controls and ATT&CK mappings into STIX2.0 bundles")
    parser.add_argument("-input-controls",
                        dest="incontrols",
                        help="tsv file of NIST 800-53 revision 4 controls",
                        default=os.path.join("data", "nist800-53-r4-controls.tsv"))
    parser.add_argument("-input-mappings",
                        dest="inmappings",
                        help="tsv file mapping NIST 800-53 revision 4 controls to ATT&CK",
                        default=os.path.join("data", "nist800-53-r4-mappings.tsv"))
    parser.add_argument("-output-controls",
                         dest="outcontrols",
                         help="output STIX bundle file for the controls. If this file already exists, the STIX IDs within will be reused in the replacing file so that they don't change between consecutive executions of this script.",
                         default=os.path.join("data", "nist800-53-r4-controls.json"))
    parser.add_argument("-output-mappings",
                         dest="outmappings",
                         help="output STIX bundle file for the mappings.",
                         default=os.path.join("data", "nist800-53-r4-mappings.json"))
    parser.add_argument("-attack-data",
                        dest="attackdata",
                        help="URL of the attack STIX bundle to use when looking up mapping IDs",
                        default="https://raw.githubusercontent.com/mitre/cti/subtechniques/enterprise-attack/enterprise-attack.json")

    args = parser.parse_args()

    main(**vars(args))
