from stix2.v20 import Bundle
import pandas as pd
import argparse
import os
import requests
import json
from colorama import Fore

def mappingsToDF(attackbundle, controlsbundle, mappingsbundle):
    """Return a pandas dataframe listing the mappings in mappingsbundle"""
    rows = []
    for mapping in mappingsbundle.objects:
        control = controlsbundle.get(mapping.source_ref)
        if not control:
            print(Fore.RED + f"ERROR: cannot find object with ID {mapping.source_ref} in controls bundle" + Fore.RESET)
            exit()
        else: control = control[0]

        technique = attackbundle.get(mapping.target_ref)
        if not technique:
            print(Fore.RED + f"ERROR: cannot find object with ID {mapping.target_ref} in ATT&CK bundle" + Fore.RESET)
            exit()
        else: technique = technique[0]

        rows.append({
            "control ID": control["external_references"][0]["external_id"],
            "control name": control["name"],
            "mapping type": mapping["relationship_type"],
            "technique ID": technique["external_references"][0]["external_id"],
            "technique name": technique["name"],
            "mapping description": mapping["description"] if "description" in mapping else ""
        })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    extensionToPDExport = {
        "xlsx": "to_excel", # extension to df export function name
        "csv": "to_csv",
        "html": "to_html",
        "md": "to_markdown"
    }
    allowedExtensionList = ", ".join(extensionToPDExport.keys())
    parser = argparse.ArgumentParser(description="List mappings in human readable formats")
    parser.add_argument("-controls",
                        dest="controls",
                        help="filepath to the stix bundle representing the control framework",
                        default=os.path.join("..", "frameworks", "nist800-53-r4", "stix", "nist800-53-r4-controls.json"))
    parser.add_argument("-mappings",
                        dest="mappings",
                        help="filepath to the stix bundle mapping the controls to ATT&CK",
                        default=os.path.join("..", "frameworks", "nist800-53-r4", "stix", "nist800-53-r4-mappings.json"))
    parser.add_argument("-domain",
                        dest="domain",
                        help="which ATT&CK domain to use",
                        default="enterprise-attack")
    parser.add_argument("-version",
                        dest="version",
                        help="which ATT&CK version to use",
                        default="v7.0")
    parser.add_argument("-output",
                        help=f"filepath to write the output mappings to. Output format will be inferred from the extension. Allowed extensions: {allowedExtensionList}",
                        default=os.path.join("..", "frameworks", "nist800-53-r4", "nist800-53-r4-mappings.xlsx"))

    args = parser.parse_args()

    extension = args.output.split(".")[-1]
    if extension not in extensionToPDExport:
        print(Fore.RED + f"ERROR: Unknown output extension \"{extension}\", please make sure your output extension is one of: {allowedExtensionList}", Fore.reset)
        exit()

    print("downloading ATT&CK data... ", end="", flush=True)
    attackdata = Bundle(
        requests.get(f"https://raw.githubusercontent.com/mitre/cti/ATT%26CK-{args.version}/{args.domain}/{args.domain}.json", verify=False).json()["objects"],
        allow_custom=True)
    print("done")

    print("loading controls framework... ", end="", flush=True)
    with open(args.controls, "r") as f:
        controls = Bundle(json.load(f)["objects"], allow_custom=True)
    print("done")

    print("loading mappings... ", end="", flush=True)
    with open(args.mappings, "r") as f:
        mappings = Bundle(json.load(f)["objects"])
    df = mappingsToDF(attackdata, controls, mappings)
    print("done")

    print(f"writing {args.output}...", end="", flush=True)
    if extension in ["md"]: # md doesn't support index=False and requires a stream and not a path
        with open(args.output, "w") as f:
            getattr(df, extensionToPDExport[extension])(f)
    else:
        getattr(df, extensionToPDExport[extension])(args.output, index=False)
        print("done")
