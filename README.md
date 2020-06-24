# ATT&CK Control Mappings
This repository includes tools and data for mapping control frameworks to MITRE ATT&amp;CK. In addition to mapping the frameworks, it defines a common STIX2.0 representation for control frameworks &mdash; see [output data](#output-data), below.

See also:
- [USE-CASES](USE-CASES.md) for common use cases of the controls framework data
- [CHANGELOG](CHANGELOG.md) to learn about recent changes to this repository
- [CONTRIBUTING](CONTRIBUTING.md) for information about how to contribute controls, mappings, or other improvements

# Usage

This repository provides data representing control frameworks, and mappings from said frameworks to ATT&CK, in STIX2.0 JSON. You can find the data for those frameworks in the `/frameworks/` folder:
- [NIST 800-53 Revision 4](frameworks/nist800-53-r4/)
- [NIST 800-53 Revision 5](frameworks/nist800-53-r5/)

Each framework folder includes the framework and mapping data in a `/data/` folder, and ATT&CK Navigator Layers in the `/layers/` folder. The [install](#install) section below explains how to set up this repository for local use if you intend to extend the defined mappings.


## Input Data
Each control framework has one input for the controls and one for the mappings. The controls input is generally supplied by the organization publishing the controls in the first place. The mappings were created as part of this project. 

## Framework Parser

<img src="docs/parser_overview.png" width="720px">

*Above: overview of the parser structure*

The controls parser consists of two major parts, `parse_controls.py` and the `parse_mappings.py`. These are coupled together with `parse.py` which performs both operations sequentially. 
- `parse_controls.py` takes as input the controls spreadsheet and builds a STIX2.0 representation of the control framework. Because the representation of each control framework differs, this script will likely have to be rewritten for each additional control framework since the input data format is not standardized.
- `parse_mappings.py` takes as input the mappings spreadsheet, and the STIX representation of the control framework and builds a STIX2.0 representation of the mappings to ATT&CK. Because the input mappings file format can be standardized, this parser can often be reused when adding additional control frameworks.

## Output Data

The controls parser system outlined above produces a series of STIX2.0 bundles representing the controls framework as well as mappings to ATT&CK. See the README of the data folder for a given framework for a description of each file:
- [NIST 800-53 Revision 4](frameworks/nist800-53-r4/data/)
- [NIST 800-53 Revision 5](frameworks/nist800-53-r5/data/)

The general format is as follows:
- Both controls and mappings are represented in STIX2.0 JSON.
- Controls are represented as [course-of-actions](https://docs.oasis-open.org/cti/stix/v2.0/csprd01/part2-stix-objects/stix-v2.0-csprd01-part2-stix-objects.html#_Toc476230929).
- The hierarchy of the control framework is also represented in the STIX. Relationships of type `subcontrol-of` map sub-controls to their parent controls for frameworks which have hierarchical controls. 
- `x_mitre_` properties are added to control `course-of-action` objects for additional properties depending on the control framework, such as the control family (`x_mitre_family`) or control priority (`x_mitre_priority`). These additional properties are not standardized across control frameworks, and are described in the README of each control framework.
- Mappings from individual controls to ATT&CK techniques and sub-techniques are represented as [relationships](https://docs.oasis-open.org/cti/stix/v2.0/csprd01/part2-stix-objects/stix-v2.0-csprd01-part2-stix-objects.html#_Toc476230970) of type `mitigates`, where the `source_ref` is the `id` of the control and the `target_ref` is the `id` of the technique or sub-technique. The optional `description` field on the relationship is taken from the input spreadsheet if a description is given there, and is used to justify the mapping of the control.

## Utility Scripts

The [/util/](util/) folder includes utility scripts designed to work with generic control frameworks and mappings that implement the format described [above](#output-data). Please see the readme in the util folder for more details of the functionality of these scripts.

# Install
## Requirements

- [python](https://www.python.org/) 3.6 or greater

## Environment Setup

1. Create a virtual environment: 
    - macOS and Linux: `python3 -m venv env`
    - Windows: `py -m venv env`
2. Activate the virtual environment: 
    - macOS and Linux: `source env/bin/activate`
    - Windows: `env/Scripts/activate.bat`
3. Install requirement packages: `pip3 install -r requirements.txt`

## Rebuild the STIX data

To rebuild all the data in the repository based on the most up-to-date input data, run `python3 make.py`.

To rebuild the STIX data for a specific control framework:
1. run `python3 parser.py` from within the folder of the given control framework. This will rebuild the raw STIX data from the input spreadsheets.
2. Then use the scripts in [util](util/) to regenerate the ancillary control data such as ATT&CK Navigator layers.
