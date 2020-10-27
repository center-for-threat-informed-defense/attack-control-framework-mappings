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

Scoping decisions and mapping methodology for NIST 800-53 revision 4 controls are decoumented below. The mapping methodology for NIST 800-53 revision 4 controls builds upon and refines the overall [security control framework mapping methodology](/docs/mapping_methodology.md).

### General Scoping Decisions
- Opperational vs. Policy and Prodedural Controls - This effort is focused on the technical and operational elements of NIST 800-53 and did not take into account the management elements that are often focused on organization specific policies and procedures.  This decision was made because management specific controls are policy-based, and the intent of this effort was focusing on technical and operation controls that correlate to ATT&CK mitigations, techniques, and sub-techniques. 
- Mitigation vs. Montioring - 
- 

### Control Family Scoping Decisions
NIST 800-53 revision 4 contolr families are listed below with links to the control family on the NIST web site and our rational for a given control family being in or out of scope: 
- AC - [Access Control](https://nvd.nist.gov/800-53/Rev4/family/Access%20Control)
- AU - [Audit and Accountability](https://nvd.nist.gov/800-53/Rev4/family/Audit%20and%20Accountability) - (out of scope) - Audit controls are not applicable as they do not provide mitigations of specific threats, but instead detect successful attacks.
- AT - [Awareness and Training](https://nvd.nist.gov/800-53/Rev4/family/Awarenessand%20Training) - (out of scope) - 
- CM - [Configuration Management](https://nvd.nist.gov/800-53/Rev4/family/Configuration%20Management)
- CP - [Contingency Planning](https://nvd.nist.gov/800-53/Rev4/family/Contingency%20Planning)
- IA - [Identification and Authentication](https://nvd.nist.gov/800-53/Rev4/family/Identification%20and%20Authentication)
- IR - [Incident Response](https://nvd.nist.gov/800-53/Rev4/family/Incident%20Response) - (out of scope) - pending discusssion with Tiffany
- MA - [Maintenance](https://nvd.nist.gov/800-53/Rev4/family/Maintenance) - (out of scope) - 
- MP - [Media Protection](https://nvd.nist.gov/800-53/Rev4/family/Media%20Protection)
- PS - [Personnel Security](https://nvd.nist.gov/800-53/Rev4/family/Personnel%20Security) - (out of scope) - 
- PE - [Physical and Environmental Protection](https://nvd.nist.gov/800-53/Rev4/family/Physical%20and%20Environmental%20Protection) - (out of scope) - 
- PL - [Planning](https://nvd.nist.gov/800-53/Rev4/family/Planning) - (out of scope) - pending discussion with Tiffany
- PM - [Program Management](https://nvd.nist.gov/800-53/Rev4/family/Program%20Management) - (out of scope) - pending discussion wiht Tiffany
- RA - [Risk Assessment](https://nvd.nist.gov/800-53/Rev4/family/Risk%20Assessment)
- CA - [Security Assessment and Authorization](https://nvd.nist.gov/800-53/Rev4/family/Security%20Assessment%20and%20Authorization)
- SC - [System and Communications Protection](https://nvd.nist.gov/800-53/Rev4/family/System%20and%20Communications%20Protection)
- SI - [System and Information Integrity](https://nvd.nist.gov/800-53/Rev4/family/System%20and%20Information%20Integrity)
- SA - [System and Services Acquisition](https://nvd.nist.gov/800-53/Rev4/family/System%20and%20Services%20Acquisition)
