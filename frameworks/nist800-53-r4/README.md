# NIST 800-53 Revision 4 Control Mappings
This folder contains data and parsers for the NIST 800-53 Revision 4 control framework, and the mappings of that framework to ATT&CK.

| Mappings Version | Last Updated      | Scope    | ATT&CK Version | ATT&CK Domain |
|------------------|-------------------|----------|----------------|---------------|
| 1.1              | 8 October 2020    | Partial<sup>[1]</sup> | [ATT&CK v7](https://attack.mitre.org/resources/versions/) | Enterprise |

[1] This initial release of security control mappings includes all the techniques and sub-techniques associated with the following mitigations: M1036, M1015, M1049, M1013, M1048, M1047, M1040, M1046, M1045, M1043, M1053, M1042, M1041,  M1039, M1038, M1050 and M1037.

| Data ||
|------|------|
| [spreadsheet](nist800-53-r4-mappings.xlsx) | Lists all of the mappings for this control framework.
| [layers](layers) | [ATT&CK Navigator](https://github.com/mitre-attack/attack-navigator) layers showing the mappings in the context of the ATT&CK Matrix. |
| [stix](stix) | Output STIX 2.0 json data. See the README in that folder for more information. |
| [input](input) | Input spreadsheets from which the STIX is built. To rebuild the STIX data from the input spreadsheets, run `python3 parse.py`.See the README in that folder for more information. |


## Extended Fields

The NIST 800-53 Revision 4 STIX data extends the [general controls format](/docs/stix_format.md) with the following properties:

| STIX field | type | description |
|:-----------|:-----|:------------|
| `x_mitre_impact` | list of strings | the baseline-impact of the control or enhancement. Values include `"LOW"`, `"MODERATE"`, `"HIGH"`. |
| `x_mitre_family` | string | The family to which the control belongs. |
| `x_mitre_priority` | string | The priority of the control. Control enhancements inherit this value from their parent control. |

## Mapping NIST 800-53 revision 4 to ATT&CK

During the analysis and mapping of ATT&CK techniques and sub-techniques to NIST 800-53 revision 4 controls, several decision points were made regarding applicability and relevance. Specifically, the following was considered as part of the decision points:


** DOCUMENT SCOPE HERE

- This effort is focused on the technical and operational elements of NIST 800-53 and did not take into account the management elements that are often focused on organization specific policies and procedures.  This decision was made because management specific controls are policy-based, and the intent of this effort was focusing on technical and operation controls that correlate to ATT&CK mitigations, techniques, and sub-techniques.   
- During the NIST 800-53 control analysis, the context of the prescribed mitigation for a given technique or sub-technique was important to refine and select specific controls within a given control family.  This helped narrow the search space during security control analysis as each control family contains specific security controls related to the broader general security topic of the family.  
