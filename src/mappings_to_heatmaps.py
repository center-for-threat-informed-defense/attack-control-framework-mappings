import argparse
import json
import os
import re
import shutil
import urllib.parse

from stix2 import Filter, MemoryStore
import requests


def technique(attack_id, mapped_controls):
    """create a technique for a layer"""
    return {
        "techniqueID": attack_id,
        "score": len(mapped_controls),  # count of mapped controls
        "comment": f"Mitigated by {', '.join(sorted(mapped_controls))}",  # list of mapped controls
    }


def create_layer(name, description, domain, techniques, version):
    """create a Layer"""
    min_mappings = min(map(lambda t: t["score"], techniques)) if len(techniques) > 0 else 0
    max_mappings = max(map(lambda t: t["score"], techniques)) if len(techniques) > 0 else 100
    gradient = ["#ACD0E6", "#08336E"]
    # check if all the same count of mappings
    if max_mappings - min_mappings == 0:
        min_mappings = 0  # set low end of gradient to 0
        gradient = ["#ffffff", "#66b1ff"]

    # convert version to just major version
    if version.startswith("v"):
        version = version[1:]
    version = version.split(".")[0]

    return {
        "name": name,
        "versions": {
            "navigator": "4.3",
            "layer": "4.2",
            "attack": version
        },
        "sorting": 3,  # descending order of score
        "description": description,
        "domain": domain,
        "techniques": techniques,
        "gradient": {
            "colors": gradient,
            "minValue": min_mappings,
            "maxValue": max_mappings
        },
    }


def parse_family_data(controls):
    """ingest control data to return family_id_to_controls mapping and family_id_to_name mapping"""
    id_to_family = re.compile(r"(\w+)-.*")

    family_id_to_controls = {}  # family ID to control object
    family_id_to_name = {}
    for control in controls.query([Filter("type", "=", "course-of-action")]):
        # parse family ID from control external ID
        family_id = id_to_family.search(control["external_references"][0]["external_id"]).groups()[0]
        if family_id not in family_id_to_controls:
            family_id_to_controls[family_id] = [control]
        else:
            family_id_to_controls[family_id].append(control)
        # parse family name if possible, or just use family ID if not
        if "x_mitre_family" in control:
            family_id_to_name[family_id] = control["x_mitre_family"]
        else:
            family_id_to_name[family_id] = family_id

    return family_id_to_controls, family_id_to_name, id_to_family


def to_technique_list(controls, mappings, attackdata, family_id_to_controls, family_id_to_name, id_to_family):
    """take a controls ms, a mappings ms, and attack_data ms
    return a list of Techniques where the score is the number of controls that map to the technique"""
    technique_to_mapped_controls = {}
    for mapping in mappings.query():
        # source_ref is the control in controls
        if not controls.get(mapping["source_ref"]):
            continue  # mapping not relevant to this list of controls
        control_id = controls.get(mapping["source_ref"])["external_references"][0]["external_id"]
        # target_ref is the technique in attack_data
        attack_id = attackdata.get(mapping["target_ref"])["external_references"][0]["external_id"]
        # build the mapping
        if attack_id in technique_to_mapped_controls:
            technique_to_mapped_controls[attack_id].append(control_id)
        else:
            technique_to_mapped_controls[attack_id] = [control_id]

    # collapse families where all controls are mapped; list just the family identifier
    for attack_id in technique_to_mapped_controls:
        control_ids = technique_to_mapped_controls[attack_id]
        # Group mapped controls for this technique according to the family
        families = {}
        for cid in control_ids:
            family_id = id_to_family.search(cid).groups()[0]
            if family_id not in families:
                families[family_id] = {cid}  # new set
            else:
                families[family_id].add(cid)  # add to set

        # are all controls in the family mapped?
        collapsed_controls = []
        for family_id in families:
            family_set = families[family_id]
            controls_in_family = set(map(lambda c: c["external_references"][0]["external_id"],
                                         family_id_to_controls[family_id]))
            if family_set == controls_in_family:  # all controls in family mapped?
                # collapse
                collapsed_controls.append(f"all '{family_id_to_name[family_id]}' controls")
            else:
                collapsed_controls += control_ids
        technique_to_mapped_controls[attack_id] = collapsed_controls

    # remove duplicate mappings
    for attack_id in technique_to_mapped_controls:
        technique_to_mapped_controls[attack_id] = list(set(technique_to_mapped_controls[attack_id]))

    # transform to techniques
    return [technique(attack_id, technique_to_mapped_controls[attack_id])
            for attack_id in technique_to_mapped_controls]


