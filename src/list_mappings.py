from colorama import Fore
import openpyxl
import openpyxl.utils
import pandas


def mappings_to_df(mappings_bundle, stixid_to_object):
    """Return a pandas dataframe listing the mappings in mappings_bundle"""
    rows = []
    for mapping in mappings_bundle:
        control = stixid_to_object.get(mapping["source_ref"])
        if not control:
            print(Fore.RED + f"ERROR: cannot find object with ID {mapping.source_ref} in controls bundle" + Fore.RESET)
            exit()

        technique = stixid_to_object.get(mapping["target_ref"])
        if not technique:
            print(Fore.RED + f"ERROR: cannot find object with ID {mapping.target_ref} in ATT&CK bundle" + Fore.RESET)
            exit()

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


def main(attack_data, controls, mappings, output):
    extension_to_pd_export = {
        ".xlsx": "to_excel",  # extension to df export function name
        ".csv": "to_csv",
        ".html": "to_html",
        ".md": "to_markdown",
    }
    allowed_extension_list = ", ".join(extension_to_pd_export.keys())
    file_extension = output.suffix
    if file_extension not in extension_to_pd_export:
        msg = (f"ERROR: Unknown output extension \"{file_extension}\", please make "
               f"sure your output extension is one of: {allowed_extension_list}")
        print(Fore.RED + msg + Fore.RESET)
        exit()

    stixid_to_object = {obj["id"]: obj for obj in attack_data}
    stixid_to_object.update({obj["id"]: obj for obj in controls})

    df = mappings_to_df(mappings, stixid_to_object)

    print(f"writing {output}... ", end="", flush=True)
    if file_extension in [".md"]:  # md doesn't support index=False and requires a stream and not a path
        with open(output, "w") as f:
            getattr(df, extension_to_pd_export[file_extension])(f)
    else:
        getattr(df, extension_to_pd_export[file_extension])(output, index=False)

        if file_extension in [".xlsx"]:
            workbook_changes(output)

        print("done")
