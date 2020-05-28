import argparse
import re
import stix2
import os
import json
import requests


def technique(attackID, mapped_controls):
    """create a technique for a layer"""
    return {
        "techniqueID": attackID,
        "score": len(mapped_controls), # count of mapped controls
        "comment": "Mitigated by " + ", ".join(mapped_controls) # list of mapped controls
    }


def layer(name, description, domain, techniques):
    """create a Layer"""
    return {
        "name": name,
        "version": "3.0",
        "sorting": 3, # descending order of score
        "description": description,
        "domain": domain,
        "techniques": techniques,
        "gradient": {
            "colors": [
                "#8cff8c", # low counts are green
                "#fcff7c",
                "#ff8c8c", # high counts are red
            ],
            "minValue": min(map(lambda t: t["score"], techniques)) if len(techniques) > 0 else 0,
            "maxValue": max(map(lambda t: t["score"], techniques)) if len(techniques) > 0 else 100 # max value is max usage count
        },
    }

def mappingsToTechniquelist(controls, mappings, attackdata):
    """take an array of controls ms, a mappings ms, and attackdata ms
    return a list of Techniques where the score is the number of controls that map to the technique"""
    techniqueToMappedControls = {}
    for mapping in mappings.query():
        # source_ref is the control in controls
        if not controls.get(mapping.source_ref): continue # mapping not relevant to this list of controls
        controlID = controls.get(mapping.source_ref).external_references[0].external_id
        # target_ref is the technique in attackdata
        attackID = attackdata.get(mapping.target_ref).external_references[0].external_id
        # build the mapping
        if attackID in techniqueToMappedControls:
            techniqueToMappedControls[attackID].append(controlID)
        else:
            techniqueToMappedControls[attackID] = [controlID]
    # transform to techniques
    return [technique(id, techniqueToMappedControls[id]) for id in techniqueToMappedControls]

def mappingsToHeatmaps(controls, mappings, attackdata, domain):
    """ingest mappings and controls and attackdata, and return an array of layer jsons"""
    # build list of control families
    idToFamily = re.compile("(\w+)-.*")
    familyToControls = {} # family ID to control object
    for control in controls.query([stix2.Filter("type", "=", "course-of-action")]):
        family = idToFamily.search(control.external_references[0].external_id).groups()[0]
        if family not in familyToControls:
            familyToControls[family] = [control]
        else:
            familyToControls[family].append(control)
    
    outlayers = [
        layer(
            "overview heatmap", 
            "heatmap overview of control mappings, where scores are the number of associated controls",
            domain, 
            mappingsToTechniquelist(controls, mappings, attackdata)
        )
    ]
    for family in familyToControls:
        controlsInFamily = stix2.MemoryStore(stix_data=familyToControls[family])
        techniques = mappingsToTechniquelist(controlsInFamily, mappings, attackdata)
        if len(techniques) > 0: # don't build heatmaps with no mappings
            outlayers.append(
                layer(
                    f"{family} heatmap",
                    f"heatmap for controls in the family {family}, where scores are the number of associated controls",
                    domain,
                    techniques
                )
        )

    return outlayers


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create ATT&CK Navigator heatmap layers from control mappings")
    parser.add_argument("-controls",
                        dest="controls",
                        help="filepath to the stix bundle representing the control framework",
                        default=os.path.join("..", "frameworks", "nist800-53-r5", "data", "sp800-53r5-controls.json"))
    parser.add_argument("-mappings",
                        dest="mappings",
                        help="filepath to the stix bundle mapping the controls to ATT&CK",
                        default=os.path.join("..", "frameworks", "nist800-53-r5", "data", "sp800-53r5-mappings.json"))
    parser.add_argument("-domain",
                        choices=["enterprise-attack", "mobile-attack", "pre-attack"],
                        help="the domain of ATT&CK to visualize",
                        default="enterprise-attack")
    parser.add_argument("-output",
                        help="folder to write output layers to",
                        default=os.path.join("..", "frameworks", "nist800-53-r5", "layers"))
    
    args = parser.parse_args()

    print("downloading ATT&CK data... ", end="", flush=True)
    attackdata = stix2.MemoryStore(stix_data=requests.get(f"https://raw.githubusercontent.com/mitre/cti/subtechniques/{args.domain}/{args.domain}.json", verify=False).json()["objects"])
    print("done")

    print("loading controls framework... ", end="", flush=True)
    with open(args.controls, "r") as f:
        controls = stix2.MemoryStore(stix_data=json.load(f)["objects"])
    print("done")

    print("loading mappings... ", end="", flush=True)
    with open(args.mappings, "r") as f:
        mappings = stix2.MemoryStore(stix_data=json.load(f)["objects"])
    print("done")

    print("creating layers... ", end="", flush=True)
    layers = mappingsToHeatmaps(controls, mappings, attackdata, args.domain)
    for layer in layers:
        filename = "_".join(layer["name"].split(" ")) + ".json"
        with open(os.path.join(args.output, filename), "w") as f:
            json.dump(layer, f)
    print("done")