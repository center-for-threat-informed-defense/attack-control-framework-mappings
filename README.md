[![codecov](https://codecov.io/gh/center-for-threat-informed-defense/attack-control-framework-mappings/branch/master/graph/badge.svg?token=PLVBGOUWMC)](https://codecov.io/gh/center-for-threat-informed-defense/attack-control-framework-mappings)

# Security Control Framework Mappings to ATT&CK
This repository contains security control framework mappings to MITRE ATT&CK® with supporting documentation and resources. These mappings provide a critically important resource for organizations to assess their security control coverage against real-world threats as described in the ATT&CK knowledge base and provide a foundation for integrating ATT&CK-based threat information into the risk management process. This work was developed by the [Center for Threat-Informed Defense](https://mitre-engenuity.org/center-for-threat-informed-defense/) in collaboration with our participants.

**NIST 800-53 Revision 4 Security Control Mappings**

| ATT&CK Version | Mappings as XLSX (download) | ATT&CK Navigator Layers | STIX Data |
|---|---|---|---|
| [ATT&CK-v9.0](/frameworks/ATT&CK-v9.0/nist800-53-r4/) | [Spreadsheet](https://github.com/center-for-threat-informed-defense/attack-control-framework-mappings/raw/attackv9_update/frameworks/ATT%26CK-v9.0/nist800-53-r4/nist800-53-r4-mappings.xlsx) | [Navigator Layers](/frameworks/ATT&CK-v9.0/nist800-53-r4/layers) | [STIX](/frameworks/ATT&CK-v9.0/nist800-53-r4/stix) |
| [ATT&CK-v8.2](/frameworks/ATT&CK-v8.2/nist800-53-r4/) | [Spreadsheet](https://github.com/center-for-threat-informed-defense/attack-control-framework-mappings/raw/attackv9_update/frameworks/ATT%26CK-v8.2/nist800-53-r4/nist800-53-r4-mappings.xlsx) | [Navigator Layers](/frameworks/ATT&CK-v8.2/nist800-53-r4/layers) | [STIX](/frameworks/ATT&CK-v8.2/nist800-53-r4/stix) |

**NIST 800-53 Revision 5 Security Control Mappings**

| ATT&CK Version | Mappings as XLSX (download) | ATT&CK Navigator Layers | STIX Data |
|---|---|---|---|
| [ATT&CK-v9.0](/frameworks/ATT&CK-v9.0/nist800-53-r5/) | [Spreadsheet](https://github.com/center-for-threat-informed-defense/attack-control-framework-mappings/raw/attackv9_update/frameworks/ATT%26CK-v9.0/nist800-53-r5/nist800-53-r5-mappings.xlsx) | [Navigator Layers](/frameworks/ATT&CK-v9.0/nist800-53-r5/layers) | [STIX](/frameworks/ATT&CK-v9.0/nist800-53-r5/stix) |
| [ATT&CK-v8.2](/frameworks/ATT&CK-v8.2/nist800-53-r5/) | [Spreadsheet](https://github.com/center-for-threat-informed-defense/attack-control-framework-mappings/raw/attackv9_update/frameworks/ATT%26CK-v8.2/nist800-53-r5/nist800-53-r5-mappings.xlsx) | [Navigator Layers](/frameworks/ATT&CK-v8.2/nist800-53-r5/layers) | [STIX](/frameworks/ATT&CK-v8.2/nist800-53-r5/stix) |

## A Collaborative Approach

Mapping NIST Special Publication 800-53, or any security control framework, to ATT&CK is a labor intensive and often subjective undertaking. Furthermore, due to the large number of security controls in any given framework and the evolving nature of cyber adversaries, these mappings are often error prone and difficult to maintain. We recognized that there was not only a need for mappings NIST 800-53, but an opportunity to work collaboratively and advance threat-informed defense with the global community. With over 6,300 individual mappings between NIST 800-53 and ATT&CK, we believe that this work will greatly reduce the burden on the community – allowing organizations to focus their limited time and resources on understanding how controls map to threats in their environment.

## Repository Contents

- [Frameworks](/frameworks) — this directory contains the security control frameworks and their mappings to ATT&CK techniques. Each security control framework has its own directory of documentation and resources. 
- [Mapping Methodology](/docs/mapping_methodology.md) — a description of the general process used to create the control mappings
- [Tooling](/docs/tooling.md) — a set of python tools to support the creation of new mappings and the customization of existing mappings
- [Use Cases](/docs/use-cases.md) - use cases for security control framework mappings to ATT&CK
- [STIX Format](/docs/STIX_format.md) — information regarding the STIX representation of the control frameworks and the mappings to ATT&CK
- [Visualization](/docs/visualization.md) — this document describes some ways the mappings data can be visualized. 
- [Contributing](/CONTRIBUTING.md) — information about how to contribute controls, mappings, or other improvements to this repository
- [Changelog](/CHANGELOG.md) — list of updates to this repository


## Getting Involved

There are several ways that you can get involved with this project and help advance threat-informed defense. 

First, review the mappings, use them, and tell us what you think. We welcome your review and feedback on the NIST 800-53 mappings, our methodology, and resources. 

Second, we are interested in applying our methodology to other security control frameworks. Let us know what frameworks you would like to see mapped to ATT&CK. Your input will help us prioritize how we expand our mappings. 

Finally, we are interested developing additional tools and resources to help the community understand and make threat-informed decisions in their risk management programs. Share your ideas and we will consider them as we explore additional research projects.  

## Questions and Feedback
   
Please submit issues for any technical questions/concerns or contact ctid@mitre-engenuity.org directly for more general inquiries.

Also see the guidance for contributors if are you interested in [contributing or simply reporting issues.](/CONTRIBUTING.md)

## Notice 

Copyright 2020 MITRE Engenuity. Approved for public release. Document number CT0011

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at 

http://www.apache.org/licenses/LICENSE-2.0 

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License. 

This project makes use of ATT&CK®

[ATT&CK Terms of Use](https://attack.mitre.org/resources/terms-of-use/)
