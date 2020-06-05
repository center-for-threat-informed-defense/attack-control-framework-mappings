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
    min_mappings = min(map(lambda t: t["score"], techniques)) if len(techniques) > 0 else 0
    max_mappings = max(map(lambda t: t["score"], techniques)) if len(techniques) > 0 else 100
    gradient = [ "#8ec843", "#ffe766", "#ff6666" ]
    # check if all the same count of mappings
    if max_mappings - min_mappings == 0: 
        min_mappings = 0 # set low end of gradient to 0
        gradient = ["#ffffff", "#66b1ff"]

    return {
        "name": name,
        "version": "3.0",
        "sorting": 3, # descending order of score
        "description": description,
        "domain": domain,
        "techniques": techniques,
        "gradient": {
            "colors": gradient,
            "minValue": min_mappings,
            "maxValue": max_mappings
        },
    }

def mappingsToTechniquelist(controls, mappings, attackdata):
    """take a controls ms, a mappings ms, and attackdata ms
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

    # remove duplicate mappings
    for id in techniqueToMappedControls:
        techniqueToMappedControls[id] = list(set(techniqueToMappedControls[id]))

    # transform to techniques
    return [technique(id, techniqueToMappedControls[id]) for id in techniqueToMappedControls]

def mappingsToHeatmaps(controls, mappings, attackdata, domain, frameworkname):
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
        {
            "outfile": f"{frameworkname}-overview.json",
            "layer": layer(
                f"{frameworkname} overview", 
                f"{frameworkname} heatmap overview of control mappings, where scores are the number of associated controls",
                domain, 
                mappingsToTechniquelist(controls, mappings, attackdata)
            )
        }
    ]
    for family in familyToControls:
        controlsInFamily = stix2.MemoryStore(stix_data=familyToControls[family])
        techniquesInFamily = mappingsToTechniquelist(controlsInFamily, mappings, attackdata)
        if len(techniquesInFamily) > 0: # don't build heatmaps with no mappings
            # build family overview mapping
            outlayers.append({
                "outfile": os.path.join(family, f"{family}-overview.json"),
                "layer": layer(
                    f"{family} overview",
                    f"{frameworkname} heatmap for controls in the family {family}, where scores are the number of associated controls",
                    domain,
                    techniquesInFamily
                )
            })
            # build layer for each control
            for control in familyToControls[family]:
                controlMs = stix2.MemoryStore(stix_data=control)
                control_id = control.external_references[0].external_id
                techniquesMappedToControl = mappingsToTechniquelist(controlMs, mappings, attackdata)
                if len(techniquesMappedToControl) > 0: # don't build heatmaps with no mappings
                    outlayers.append({
                        "outfile": os.path.join(family, f"{'_'.join(control_id.split(' '))}.json"),
                        "layer": layer(
                            f"{control_id} mappings",
                            f"{frameworkname} {control_id} mappings",
                            domain,
                            techniquesMappedToControl
                        )
                    })

            


    return outlayers


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create ATT&CK Navigator heatmap layers from control mappings")
    parser.add_argument("-framework",
                        help="the name of the control framework",
                        default="nist800-53-r5")
    parser.add_argument("-controls",
                        dest="controls",
                        help="filepath to the stix bundle representing the control framework",
                        default=os.path.join("..", "frameworks", "nist800-53-r5", "data", "nist800-53-r5-controls.json"))
    parser.add_argument("-mappings",
                        dest="mappings",
                        help="filepath to the stix bundle mapping the controls to ATT&CK",
                        default=os.path.join("..", "frameworks", "nist800-53-r5", "data", "nist800-53-r5-mappings.json"))
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
    layers = mappingsToHeatmaps(controls, mappings, attackdata, args.domain, args.framework)
    for layer in layers:
        # make path if it doesn't exist
        layerdir = os.path.dirname(os.path.join(args.output, layer["outfile"]))
        if not os.path.exists(layerdir):
            os.makedirs(layerdir)
        # write layer
        with open(os.path.join(args.output, layer["outfile"]), "w") as f:
            json.dump(layer["layer"], f)
    print("done")