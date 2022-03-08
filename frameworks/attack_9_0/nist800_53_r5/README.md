# NIST 800-53 Revision 5 Control Mappings


This folder contains mappings of NIST Special Publication (SP) 800-53 Revision 5 to MITRE ATT&CK v9.0 along with parsers and supporting data. NIST 800-53 Rev. 5 was mapped to ATT&CK based on its initial publication in September 2020. NIST published an [update on December 10, 2020](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final) to 800-53 Rev. 5 that has not yet been evaluated. 

| Mappings Version | Last Updated | ATT&CK Version | ATT&CK Domain |
|---|---|---|---|
| 2.0 | 14 July 2021 | [ATT&CK-v9.0](https://attack.mitre.org/versions/v9/) | Enterprise |


| Data ||
|---|---|
| [spreadsheet](nist800-53-r5-mappings.xlsx) | Lists all of the mappings for this control framework. |
| [layers](layers) | [ATT&CK Navigator](https://github.com/mitre-attack/attack-navigator) layers showing the mappings in the context of the ATT&CK Matrix. |
| [stix](stix) | Output STIX 2.0 json data. See the README in that folder for more information. |
| [input](input) | Input spreadsheets from which the STIX is built. To rebuild the STIX data from the input spreadsheets, run `python3 parse.py`.See the README in that folder for more information. |

## Extended Fields

The NIST 800-53 Rev. 5 STIX data does not extend the [general controls format](/docs/stix_format.md) with any additional properties. This is because the input control data does not include any properties other than the control text.

## Mapping NIST 800-53 revision 5 to ATT&CK

Scoping decisions and mapping methodology for NIST 800-53 Rev. 5 controls are documented below. The mapping methodology for NIST 800-53 Rev. 5 controls builds upon and refines the overall [security control framework mapping methodology](/docs/mapping_methodology.md).

### General Scoping Decisions

| Item | Scoping Decision |
|---|---|
| Operational vs. Policy and Procedural Controls | This effort is focused on the technical and operational elements of NIST 800-53 and did not take into account the management elements that are often focused on organization specific policies and procedures.  This decision was made because management specific controls are policy-based, and the intent of this effort was focusing on technical and operation controls that correlate to ATT&CK mitigations, techniques, and sub-techniques. |
| Mitigation vs. Monitoring | Controls that may only monitor adversary behaviors are out of scope. The focus of this effort is on technical controls that mitigate adversary techniques and sub-techniques. For example, IR-5 Incident Monitoring would be out-of-scope as this does not serve as a mitigation, but rather detection of security incident occurrence. However, RA-4 Vulnerability Scanning is in scope as it can lead to findings which allow for remediation prior to exploitation (e.g., apply patches, remove vulnerable software) thereby mitigating attacks. Consideration is not given for the potential that an adversary might be dissuaded or change their tactics to try and avoid detection if they thought activity was being monitored. |
| Controls vs. Control Enhancements | This effort maps at the control level and does not map to specific control enhancements. |
| Implicit vs. Explicit Mitigation | This effort focuses on system-specific technical mitigations (e.g., block USB devices, perform data backups) and controls that support those mitigations rather than other, non-technical methods of mitigation (e.g., put system in a locked room, write a backup policy).|
| Network Infrastructure Devices | [ATT&CK v8](https://attack.mitre.org/resources/versions/) released on October 27, 2020, introduces techniques for adversary behavior on Network Infrastructure Devices, such as switches and routers. These have not been included in the control mappings. |
| [Pre-compromise Mitigation](https://attack.mitre.org/mitigations/M1056/) | Those techniques only associated with the Pre-compromise Mitigation are excluded. These apply to techniques occurring before an adversary gains Initial Access, such as Reconnaissance and Resource Development techniques, and are considered out of scope. |

### Control Family Scoping Decisions

NIST 800-53 Rev. 5 control families are listed below with our rational for a given control family being in or out of scope:

| Control Family | In Scope | Rationale |
|---|---|---|
| AC - Access Control | Yes | Access Control family is in scope as it provides technical and operational controls for the control and enforcement of system access, accounts, and information. |
| AT - Awareness and Training | No | Awareness and Training controls are not applicable as they are for general security awareness training and not specific threat mitigations.|
| AU - Audit and Accountability | No | Audit and Accountability controls are not applicable as they do not provide mitigations of specific threats, but instead detect successful attacks. |
| CM - Configuration Management | Yes | Configuration Management controls are in scope as they maintain technical and operational controls for maintaining secure configuration of information systems. |
| CP - Contingency Planning | Yes | Contingency Planning controls are in scope as they provide operational and technical controls for information protection at the system level.|
| IA - Identification and Authentication | Yes | Identification and Authentication controls are in scope as they provide operational and technical controls for managing and enforcing identification and authentication of network and system users and devices. |
| IR - Incident Response | No | Incident Response controls are not applicable as they do not provide mitigations of specific threats but rather provide detection of security incident occurrences. |
| MA - Maintenance |  No | Maintenance controls are not applicable as they are related to the procedural management of information system maintenance and are not threat-specific. |
| MP - Media Protection | Yes | Media Protection family is in scope as it provides technical and operational controls for the control and access of digital system media. |
| PE - Physical and Environmental Protection | No | Physical and Environmental Protection controls are not applicable as they are related to the management and protection of physical space. |
| PL - Planning | No | Planning controls are not applicable as they focus on high-level system security plans and are not threat-specific.|
| PM - Program Management | No | Program Management controls are not applicable as they focus on programmatic, organization-wide information security requirements for managing information security programs.|
| PS - Personnel Security | No | Personnel security controls are not applicable as they are related to the procedural management of individuals. |
| PT - PII Processing and Transparency | No | PII Processing and Transparency controls are not applicable as they are procedural in nature.|
| RA - Risk Assessment | Yes | Risk Assessment controls are in scope as they provide technical and operational controls and techniques for risk and vulnerability management and maintaining security at the system level. |
| CA - Security Assessment and Authorization | Yes | Security Assessment and Authorization controls are in scope as they provide technical and operational controls and techniques for monitoring and assessing security at the system level. |
| SC - System and Communications Protection | Yes | System and Communications Protection controls are in scope as they provide technical and operational controls for the separation and protection of systems and information. |
| SI - System and Information Integrity | Yes | System and Information Integrity controls are in scope as they provide technical and operational controls and techniques for protecting and analyzing the integrity of software, firmware, and information. |
| SA - System and Services Acquisition | Yes | System and Services Acquisition are in scope as they provide technical and operational controls for security testing and evaluation of the system development life cycle. |
| SR - Supply Chain Risk Management | Yes | Supply Chain Risk Management is in scope as they provide technical and operational controls for security testing and evaluation of supply chain processes and elements. |
