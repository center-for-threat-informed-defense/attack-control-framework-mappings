import argparse
import json
import os

from colorama import Fore
from stix2.v20 import Bundle
import openpyxl
import openpyxl.utils
import pandas
import requests


def mappings_to_df(attack_bundle, controls_bundle, mappings_bundle):
    """Return a pandas dataframe listing the mappings in mappings_bundle"""
    rows = []
    for mapping in mappings_bundle.objects:
        control = controls_bundle.get(mapping.source_ref)
        if not control:
            print(Fore.RED + f"ERROR: cannot find object with ID {mapping.source_ref} in controls bundle" + Fore.RESET)
            exit()
        else:
            control = control[0]

        technique = attack_bundle.get(mapping.target_ref)
        if not technique:
            print(Fore.RED + f"ERROR: cannot find object with ID {mapping.target_ref} in ATT&CK bundle" + Fore.RESET)
            exit()
        else:
            technique = technique[0]

        rows.append({
            "Control ID": control["external_references"][0]["external_id"],
            "Control Name": control["name"],
            "Mapping Type": mapping["relationship_type"],
            "Technique ID": technique["external_references"][0]["external_id"],
            "Technique Name": technique["name"],
        })

    data_frame = pandas.DataFrame(rows)
    data_frame.sort_values(['Control ID', 'Technique ID'], ascending=[True, True], inplace=True)

    return data_frame


def workbook_changes(filename):
    """Changes spreadsheet format width, freezes first row, and sets
    filtering reference"""
    sheet_name = 'Sheet1'
    freeze_row = 'A2'  # freezes the first row of the document

    control_id_width = 14
    control_name_width = 69
    mapping_type_width = 18
    technique_id_width = 18
    technique_name_width = 58

    column_widths = [
        control_id_width,
        control_name_width,
        mapping_type_width,
        technique_id_width,
        technique_name_width,
    ]

    workbook = openpyxl.load_workbook(filename)
    worksheet = workbook[sheet_name]
    worksheet.freeze_panes = worksheet[freeze_row]

    # establishes filtering references in document
    auto_filter_section = f'A1:E{len(list(worksheet.rows))}'
    worksheet.auto_filter.ref = auto_filter_section

    for i, column_width in enumerate(column_widths):
        worksheet.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = column_width

    workbook.save(filename)


def main(controls, mappings, domain, version, output):
    extensionToPDExport = {
        "xlsx": "to_excel",  # extension to df export function name
        "csv": "to_csv",
        "html": "to_html",
        "md": "to_markdown",
    }
    allowedExtensionList = ", ".join(extensionToPDExport.keys())

    if version != "v9.0":
        controls = controls.replace("attack_9_0", f"ATT&CK-{version}")
        mappings = mappings.replace("attack_9_0", f"ATT&CK-{version}")
        output = output.replace("attack_9_0", f"ATT&CK-{version}")

    extension = output.split(".")[-1]
    if extension not in extensionToPDExport:
        msg = (f"ERROR: Unknown output extension \"{extension}\", please make "
               f"sure your output extension is one of: {allowedExtensionList}")
        print(Fore.RED + msg, Fore.reset)
        exit()

    print("downloading ATT&CK data... ", end="", flush=True)
    url = f"https://raw.githubusercontent.com/mitre/cti/ATT%26CK-{version}/{domain}/{domain}.json"
    attack_data = Bundle(
        requests.get(url, verify=True).json()["objects"],
        allow_custom=True
    )
    print("done")

    print("loading controls framework... ", end="", flush=True)
    with open(controls, "r") as f:
        controls = Bundle(json.load(f)["objects"], allow_custom=True)
    print("done")

    print("loading mappings... ", end="", flush=True)
    with open(mappings, "r") as f:
        mappings = Bundle(json.load(f)["objects"])
    df = mappings_to_df(attack_data, controls, mappings)
    print("done")

    print(f"writing {output}...", end="", flush=True)
    if extension in ["md"]:  # md doesn't support index=False and requires a stream and not a path
        with open(output, "w") as f:
            getattr(df, extensionToPDExport[extension])(f)
    else:
        getattr(df, extensionToPDExport[extension])(output, index=False)

        if extension in ["xlsx"]:
            workbook_changes(output)

        print("done")
