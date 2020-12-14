# NIST 800-53 Revision 5 Control Mappings

This folder contains mappings of NIST Special Publication (SP) 800-53 Revision 5 to MITRE ATT&CK along with parsers and supporting data.

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

Scoping decisions and mapping methodology for NIST 800-53 revision 4 controls are decoumented below. The mapping methodology for NIST 800-53 revision 5 controls builds upon and refines the overall [security control framework mapping methodology](/docs/mapping_methodology.md).

### General Scoping Decisions

| Item | Scoping Decision |
|------|------|
| Operational vs. Policy and Procedural Controls | This effort is focused on the technical and operational elements of NIST 800-53 and did not take into account the management elements that are often focused on organization specific policies and procedures.  This decision was made because management specific controls are policy-based, and the intent of this effort was focusing on technical and operation controls that correlate to ATT&CK mitigations, techniques, and sub-techniques. |
| Mitigation vs. Monitoring | Controls that may only monitor adversary behaviors are out of scope. The focus of this effort is on technical controls that mitigate adversary techniques and sub-techniques. For example, IR-5 Incident Monitoring would be out-of-scope as this does not serve as a mitigation, but rather detection of security incident occurrence. However, RA-4 Vulnerability Scanning is in scope as it can lead to findings which allow for remediation prior to exploitation (e.g., apply patches, remove vulnerable software) thereby mitigating attacks. Consideration is not given for the potential that an adversary might be dissuaded or change their tactics to try and avoid detection if they thought activity was being monitored. |
| Controls vs. Control Enhancements | This effort maps at the control level and does not map to specific control enhancements. |
| Implicit vs. Explicit Mitigation | This effort focuses on system-specific technical mitigations (e.g., block USB devices, perform data backups) and controls that support those mitigations rather than other, non-technical methods of mitigation (e.g., put system in a locked room, write a backup policy).|
| Cloud Technologies | Cloud technologies are not fully covered. This work is focused on Enterprise ATT&CK techniques. |
| Network Infrastructure Devices | [ATT&CK v8](https://attack.mitre.org/resources/versions/) released on October 27, 2020, introduces techniques for adversary behavior on Network Infrastructure Devices, such as switches and routers. These have not been included in the control mappings. |
| [Pre-compromise Mitigation](https://attack.mitre.org/mitigations/M1056/) | Those techniques only associated with the Pre-compromise Mitigation are excluded. These apply to techniques occurring before an adversary gains Initial Access, such as Reconnaissance and Resource Development techniques, and are considered out of scope. |

### Control Family Scoping Decisions

NIST 800-53 revision 5 control families are listed below with out of scope control families identified:

| Control Family | Scoping Decision |
|------|------|
| AC - Access Control | Access Control family is in scope. |
| AU - Audit and Accountability | Audit and Accountability controls are not applicable as they do not provide mitigations of specific threats, but instead detect successful attacks. |
| AT - Awareness and Training | Awareness and Training controls are not applicable as they are for general security awareness training and not specific threat mitigations.|
| CM - Configuration Management | Configuration Management controls are in scope. |
| CP - Contingency Planning | Contingency Planning controls are in scope.|
| IA - Identification and Authentication | Identification and Authentication controls are in scope.|
| IR - Incident Response | Incident Response controls are not applicable as they do not provide mitigations of specific threats but rather provide detection of security incident occurrences. |
| MA - Maintenance |  Maintenance controls are not applicable as they are related to the procedural management of information system maintenance and are not threat-specific. |
| MP - Media Protection | Media Protection controls are in scope.|
| PS - Personnel Security | Personnel security controls are not applicable as they are related to the procedural management of individuals. |
| PE - Physical and Environmental Protection | Physical and Environmental Protection controls are not applicable as they are related to the management and protection of physical space. |
| PL - Planning | Planning controls are not applicable as they focus on high-level system security plans and are not threat-specific.|
| PM - Program Management | Program Management controls are not applicable as they focus on programmatic, organization-wide information security requirements for managing information security programs.|
| PT - PII Processing and Transparency | PII Processing and Transparency controls are not applicable as they are procedural in nature.|
| RA - Risk Assessment | Risk Assessment controls are in scope. |
| CA - Security Assessment and Authorization| Security Assessment and Authorization controls are in scope. |
| SC - System and Communications Protection| System and Communications Protection controls are in scope. |
| SI - System and Information Integrity| System and Information Integrity controls are in scope. |
| SA - System and Services Acquisition| System and Services Acquisition are in scope. |
| SR - Supply Chain Risk Management | Supply Chain Risk Management is in scope. |
