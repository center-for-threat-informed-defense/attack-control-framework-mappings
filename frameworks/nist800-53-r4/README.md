# NIST 800-53 Revision 4 Control Mappings

This folder contains data and parsers for the NIST 800-53 Revision 4 control framework, and the mappings of that framework to ATT&CK.

To build the framework from the input data, run `python3 parse.py`.

- The [data](data) folder contains the input spreadsheets and output STIX2.0 json data. See the README in that folder for more information.
- The [layers](layers) folder contains [ATT&CK Navigator](https://github.com/mitre-attack/attack-navigator) layers showing the mappings in the context of the ATT&CK Matrix.