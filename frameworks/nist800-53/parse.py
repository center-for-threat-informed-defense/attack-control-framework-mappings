import stix2
import argparse
from parse_controls import parse_controls
import os
import json

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="parse the NIST 800-53 controls and ATT&CK mappings into a STIX2.0 bundle")
    parser.add_argument("-input-controls",
                        dest="incontrols",
                        help="tsv file of NIST 800-53 controls",
                        default=os.path.join("data", "800-53-controls.tsv"))
    parser.add_argument("-input-mappings",
                        dest="inmappings",
                        help="tsv file mapping NIST 800-53 controls to ATT&CK",
                        default=os.path.join("data", "800-53-mappings.tsv"))
    parser.add_argument("-output-controls",
                         dest="outcontrols",
                         help="output STIX bundle file for the controls. If this file already exists, the STIX IDs within will be reused in the replacing file so that they don't change between consecutive executions of this script.",
                         default=os.path.join("data", "800-53-controls.json"))
    parser.add_argument("-output-mappings",
                         dest="outmappings",
                         help="output STIX bundle file for the mappings.",
                         default=os.path.join("data", "800-53-mappings.json"))

    args = parser.parse_args()

    idMappings = {}
    if os.path.exists(args.outcontrols):
        # parse idMappings from existing output so that IDs don't change when regenerated
        with open(args.outcontrols, "r") as f:
            bundle = json.load(f)
        for sdo in bundle["objects"]:
            fromID = sdo["external_references"][0]["external_id"]
            toID = sdo["id"]
            idMappings[fromID] = toID

    controls = parse_controls(
        args.incontrols,
        idMappings
    )
    print(f"saving controls to {args.outcontrols}... ", end="", flush=True)
    controls_ms = stix2.MemoryStore()
    controls_ms.add(controls)
    controls_ms.save_to_file(args.outcontrols)
    print("done!")