def get_framework_overview_layers(controls, mappings, attack_data, domain, framework_name, version):
    """ingest mappings and controls and attack_data, and return an array of layer jsons for layers
     according to control family"""
    # build list of control families
    family_id_to_controls, family_id_to_name, id_to_family = parse_family_data(controls)

    out_layers = [
        {
            "outfile": f"{framework_name}-overview.json",
            "layer": create_layer(
                f"{framework_name} overview",
                f"{framework_name} heatmap overview of control mappings, where scores are "
                f"the number of associated controls",
                domain,
                to_technique_list(controls, mappings, attack_data, family_id_to_controls,
                                  family_id_to_name, id_to_family),
                version
            )
        }
    ]
    for family_id in family_id_to_controls:
        controls_in_family = MemoryStore(stix_data=family_id_to_controls[family_id])
        techniques_in_family = to_technique_list(controls_in_family, mappings, attack_data,
                                                 family_id_to_controls, family_id_to_name, id_to_family)
        if len(techniques_in_family) > 0:  # don't build heatmaps with no mappings
            # build family overview mapping
            out_layers.append({
                "outfile": os.path.join("by_family",
                                        family_id_to_name[family_id].replace(" ", "_"),
                                        f"{family_id}-overview.json"),
                "layer": create_layer(
                    f"{family_id_to_name[family_id]} overview",
                    f"{framework_name} heatmap for controls in the {family_id_to_name[family_id]} family, "
                    f"where scores are the number of associated controls",
                    domain,
                    techniques_in_family,
                    version
                )
            })
            # build layer for each control
            for control in family_id_to_controls[family_id]:
                control_ms = MemoryStore(stix_data=control)
                control_id = control["external_references"][0]["external_id"]
                techniques_mapped_to_control = to_technique_list(control_ms, mappings, attack_data,
                                                                 family_id_to_controls, family_id_to_name, id_to_family)
                if len(techniques_mapped_to_control) > 0:  # don't build heatmaps with no mappings
                    out_layers.append({
                        "outfile": os.path.join("by_family",
                                                family_id_to_name[family_id].replace(" ", "_"),
                                                f"{'_'.join(control_id.split(' '))}.json"),
                        "layer": create_layer(
                            f"{control_id} mappings",
                            f"{framework_name} {control_id} mappings",
                            domain,
                            techniques_mapped_to_control,
                            version
                        )
                    })

    return out_layers


def get_layers_by_property(controls, mappings, attack_data, domain, framework_name, x_mitre, version):
    """get layers grouping the mappings according to values of the given property"""
    property_name = x_mitre.split("x_mitre_")[1]  # remove prefix
    family_id_to_controls, family_id_to_name, id_to_family = parse_family_data(controls)

    # group controls by the property
    property_value_to_controls = {}

    def add_to_dict(value, control):
        if value in property_value_to_controls:
            property_value_to_controls[value].append(control)
        else:
            property_value_to_controls[value] = [control]

    # iterate through controls, grouping by property
    is_list_type = False
    for control in controls.query([Filter("type", "=", "course-of-action")]):
        value = control.get(x_mitre)
        if not value:
            continue
        if isinstance(value, list):
            is_list_type = True
            for v in value:
                add_to_dict(v, control)
        else:
            add_to_dict(value, control)

    out_layers = []
    for value in property_value_to_controls:
        # controls for the corresponding values
        controls_of_value = MemoryStore(stix_data=property_value_to_controls[value])
        techniques = to_technique_list(controls_of_value, mappings, attack_data,
                                       family_id_to_controls, family_id_to_name, id_to_family)
        if len(techniques) > 0:
            # build layer for this technique set
            out_layers.append({
                "outfile": os.path.join(f"by_{property_name}", f"{value}.json"),
                "layer": create_layer(
                    f"{property_name}={value} mappings",
                    f"techniques where the {property_name} of associated controls "
                    f"{'includes' if is_list_type else 'is'} {value}",
                    domain,
                    techniques,
                    version
                )
            })

    return out_layers


