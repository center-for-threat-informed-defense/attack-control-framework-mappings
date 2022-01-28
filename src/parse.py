import json
import os

from parse_mappings import parse_mappings
import parse_r4_controls
import parse_r5_controls


def save_bundle(bundle, path):
    """helper function to write a STIX bundle to file"""
    print(f"{'overwriting' if os.path.exists(path) else 'writing'} {path}... ", end="", flush=True)
    with open(path, "w", encoding="utf-8") as outfile:
        bundle.fp_serialize(outfile, indent=4, sort_keys=True, ensure_ascii=False)
    print("done")


def main(in_controls,
         in_mappings,
         out_controls,
         out_mappings,
         framework_id,
         attack_data):
    """
    parse the NIST 800-53 controls and ATT&CK mappings into STIX2.0 bundles
    :param in_controls: tsv file of NIST 800-53 revision 4 controls
    :param in_mappings: tsv file mapping NIST 800-53 revision 4 controls to ATT&CK
    :param out_controls: output STIX bundle file for the controls. If this file already exists,
                         the STIX IDs within will be reused in the replacing file so that they
                         don't change between consecutive executions of this script.
    :param out_mappings: output STIX bundle file for the mappings.
    :param framework_id: the framework id - e.g., "NIST 800-53 Revision 4"
    :param attack_data: ATT&CK content.

    :returns tuple: containing the output controls and mappings (out_controls, out_mappings)
    """

    # build control ID helper lookups so that STIX IDs don't get replaced on each rebuild
    control_ids = {}
    control_relationship_ids = {"subcontrol-of": {}, "related-to": {}}
    if os.path.exists(out_controls):
        # parse idMappings from existing output so that IDs don't change when regenerated
        with open(out_controls, "r") as f:
            bundle = json.load(f)
        for sdo in bundle["objects"]:
            if not sdo["type"] == "relationship":
                from_id = sdo["external_references"][0]["external_id"]
                to_id = sdo["id"]
                control_ids[from_id] = to_id
            else:
                # parse relationships
                from_ids = f"{sdo['source_ref']}---{sdo['target_ref']}"
                to_id = sdo["id"]
                rel_type = sdo["relationship_type"]
                control_relationship_ids[rel_type][from_ids] = to_id

    # build controls in STIX
    if framework_id == "NIST 800-53 Revision 4":
        parse_controls = parse_r4_controls.parse_controls
    elif framework_id == "NIST 800-53 Revision 5":
        parse_controls = parse_r5_controls.parse_controls
    else:
        raise ValueError(f"Unknown framework_id \"{framework_id}\"")

    controls = parse_controls(
        in_controls,
        control_ids,
        control_relationship_ids,
        framework_id,
    )

    # build mapping ID helper lookup so that STIX IDs don't get replaced on each rebuild
    mapping_relationship_ids = {}
    if os.path.exists(out_mappings):
        with open(out_mappings, "r") as f:
            bundle = json.load(f)
        for sdo in bundle["objects"]:
            from_ids = f"{sdo['source_ref']}---{sdo['target_ref']}"
            to_id = sdo["id"]
            mapping_relationship_ids[from_ids] = to_id

    # build mappings in STIX
    mappings = parse_mappings(
        in_mappings,
        controls,
        mapping_relationship_ids,
        attack_data,
    )

    save_bundle(controls, out_controls)
    save_bundle(mappings, out_mappings)

    return out_controls, out_mappings
