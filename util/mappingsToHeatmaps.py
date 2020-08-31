import argparse
import re
from stix2 import Filter, MemoryStore
import os
import json
import requests
import itertools
import shutil

def technique(attackID, mapped_controls):
    """create a technique for a layer"""
    return {
        "techniqueID": attackID,
        "score": len(mapped_controls), # count of mapped controls
        "comment": "Mitigated by " + ", ".join(sorted(mapped_controls)) # list of mapped controls
    }


def layer(name, description, domain, techniques):
    """create a Layer"""
    min_mappings = min(map(lambda t: t["score"], techniques)) if len(techniques) > 0 else 0
    max_mappings = max(map(lambda t: t["score"], techniques)) if len(techniques) > 0 else 100
    gradient = [ "#ACD0E6", "#08336E" ]
    # check if all the same count of mappings
    if max_mappings - min_mappings == 0: 
        min_mappings = 0 # set low end of gradient to 0
        gradient = ["#ffffff", "#66b1ff"]

    domain = { # convert domain to navigator format
        "enterprise-attack": "mitre-enterprise",
        "mobile-attack": "mitre-mobile",
    }[domain]

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

def parseFamilyData(controls):
    """ingest control data to return familyIDToControls mapping and familyIDToName mapping"""
    idToFamily = re.compile("(\w+)-.*")

    familyIDToControls = {} # family ID to control object
    familyIDToName = {}
    for control in controls.query([Filter("type", "=", "course-of-action")]):
        # parse family ID from control external ID
        familyID = idToFamily.search(control["external_references"][0]["external_id"]).groups()[0]
        if familyID not in familyIDToControls:
            familyIDToControls[familyID] = [control]
        else:
            familyIDToControls[familyID].append(control)
        # parse family name if possible, or just use family ID if not
        if "x_mitre_family" in control:
            familyIDToName[familyID] = control["x_mitre_family"]
        else:
            familyIDToName[familyID] = familyID

    return familyIDToControls, familyIDToName, idToFamily

def toTechniquelist(controls, mappings, attackdata, familyIDToControls, familyIDToName, idToFamily):
    """take a controls ms, a mappings ms, and attackdata ms
    return a list of Techniques where the score is the number of controls that map to the technique"""

    techniqueToMappedControls = {}
    for mapping in mappings.query():
        # source_ref is the control in controls
        if not controls.get(mapping["source_ref"]): continue # mapping not relevant to this list of controls
        controlID = controls.get(mapping["source_ref"])["external_references"][0]["external_id"]
        # target_ref is the technique in attackdata
        attackID = attackdata.get(mapping["target_ref"])["external_references"][0]["external_id"]
        # build the mapping
        if attackID in techniqueToMappedControls:
            techniqueToMappedControls[attackID].append(controlID)
        else:
            techniqueToMappedControls[attackID] = [controlID]
    
    # collapse families where all controls are mapped; list just the family identifier
    for id in techniqueToMappedControls:
        controlIDs = techniqueToMappedControls[id]
        # Group mapped controls for this technique according to the family
        families = {}
        for controlID in controlIDs:
            familyID = idToFamily.search(controlID).groups()[0]
            if familyID not in families:
                families[familyID] = {controlID} # new set
            else:
                families[familyID].add(controlID) # add to set

        # are all controls in the family mapped?
        collapsedControls = []
        for familyID in families:
            familySet = families[familyID]
            controlsInFamily = set(map(lambda c: c["external_references"][0]["external_id"], familyIDToControls[familyID]))
            if familySet == controlsInFamily: # all controls in family mapped?
                # collapse
                collapsedControls.append(f"all '{familyIDToName[familyID]}' controls")
            else:
                collapsedControls += controlIDs
        techniqueToMappedControls[id] = collapsedControls
    
    # remove duplicate mappings
    for id in techniqueToMappedControls:
        techniqueToMappedControls[id] = list(set(techniqueToMappedControls[id]))

    # transform to techniques
    return [technique(id, techniqueToMappedControls[id]) for id in techniqueToMappedControls]

def getFrameworkOverviewLayers(controls, mappings, attackdata, domain, frameworkname):
    """ingest mappings and controls and attackdata, and return an array of layer jsons for layers according to control family"""
    # build list of control families
    familyIDToControls, familyIDToName, idToFamily = parseFamilyData(controls)
    
    outlayers = [
        {
            "outfile": f"{frameworkname}-overview.json",
            "layer": layer(
                f"{frameworkname} overview", 
                f"{frameworkname} heatmap overview of control mappings, where scores are the number of associated controls",
                domain, 
                toTechniquelist(controls, mappings, attackdata, familyIDToControls, familyIDToName, idToFamily)
            )
        }
    ]
    for familyID in familyIDToControls:
        controlsInFamily = MemoryStore(stix_data=familyIDToControls[familyID])
        techniquesInFamily = toTechniquelist(controlsInFamily, mappings, attackdata, familyIDToControls, familyIDToName, idToFamily)
        if len(techniquesInFamily) > 0: # don't build heatmaps with no mappings
            # build family overview mapping
            outlayers.append({
                "outfile": os.path.join("by family", familyIDToName[familyID], f"{familyID}-overview.json"),
                "layer": layer(
                    f"{familyIDToName[familyID]} overview",
                    f"{frameworkname} heatmap for controls in the {familyIDToName[familyID]} family, where scores are the number of associated controls",
                    domain,
                    techniquesInFamily
                )
            })
            # build layer for each control
            for control in familyIDToControls[familyID]:
                controlMs = MemoryStore(stix_data=control)
                control_id = control["external_references"][0]["external_id"]
                techniquesMappedToControl = toTechniquelist(controlMs, mappings, attackdata, familyIDToControls, familyIDToName, idToFamily)
                if len(techniquesMappedToControl) > 0: # don't build heatmaps with no mappings
                    outlayers.append({
                        "outfile": os.path.join("by family", familyIDToName[familyID], f"{'_'.join(control_id.split(' '))}.json"),
                        "layer": layer(
                            f"{control_id} mappings",
                            f"{frameworkname} {control_id} mappings",
                            domain,
                            techniquesMappedToControl
                        )
                    })
    
    return outlayers

