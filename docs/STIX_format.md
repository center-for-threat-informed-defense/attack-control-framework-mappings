# STIX Format
This document describes the formatting of the control frameworks and mappings in STIX2.0 JSON. You can find the STIX data in the `/frameworks/` folder:
- [NIST 800-53 Revision 4 STIX data](/frameworks/nist800-53-r4/stix)
- [NIST 800-53 Revision 5 STIX data](/frameworks/nist800-53-r5/stix)

## STIX
Structured Threat Information Expression (STIX&trade;) is a language and serialization format used to exchange cyber threat intelligence (CTI). STIX enables organizations to share CTI with one another in a consistent and machine readable manner, allowing security communities to better understand what computer-based attacks they are most likely to see and to anticipate and/or respond to those attacks faster and more effectively. To find out more about STIX, please see [the STIX 2.0 website](https://oasis-open.github.io/cti-documentation/stix/intro). 

<img src="/docs/controls_in_stix.png" width="900px">

## Format
The control and mapping data in this repository follows the STIX 2.0 format as follows:
- Both controls and mappings are represented in STIX2.0 JSON.
- Controls are represented as [course-of-actions](https://docs.oasis-open.org/cti/stix/v2.0/csprd01/part2-stix-objects/stix-v2.0-csprd01-part2-stix-objects.html#_Toc476230929).
- Relationships of type `subcontrol-of` map sub-controls to their parent controls for frameworks which have hierarchical controls. 
- `x_mitre_` properties are added to control `course-of-action` objects for additional properties depending on the control framework, such as the control family (`x_mitre_family`) or control priority (`x_mitre_priority`). These additional properties are not standardized across control frameworks, and are described in the README of each control framework:
    - [NIST 800-53 Revision 4 Extended Fields](/frameworks/nist800-53-r4#extended-fields)
    - [NIST 800-53 Revision 5 Extended Fields](/frameworks/nist800-53-r5#extended-fields)
- Mappings from individual controls to ATT&CK techniques and sub-techniques are represented as [relationships](https://docs.oasis-open.org/cti/stix/v2.0/csprd01/part2-stix-objects/stix-v2.0-csprd01-part2-stix-objects.html#_Toc476230970) of type `mitigates`, where the `source_ref` is the `id` of the control and the `target_ref` is the `id` of the technique or sub-technique. The optional `description` field on the relationship is taken from the input spreadsheet if a description is given there, and is used to justify the mapping.

## See also
- [Tooling](/docs/tooling.md) for more information about how the STIX data was created.
- [Visualization](/docs/visualization.md) for more information about how to visualize the mappings.
