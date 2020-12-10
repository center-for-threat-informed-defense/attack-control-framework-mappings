# Security Control Framework Mappings to ATT&CK
This repository contains security control framework mappings to MITRE ATT&CK® with supporting documentation and resources. These mappings provide a critically important resource for organizations to assess their security control coverage against real-world threats as described in the ATT&CK knowledge base and provide a foundation for integrating ATT&CK-based threat information into the risk management process. This work was developed by the [Center for Threat Informed Defense](https://mitre-engenuity.org/center-for-threat-informed-defense/) in collaboration with our participants.

Mapping security control frameworks to ATT&CK is a labor intensive and often subjective undertaking. Furthermore, due to the large number of security controls in any given framework and the evolving nature of cyber adversaries, these mappings are often error prone and difficult to maintain. We recognized that there was an opportunity to work collaboratively and advance threat-informed defense with the global community by creating a venue for developing and sharing these security control framework mappings.

< TODO >  

| Security Control Framework | Mappings as XLSX | ATT&CK Navigator Layers | STIX Data |
|------|------|------|--|
| [NIST 800-53 Revision 4](/frameworks/nist800-53-r4/) | [Spreadsheet](/frameworks/nist800-53-r4/nist800-53-r4-mappings.xlsx) | [Navigator Layers](/frameworks/nist800-53-r4/layers) | [STIX](/frameworks/nist800-53-r4/stix) |
| [NIST 800-53 Revision 5](/frameworks/nist800-53-r5/) | [Spreadsheet](/frameworks/nist800-53-r5/nist800-53-r5-mappings.xlsx) | [Navigator Layers](/frameworks/nist800-53-r5/layers) | [STIX](/frameworks/nist800-53-r5/stix) |

## Repository Contents

- [Frameworks](/frameworks) — this directory contains the security control frameworks and their mappings to ATT&CK techniques. Each security control framework has its own directory of documentation and resources. 
- Methodology — processes and procedures for developing and editing mappings
    - [Mapping Methodology](/docs/mapping_methodology.md) — a description of the general process used to create the control mappings
    - [Tooling](/docs/tooling.md) — a set of python tools to support the creation of new mappings and the customization of existing mappings
- [Use Cases] (/docs/use-cases.md) - TODO
- [STIX Format](/docs/STIX_format.md) — information regarding the STIX representation of the control frameworks and the mappings to ATT&CK
- [Visualization](/docs/visualization.md) — this document describes some ways the mappings data can be visualized. 
- [Contributing](/CONTRIBUTING.md) — information about how to contribute controls, mappings, or other improvements to this repository
- [Changelog](/CHANGELOG.md) — list of updates to this repository

## Notice 

Copyright 2020 MITRE Engenuity. Approved for public release. Document number CT0011

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at 

http://www.apache.org/licenses/LICENSE-2.0 

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License. 

This project makes use of ATT&CK®

[ATT&CK Terms of Use](https://attack.mitre.org/resources/terms-of-use/)
