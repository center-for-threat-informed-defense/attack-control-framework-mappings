# NIST 800-53 Revision 5 Control Mappings

This folder contains data and parsers for the NIST 800-53 Revision 5 control framework, and the mappings of that framework to ATT&CK.

To build the framework from the input data, run `python3 parse.py`.

- The [input](data) folder contains the input spreadsheets. See the README in that folder for more information.
- The [stix](stix) folder contains the output STIX2.0 json data. See the README in that folder for more information.
- The [layers](layers) folder contains [ATT&CK Navigator](https://github.com/mitre-attack/attack-navigator) layers showing the mappings in the context of the ATT&CK Matrix.
- The [nist800-53-r5-mappings.xlsx](nist800-53-r5-mappings.xlsx) spreadsheet lists all of the mappings for this control framework. It differs from the input mappings spreadsheet in that it provides additional context for each mapping, and it is not encoded in the regex shorthand.

## Extended Fields

The Nist 800-53 Revision 5 STIX data does not extend the controls format with any additional properties.

## Mappings Methodology

Section TODO