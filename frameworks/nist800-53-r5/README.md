# NIST 800-53 Revision 5 Control Mappings
| Mappings Version | Last Updated      | Scope    | ATT&CK Version | ATT&CK Domain |
|------------------|-------------------|----------|----------------|---------------|
| 1.0              | 8 October 2020    | Complete | [ATT&CK v7](https://attack.mitre.org/resources/versions/) | Enterprise |

This folder contains data and parsers for the NIST 800-53 Revision 5 control framework, and the mappings of that framework to ATT&CK.

| Data ||
|------|------|
| [spreadsheet](nist800-53-r5-mappings.xlsx) | Lists all of the mappings for this control framework.
| [layers](layers) | [ATT&CK Navigator](https://github.com/mitre-attack/attack-navigator) layers showing the mappings in the context of the ATT&CK Matrix. |
| [stix](stix) | Output STIX 2.0 json data. See the README in that folder for more information. |
| [input](input) | Input spreadsheets from which the STIX is built. To rebuild the STIX data from the input spreadsheets, run `python3 parse.py`.See the README in that folder for more information. |

## Extended Fields

The NIST 800-53 Revision 5 STIX data does not extend the [general controls format](/docs/stix_format.md) with any additional properties.

## Mapping NIST 800-53 revision 5 to ATT&CK

Section TODO