def get_x_mitre(ms, object_type="course-of-action"):
    """return a list of all x_mitre_ properties defined on the given type"""
    keys = set()
    for obj in ms.query([Filter("type", "=", object_type)]):
        for key in obj:
            if key.startswith("x_mitre_"):
                keys.add(key)
    return keys


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create ATT&CK Navigator layers from control mappings")
    parser.add_argument("-framework",
                        help="the name of the control framework",
                        default="nist800_53_r4")
    parser.add_argument("-controls",
                        dest="controls",
                        help="filepath to the stix bundle representing the control framework",
                        default=os.path.join("..", "frameworks", "attack_9_0", "nist800_53_r4",
                                             "stix", "nist800_53_r4-controls.json"))
    parser.add_argument("-mappings",
                        dest="mappings",
                        help="filepath to the stix bundle mapping the controls to ATT&CK",
                        default=os.path.join("..", "frameworks", "attack_9_0", "nist800_53_r4",
                                             "stix", "nist800_53_r4-mappings.json"))
    parser.add_argument("-domain",
                        choices=["enterprise-attack", "mobile-attack"],
                        help="the domain of ATT&CK to visualize",
                        default="enterprise-attack")
    parser.add_argument("-version",
                        dest="version",
                        help="which ATT&CK version to use",
                        default="v9.0")
    parser.add_argument("-output",
                        help="folder to write output layers to",
                        default=os.path.join("..", "frameworks", "attack_9_0", "nist800_53_r4", "layers"))
    parser.add_argument("--clear",
                        action="store_true",
                        help="if flag specified, will remove the contents the output folder before writing layers")
    parser.add_argument("--build-directory",
                        dest="build_dir",
                        action="store_true",
                        help="if flag specified, will build a markdown file listing the output files for easy "
                             "access in the Navigator")

    args = parser.parse_args()

    if args.version != "v9.0":
        args.controls = args.controls.replace("attack_9_0", f"ATT&CK-{args.version}")
        args.mappings = args.mappings.replace("attack_9_0", f"ATT&CK-{args.version}")
        args.output = args.output.replace("attack_9_0", f"ATT&CK-{args.version}")

    print("downloading ATT&CK data... ", end="", flush=True)
    url = f"https://raw.githubusercontent.com/mitre/cti/ATT%26CK-{args.version}/{args.domain}/{args.domain}.json"
    attack_data = MemoryStore(stix_data=requests.get(url, verify=True).json()["objects"])
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
    layers = get_framework_overview_layers(controls, mappings, attack_data, args.domain, args.framework, args.version)
    for p in get_x_mitre(controls):  # iterate over all custom properties as potential layer-generation material
        if p == "x_mitre_family":
            continue
        layers += get_layers_by_property(controls, mappings, attack_data, args.domain, args.framework, p, args.version)
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
    if args.build_dir:
        print("writing layer directory markdown... ", end="", flush=True)

        mdfile_lines = [
            "# ATT&CK Navigator Layers",
            "",  # "" is an empty line
            f"The following [ATT&CK Navigator](https://github.com/mitre-attack/attack-navigator/) layers "
            f"represent the mappings from ATT&CK to {args.framework}:",
            "",
        ]
        prefix = (f"https://raw.githubusercontent.com/center-for-threat-informed-defense/"
                  f"attack-control-framework-mappings/main/frameworks/ATT&CK-{args.version}")
        nav_prefix = "https://mitre-attack.github.io/attack-navigator/#layerURL="

        for layer in layers:
            if "/" in layer["outfile"]:  # force URL delimiters even if local system uses "\"
                pathParts = layer["outfile"].split("/")
            else:
                pathParts = layer["outfile"].split("\\")

            depth = len(pathParts) - 1  # how many subdirectories deep is it?
            layer_name = layer['layer']['name']
            if layer_name.endswith("overview"):
                depth = max(0, depth - 1)  # overviews get un-indented
            path = [prefix] + [args.framework, "layers"] + pathParts
            path = "/".join(path)
            encodedPath = urllib.parse.quote(path, safe='~()*!.\'')  # encode the url for the query string
            md_line = f"{'    ' * depth}- {layer_name} ( [download]({path}) | [view]({nav_prefix}{encodedPath}) )"
            mdfile_lines.append(md_line)

        with open(os.path.join(args.output, "README.md"), "w") as f:
            f.write("\n".join(mdfile_lines))

        print("done")