def getLayersByProperty(controls, mappings, attackdata, domain, frameworkname, x_mitre):
    """get layers grouping the mappings according to values of the given property"""
    propertyname = x_mitre.split("x_mitre_")[1] # remove prefix

    familyIDToControls, familyIDToName, idToFamily = parseFamilyData(controls)

    
    # group controls by the property
    propertyValueToControls = {}
    def addToDict(value, control):
        if value in propertyValueToControls:
            propertyValueToControls[value].append(control)
        else:
            propertyValueToControls[value] = [control]
    # iterate through controls, grouping by property
    isListType = False
    for control in controls.query([Filter("type", "=", "course-of-action")]):
        value = control.get(x_mitre)
        if not value: continue
        if isinstance(value, list):
            isListType = True
            for v in value: addToDict(v, control)
        else: addToDict(value, control)
        
    outlayers = []
    for value in propertyValueToControls:
        # controls for the corresponding values
        controlsOfValue = MemoryStore(stix_data=propertyValueToControls[value])
        techniques = toTechniquelist(controlsOfValue, mappings, attackdata, familyIDToControls, familyIDToName, idToFamily)
        if len(techniques) > 0:
            # build layer for this technique set
            outlayers.append({
                "outfile": os.path.join(f"by {propertyname}", f"{value}.json"),
                "layer": layer(
                    f"{propertyname}={value}",
                    f"techniques where the {propertyname} of associated controls {'includes' if isListType else 'is'} {value}",
                    domain, 
                    techniques
                )
            })

    return outlayers

def get_x_mitre(ms, type="course-of-action"):
    """return a list of all x_mitre_ properties defined on the given type"""
    keys = set()
    for obj in ms.query([Filter("type", "=", type)]):
        for key in obj:
            if key.startswith("x_mitre_"): keys.add(key)
    return keys

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create ATT&CK Navigator layers from control mappings")
    parser.add_argument("-framework",
                        help="the name of the control framework",
                        default="nist800-53-r4")
    parser.add_argument("-controls",
                        dest="controls",
                        help="filepath to the stix bundle representing the control framework",
                        default=os.path.join("..", "frameworks", "nist800-53-r4", "data", "nist800-53-r4-controls.json"))
    parser.add_argument("-mappings",
                        dest="mappings",
                        help="filepath to the stix bundle mapping the controls to ATT&CK",
                        default=os.path.join("..", "frameworks", "nist800-53-r4", "data", "nist800-53-r4-mappings.json"))
    parser.add_argument("-domain",
                        choices=["enterprise-attack", "mobile-attack"],
                        help="the domain of ATT&CK to visualize",
                        default="enterprise-attack")
    parser.add_argument("-version",
                        dest="version",
                        help="which ATT&CK version to use",
                        default="v7.0")
    parser.add_argument("-output",
                        help="folder to write output layers to",
                        default=os.path.join("..", "frameworks", "nist800-53-r4", "layers"))
    parser.add_argument("--clear",
                        action="store_true",
                        help="if flag specified, will remove the contents the output folder before writing layers")
    
    args = parser.parse_args()

    print("downloading ATT&CK data... ", end="", flush=True)
    attackdata = MemoryStore(stix_data=requests.get(f"https://raw.githubusercontent.com/mitre/cti/ATT%26CK-{args.version}/{args.domain}/{args.domain}.json", verify=False).json()["objects"])
    print("done")

    print("loading controls framework... ", end="", flush=True)
    with open(args.controls, "r") as f:
        controls = MemoryStore(stix_data=json.load(f)["objects"], allow_custom=True)
    print("done")

    print("loading mappings... ", end="", flush=True)
    with open(args.mappings, "r") as f:
        mappings = MemoryStore(stix_data=json.load(f)["objects"])
    print("done")

    
    print("generating layers... ", end="", flush=True)
    layers = getFrameworkOverviewLayers(controls, mappings, attackdata, args.domain, args.framework)
    for property in get_x_mitre(controls): # iterate over all custom properties as potential layer-generation material
        if property == "x_mitre_family": continue
        layers += getLayersByProperty(controls, mappings, attackdata, args.domain, args.framework, property)
    print("done")

    if args.clear:
        print("clearing layers directory...", end="", flush=True)
        shutil.rmtree(args.output)
        print("done")
    
    print("writing layers... ", end="", flush=True)
    for layer in layers:
        # make path if it doesn't exist
        layerdir = os.path.dirname(os.path.join(args.output, layer["outfile"]))
        if not os.path.exists(layerdir):
            os.makedirs(layerdir)
        # write layer
        with open(os.path.join(args.output, layer["outfile"]), "w") as f:
            json.dump(layer["layer"], f)
    print("done")