# Security Control Framework Mappings to ATT&CK
This repository contains the materials developed by the [Center for Threat Informed Defense](https://mitre-engenuity.org/center-for-threat-informed-defense/) in cooperation with our participants. The goal of this effort was to develop a framework for mappings between security control frameworks and the MITRE ATT&CK® knowledge base.

These mappings provide the means for organizations to see their security control coverage against associated ATT&CK techniques and to integrate ATT&CK-based threat information within the risk management process. For example, users can employ the mappings to evaluate their cybersecurity readiness, identify gaps and deficiencies in their security posture, improve continuous monitoring activities, and assist in selecting the most appropriate security controls to mitigate the most damaging attacks. A more thorough consideration of use cases to which these mappings might be applied can be found in [our use-cases document](/docs/use-cases.md). 

## Repository Contents

- [Frameworks](/frameworks) — this directory contains the security control frameworks and their mappings to ATT&CK techniques
    - | Data ||||
      |------|------|------|--|
      | [NIST 800-53 Revision 4](/frameworks/nist800-53-r4/) | [Spreadsheet](/frameworks/nist800-53-r4/nist800-53-r4-mappings.xlsx) | [Navigator Layers](/frameworks/nist800-53-r4/layers) | [STIX](/frameworks/nist800-53-r4/stix) |
      | [NIST 800-53 Revision 5](/frameworks/nist800-53-r5/) | [Spreadsheet](/frameworks/nist800-53-r5/nist800-53-r5-mappings.xlsx) | [Navigator Layers](/frameworks/nist800-53-r5/layers) | [STIX](/frameworks/nist800-53-r5/stix) |
- Methodology — processes and procedures for developing and editing mappings
    - [Mapping Methodology](/docs/mapping_methodology.md) — a description of the general process used to create the control mappings
    - [Tooling](/docs/tooling.md) — a set of python tools to support the creation of new mappings and the customization of existing mappings
- [STIX Format](/docs/STIX_format.md) — information regarding the STIX representation of the control frameworks and the mappings to ATT&CK
- [Visualization](/docs/visualization.md) — this document describes some ways the mappings data can be visualized. 
- [Contributing](/CONTRIBUTING.md) — information about how to contribute controls, mappings, or other improvements to this repository
- [Changelog](/CHANGELOG.md) — list of updates to this repository

## Notice 

Copyright 2020 MITRE Engenuity. Approved for public release. 

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at 

http://www.apache.org/licenses/LICENSE-2.0 

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License. 

This project makes use of ATT&CK®

[ATT&CK Terms of Use](https://attack.mitre.org/resources/terms-of-use/)
