import stix2
import argparse
from parse_controls import parse_controls
import os
import json

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="parse the NIST 800-53 revision 4 controls and ATT&CK mappings into a STIX2.0 bundle")
    parser.add_argument("-input-controls",
                        dest="incontrols",
                        help="tsv file of NIST 800-53 revision 4 controls",
                        default=os.path.join("data", "800-53-r4-controls.tsv"))
    parser.add_argument("-input-mappings",
                        dest="inmappings",
                        help="tsv file mapping NIST 800-53 revision 4 controls to ATT&CK",
                        default=os.path.join("data", "800-53-r4-mappings.tsv"))
    parser.add_argument("-output-controls",
                         dest="outcontrols",
                         help="output STIX bundle file for the controls. If this file already exists, the STIX IDs within will be reused in the replacing file so that they don't change between consecutive executions of this script.",
                         default=os.path.join("data", "800-53-r4-controls.json"))
    parser.add_argument("-output-mappings",
                         dest="outmappings",
                         help="output STIX bundle file for the mappings.",
                         default=os.path.join("data", "800-53-r4-mappings.json"))

    args = parser.parse_args()

    # build ID helper lookups so that STIX IDs don't get replaced on each rebuild
    control_ids = {}
    relationship_ids = {}
    if os.path.exists(args.outcontrols):
        # parse idMappings from existing output so that IDs don't change when regenerated
        with open(args.outcontrols, "r") as f:
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
                relationship_ids[fromIDs] = toID
    
    # build controls in STIX
    controls = parse_controls(
        args.incontrols,
        control_ids,
        relationship_ids
    )
    
    # write bundle JSON
    print(f"writing {args.outcontrols}... ", end="", flush=True)
    strbundle = controls.serialize(pretty=False, include_optional_defaults=False, ensure_ascii=False)
    with open(args.outcontrols, "w") as outfile:
        json.dump(json.loads(strbundle), outfile, indent=4, sort_keys=True)

    # controls_ms = stix2.MemoryStore()
    # controls_ms.add(controls)
    # controls_ms.save_to_file(args.outcontrols)
    print("done!")
