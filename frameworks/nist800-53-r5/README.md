# NIST 800-53 Revision 5 Control Mappings
| Mappings Version | Last Updated      | Scope    | ATT&CK Version | ATT&CK Domain |
|------------------|-------------------|----------|----------------|---------------|
| 0.1              | 13 May 2020       | (WIP)      | [ATT&CK v7.0-beta](https://attack.mitre.org/resources/versions/) | Enterprise |

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

During the analysis and mapping of ATT&CK techniques and sub-techniques to NIST 800-53 revision 5 controls, several decision points were made regarding applicability and relevance. Specifically, the following was considered as part of the decision points:

- This effort is focused on the technical and operational elements of NIST 800-53 and did not take into account the management elements that are often focused on organization specific policies and procedures.  This decision was made because management specific controls are policy-based, and the intent of this effort was focusing on technical and operation controls that correlate to ATT&CK mitigations, techniques, and sub-techniques.   
- During the NIST 800-53 control analysis, the context of the prescribed mitigation for a given technique or sub-technique was important to refine and select specific controls within a given control family.  This helped narrow the search space during security control analysis as each control family contains specific security controls related to the broader general security topic of the family.  
- At the time of the security control mappings to revision 5, NIST 800-53B - Control Baselines for Information Systems and Organizations was still in draft form and was not used in security control analysis to formulate candidate list of security controls.    
