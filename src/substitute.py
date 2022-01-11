import json
import os
import uuid


def save_bundle(bundle, path):
    """helper function to write a STIX bundle to file"""
    print(f"{'overwriting' if os.path.exists(path) else 'writing'} {path}... ", end="", flush=True)
    with open(path, "w", encoding="utf-8") as outfile:
        json.dump(bundle, outfile, indent=4, sort_keys=True, ensure_ascii=False)
    print("done")


def substitute(attack_bundle, controls_bundle, mappings_bundle, allow_unmapped=False):
    """substitute the controls bundle and mappings bundle for the mitigations in attack_bundle.
    attack_bundle, controls_bundle and mappings_bundle are of type stix2.Bundle
    allow_unmapped, if true, allows controls in the output bundle if they don't have mappings to ATT&CK techniques
    Returns a new bundle resembling attack_bundle but with mitigations and mitigates relationships
    from controls_bundle and mappings_bundle
    """
    # add attack data which are not mitigations or mitigation relationships
    out_objects = [
        sdo
        for sdo in attack_bundle
        if (sdo["type"] != "course-of-action" and
            not (sdo["type"] == "relationship" and sdo["relationship_type"] == "mitigates"))
    ]
    if allow_unmapped:  # add all controls
        out_objects.extend(controls_bundle)
    else:  # add only controls which have associated mappings
        used_ids = set()
        for mapping in mappings_bundle:
            used_ids.add(mapping["source_ref"])
        out_objects.extend([sdo for sdo in controls_bundle if sdo["id"] in used_ids])
    # add mappings
    out_objects.extend(mappings_bundle)

    return {
        "type": "bundle",
        "id": f"bundle--{uuid.uuid4()}",
        "spec_version": "2.0",
        "objects": out_objects,
    }


def main(attack, controls, mappings, allow_unmapped, output):
    print("loading ATT&CK data... ", end="", flush=True)
    with open(attack, "r") as f:
        attack = json.load(f)["objects"]
    print("done")

    print("loading controls framework... ", end="", flush=True)
    with open(controls, "r") as f:
        controls = json.load(f)["objects"]
    print("done")

    print("loading mappings... ", end="", flush=True)
    with open(mappings, "r") as f:
        mappings = json.load(f)["objects"]
    print("done")

    print("substituting... ", end="", flush=True)
    out_bundle = substitute(attack, controls, mappings, allow_unmapped)
    print("done")

    save_bundle(out_bundle, output)
