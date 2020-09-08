# NIST 800-53 Revision 4 Control Mappings

This folder contains data and parsers for the NIST 800-53 Revision 4 control framework, and the mappings of that framework to ATT&CK.

To build the framework from the input data, run `python3 parse.py`.

- The [input](data) folder contains the input spreadsheets. See the README in that folder for more information.
- The [stix](stix) folder contains the output STIX2.0 json data. See the README in that folder for more information.
- The [layers](layers) folder contains [ATT&CK Navigator](https://github.com/mitre-attack/attack-navigator) layers showing the mappings in the context of the ATT&CK Matrix.
- The [nist800-53-r4-mappings.xlsx](nist800-53-r4-mappings.xlsx) spreadsheet lists all of the mappings for this control framework. It differs from the input mappings spreadsheet in that it provides additional context for each mapping, and it is not encoded in the regex shorthand.

## Extended Fields

The Nist 800-53 Revision 4 STIX data extends the controls format with the following properties:

| STIX field | type | description |
|:-----------|:-----|:------------|
| `x_mitre_impact` | list of strings | the baseline-impact of the control or enhancement. Values include `"LOW"`, `"MODERATE"`, `"HIGH"`. |
| `x_mitre_family` | string | The family to which the control belongs. |
| `x_mitre_priority` | string | The priority of the control. Control enhancements inherit this value from their parent control. |

## Mappings Methodology

Section TODO