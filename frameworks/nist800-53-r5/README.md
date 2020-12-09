# NIST 800-53 Revision 5 Control Mappings
This folder contains data and parsers for the NIST 800-53 Revision 5 control framework, and the mappings of that framework to MITRE ATT&CK.

| Mappings Version | Last Updated      | ATT&CK Version | ATT&CK Domain |
|------------------|-------------------|----------------|---------------|
| 1.0              | 15 December 2020  | [ATT&CK v8](https://attack.mitre.org/resources/versions/) | Enterprise |


| Data ||
|------|------|
| [spreadsheet](nist800-53-r5-mappings.xlsx) | Lists all of the mappings for this control framework.
| [layers](layers) | [ATT&CK Navigator](https://github.com/mitre-attack/attack-navigator) layers showing the mappings in the context of the ATT&CK Matrix. |
| [stix](stix) | Output STIX 2.0 json data. See the README in that folder for more information. |
| [input](input) | Input spreadsheets from which the STIX is built. To rebuild the STIX data from the input spreadsheets, run `python3 parse.py`.See the README in that folder for more information. |

## Extended Fields

The NIST 800-53 Revision 5 STIX data does not extend the [general controls format](/docs/stix_format.md) with any additional properties. This is because the input control data does not include any properties other than the control text.

## Mapping NIST 800-53 revision 5 to ATT&CK

Scoping decisions and mapping methodology for NIST 800-53 revision 4 controls are decoumented below. The mapping methodology for NIST 800-53 revision 4 controls builds upon and refines the overall security control framework mapping methodology.

### General Scoping Decisions

• Operational vs. Policy and Procedural Controls - This effort is focused on the technical and operational elements of NIST 800-53 and did not take into account the management elements that are often focused on organization specific policies and procedures. This decision was made because management specific controls are policy-based, and the intent of this effort was focusing on technical and operation controls that correlate to ATT&CK mitigations, techniques, and sub-techniques.

• Mitigation vs. Monitoring - Controls that may only monitor adversary behaviors are out of scope. The focus of this effort is on technical controls that mitigate adversary techniques and sub-techniques. For example, IR-5 Incident Monitoring would be out-of-scope as this does not serve as a mitigation, but rather detection of security incident occurrence. However, RA-4 Vulnerability Scanning is in scope as it can lead to findings which allow for remediation prior to exploitation (e.g., apply patches, remove vulnerable software) thereby mitigating attacks. Consideration is not given for the potential that an adversary might be dissuaded or change their tactics to try and avoid detection if they thought activity was being monitored.

• Controls vs. Control Enhancements - This effort maps at the control level and does not map to specific control enhancements.

• Implicit vs. Explicit Mitigation - This effort focuses on system-specific technical mitigations (e.g., block USB devices, perform data backups) and controls that support those mitigations rather than other, non-technical methods of mitigation (e.g., put system in a locked room, write a backup policy).

• Cloud Technologies: Cloud technologies are not fully covered.

• ATT&CKv8 release: ATT&CKv8 released on October 27, 2020, introduces techniques for adversary behavior on Network Infrastructure Devices, such as switches and routers. These have not been included in the control mappings.

• Pre-compromise Mitigation: Those techniques only associated with the Pre-compromise Mitigation are excluded. These apply to techniques occurring before an adversary gains Initial Access, such as Reconnaissance and Resource Development techniques, and are considered out of scope.


### Control Family Scoping Decisions

NIST 800-53 revision 5 control families are listed below with out of scope control families identified:

•	AC - Access Control  
•	AT - Awareness and Training - (out of scope) -  
•	AU - Audit and Accountability - (out of scope) - Audit controls are not applicable as they do not provide mitigations of specific threats, but instead detect successful attacks.  
•	CA - Security Assessment and Authorization  
•	CM - Configuration Management  
•	CP - Contingency Planning  
•	IA - Identification and Authentication  
•	IR - Incident Response - (out of scope) -  
•	MA - Maintenance - (out of scope) -  
•	MP - Media Protection  
•	PE - Physical and Environmental Protection - (out of scope) -  
•	PL - Planning - (out of scope) -  
•	PM - Program Management - (out of scope) -  
•	PS - Personnel Security - (out of scope) -  
•	PT - PII Processing and Transparency   
•	RA - Risk Assessment  
•	SA - System and Services Acquisition  
•	SC - System and Communications Protection  
•	SI - System and Information Integrity  
•	SR - Supply Chain Risk Management  

