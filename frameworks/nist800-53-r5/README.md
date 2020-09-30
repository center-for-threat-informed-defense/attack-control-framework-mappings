# NIST 800-53 Revision 5 Control Mappings

This folder contains data and parsers for the NIST 800-53 Revision 5 control framework, and the mappings of that framework to ATT&CK.

| Data ||||
|------|------|------|--|
| [spreadsheet](nist800-53-r5-mappings.xlsx) | Lists all of the mappings for this control framework.
| [layers](layers) | [ATT&CK Navigator](https://github.com/mitre-attack/attack-navigator) layers showing the mappings in the context of the ATT&CK Matrix. |
| [stix](stix) | Output STIX 2.0 json data. See the README in that folder for more information. |
| [input](input) | Input spreadsheets from which the STIX is built. To rebuild the STIX data from the input spreadsheets, run `python3 parse.py`.See the README in that folder for more information. |

## Extended Fields

The NIST 800-53 Revision 5 STIX data does not extend the controls format with any additional properties.

## Mappings Methodology

Section TODO
