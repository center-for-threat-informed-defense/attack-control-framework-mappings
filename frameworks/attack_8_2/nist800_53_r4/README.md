# NIST Special Publication 800-53 Revision 4 Control Mappings

This folder contains mappings of NIST Special Publication (SP) 800-53 Revision 4 to MITRE ATT&CK v8.2 along with parsers and supporting data.

| Mappings Version | Last Updated      | ATT&CK Version | ATT&CK Domain |
|------------------|-------------------|----------------|---------------|
| 1.3              | 3 February 2021  | [ATT&CK v8.2](https://attack.mitre.org/resources/versions/) | Enterprise |

| Data ||
|------|------|
| [spreadsheet](nist800-53-r4-mappings.xlsx) | Lists all of the mappings for this control framework. |
| [layers](layers) | [ATT&CK Navigator](https://github.com/mitre-attack/attack-navigator) layers showing the mappings in the context of the ATT&CK Matrix. |
| [stix](stix) | Output STIX 2.0 json data. See the README in that folder for more information. |
| [input](input) | Input spreadsheets from which the STIX is built. To rebuild the STIX data from the input spreadsheets, run `python3 parse.py`.See the README in that folder for more information. |


## Extended Fields

The NIST SP 800-53 Rev. 4 STIX data extends the [general controls format](/docs/stix_format.md) with the following properties:

| STIX field | type | description |
|:-----------|:-----|:------------|
| `x_mitre_impact` | list of strings | the baseline-impact of the control or enhancement. Values include `"LOW"`, `"MODERATE"`, `"HIGH"`. |
| `x_mitre_family` | string | The family to which the control belongs. |
| `x_mitre_priority` | string | The priority of the control. Control enhancements inherit this value from their parent control. |

## Mapping NIST 800-53 Revision 4 to ATT&CK

Scoping decisions and mapping methodology for NIST 800-53 Rev. 4 controls are documented below. The mapping methodology for NIST 800-53 Rev. 4 controls builds upon and refines the overall [security control framework mapping methodology](/docs/mapping_methodology.md).

### General Scoping Decisions
| Item | Scoping Decision |
|------|------|
| Operational vs. Policy and Procedural Controls | This effort is focused on the technical and operational elements of NIST 800-53 and did not take into account the management elements that are often focused on organization specific policies and procedures.  This decision was made because management specific controls are policy-based, and the intent of this effort was focusing on technical and operation controls that correlate to ATT&CK mitigations, techniques, and sub-techniques. |
| Mitigation vs. Monitoring | Controls that may only monitor adversary behaviors are out of scope. The focus of this effort is on technical controls that mitigate adversary techniques and sub-techniques. For example, IR-5 Incident Monitoring would be out-of-scope as this does not serve as a mitigation, but rather detection of security incident occurrence. However, RA-4 Vulnerability Scanning is in scope as it can lead to findings which allow for remediation prior to exploitation (e.g., apply patches, remove vulnerable software) thereby mitigating attacks. Consideration is not given for the potential that an adversary might be dissuaded or change their tactics to try and avoid detection if they thought activity was being monitored. |
| Controls vs. Control Enhancements | This effort maps at the control level and does not map to specific control enhancements. |
| Implicit vs. Explicit Mitigation | This effort focuses on system-specific technical mitigations (e.g., block USB devices, perform data backups) and controls that support those mitigations rather than other, non-technical methods of mitigation (e.g., put system in a locked room, write a backup policy).|
| Network Infrastructure Devices | [ATT&CK v8](https://attack.mitre.org/resources/versions/) released on October 27, 2020, introduces techniques for adversary behavior on Network Infrastructure Devices, such as switches and routers. These have not been included in the control mappings. |
| [Pre-compromise Mitigation](https://attack.mitre.org/mitigations/M1056/) | Those techniques only associated with the Pre-compromise Mitigation are excluded. These apply to techniques occurring before an adversary gains Initial Access, such as Reconnaissance and Resource Development techniques, and are considered out of scope. |

### Control Family Scoping Decisions
NIST 800-53 revision 4 control families are listed below with links to the control family on the NIST web site and our rational for a given control family being in or out of scope: 

| Control Family | In Scope | Rationale |
|------|------|------|
| AC - [Access Control](https://nvd.nist.gov/800-53/Rev4/family/Access%20Control)| Yes | Access Control family is in scope as it provides technical and operational controls for the control and enforcement of system access, accounts, and information. |
| AU - [Audit and Accountability](https://nvd.nist.gov/800-53/Rev4/family/Audit%20and%20Accountability) | No | Audit and Accountability controls are not applicable as they do not provide mitigations of specific threats, but instead detect successful attacks. |
| AT - [Awareness and Training](https://nvd.nist.gov/800-53/Rev4/family/Awarenessand%20Training) | No | Awareness and Training controls are not applicable as they are for general security awareness training and not specific threat mitigations.|
| CM - [Configuration Management](https://nvd.nist.gov/800-53/Rev4/family/Configuration%20Management)| Yes | Configuration Management controls are in scope as they maintain technical and operational controls for maintaining secure configuration of information systems. |
| CP - [Contingency Planning](https://nvd.nist.gov/800-53/Rev4/family/Contingency%20Planning)| Yes | Contingency Planning controls are in scope as they provide operational and technical controls for information protection at the system level.|
| IA - [Identification and Authentication](https://nvd.nist.gov/800-53/Rev4/family/Identification%20and%20Authentication)| Yes | Identification and Authentication controls are in scope as they provide operational and technical controls for managing and enforcing identification and authentication of network and system users and devices.|
| IR - [Incident Response](https://nvd.nist.gov/800-53/Rev4/family/Incident%20Response) | No | Incident Response controls are not applicable as they do not provide mitigations of specific threats but rather provide detection of security incident occurrences. |
| MA - [Maintenance](https://nvd.nist.gov/800-53/Rev4/family/Maintenance) | No | Maintenance controls are not applicable as they are related to the procedural management of information system maintenance and are not threat-specific. |
| MP - [Media Protection](https://nvd.nist.gov/800-53/Rev4/family/Media%20Protection)| Yes | Media Protection family is in scope as it provides technical and operational controls for the control and access of digital system media.|
| PS - [Personnel Security](https://nvd.nist.gov/800-53/Rev4/family/Personnel%20Security) | No | Personnel security controls are not applicable as they are related to the procedural management of individuals. |
| PE - [Physical and Environmental Protection](https://nvd.nist.gov/800-53/Rev4/family/Physical%20and%20Environmental%20Protection) | No | Physical and Environmental Protection controls are not applicable as they are related to the management and protection of physical space. |
| PL - [Planning](https://nvd.nist.gov/800-53/Rev4/family/Planning) | No | Planning controls are not applicable as they focus on high-level system security plans and are not threat-specific.|
| PM - [Program Management](https://nvd.nist.gov/800-53/Rev4/family/Program%20Management) | No | Program Management controls are not applicable as they focus on programmatic, organization-wide information security requirements for managing information security programs.|
| RA - [Risk Assessment](https://nvd.nist.gov/800-53/Rev4/family/Risk%20Assessment)| Yes | Risk Assessment controls are in scope as they provide technical and operational controls and techniques for risk and vulnerability management and maintaining security at the system level. |
| CA - [Security Assessment and Authorization](https://nvd.nist.gov/800-53/Rev4/family/Security%20Assessment%20and%20Authorization)| Yes | Security Assessment and Authorization controls are in scope as they provide technical and operational controls and techniques for monitoring and assessing security at the system level. |
| SC - [System and Communications Protection](https://nvd.nist.gov/800-53/Rev4/family/System%20and%20Communications%20Protection)| Yes | System and Communications Protection controls are in scope as they provide technical and operational controls for the separation and protection of systems and information. |
| SI - [System and Information Integrity](https://nvd.nist.gov/800-53/Rev4/family/System%20and%20Information%20Integrity)| Yes | System and Information Integrity controls are in scope as they provide technical and operational controls and techniques for protecting and analyzing the integrity of software, firmware, and information. |
| SA - [System and Services Acquisition](https://nvd.nist.gov/800-53/Rev4/family/System%20and%20Services%20Acquisition)| Yes | System and Services Acquisition are in scope as they provide technical and operational controls for security testing and evaluation of the system development life cycle and supply chain risk management. |
