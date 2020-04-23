# ATT&CK Control Mappings
This repository includes tools and data for mapping control frameworks to MITRE ATT&amp;CK. In addition to mapping the frameworks, it defines a common representation for frameworks — see [control format](#control-format), below.


## Control Format v1.0
This project defines a common format for representing a control. A control framework is then represented as a list of control objects. A python class and additional utilities for mapping controls can be found in [common/classes/control.py](common/classes/control.py).

### Control Bundle
A control bundle is a collection of individual controls. It typically represents an entire control framework.

| Name | Type | Required? | Description |
|:----|:----|:----|:----|
| name | string | no | the name of the mappings bundle. Typically a more human-readable version of the "source" field |
| description | string | no | A description of what the mapping bundle contains |
| spec_version | string | yes | the version of the mapping format used to create the bundle |
| source | string | yes | the control framework the mappings correspond to, e.g "nist800-53 Rev4" |
| controls | Control[] | yes | list of objects of type Control (below) |


### Control object
A control object is an individual control from within a control framework. Controls can be nested hierarchically using the `parent` field. 

| Name | Type | Required? | Description |
|:----|:----|:----|:----|
| id | string | yes | the ID of the control, corresponding to the `source_id` of a mapping object. |
| name | string | no | the long-form name of the control, e.g `"account management"` |
| parent_id | string | no | the `id` of the control under which this control is nested. If this field is omitted, the control will be at the top-level of the control framework |
| description | string | no | A description of the control |
| characteristics | Characteristic[] | no | list of objects of type Characteristic (below) |

### Characteristic object
A control characteristic is a flexible way to encode additional data about a control. Within a given control framework all controls *should* have the same characteristic types (names), but not necessarily the same characteristic values. For example, in NIST 800-53 the baseline-impact of a control may be represented as a control characteristic. Other frameworks may not record an analogous baseline-impact value for their controls so they may lack that characteristic.

Some example characteristics may be:
- `baseline-impact` (low, moderate, high)
- `incident-relativity` (preventative, detective, corrective)
- `control-type` (physical, procedural, technical, legal/regulatory)

| Name | Type | Required? | Description |
|:----|:----|:----|:----|
| name | string | yes | the name of the characteristic, e.g `"baseline-impact"` |
| value | string[] | yes | the value of the characteristic for the control, e.g `["moderate", "high"]`. |

Example control bundle:
```json
{
    "name": "NIST 800-53 revision 4",
    "description": "a catalog of security and privacy controls for all U.S. federal information systems except those related to national security",
    "spec_version": "1.0",
    "source": "nist800-53 rev4",
    "controls": [
        {
            "id": "FAMILY-AC",
            "name": "ACCESS CONTROL",
        }
        {
            "id": "AC-1",
            "name": "ACCESS CONTROL POLICY AND PROCEDURES",
            "parent_id": "FAMILY-AC",
            "description": "This control addresses the establishment of policy and procedures for the effective implementation of selected security controls and control enhancements in the AC family. Policy and procedures reflect applicable federal laws, Executive Orders, directives, regulations, policies, standards, and guidance. Security program policies and procedures at the organization level may make the need for system-specific policies and procedures unnecessary. The policy can be included as part of the general information security policy for organizations or conversely, can be represented by multiple policies reflecting the complex nature of certain organizations. The procedures can be established for the security program in general and for particular information systems, if needed. The organizational risk management strategy is a key factor in establishing policy and procedures.",
            "characteristics": [
                {
                    "name": "baseline-impact",
                    "values": ["LOW","MODERATE","HIGH"]
                },
                {
                    "name": "priority",
                    "values": ["P1"]
                }
            ]
        },
        {
            "id": "AC-1a.",
            "parent_id": "AC-1",
            "description": "The organization: Develops, documents, and disseminates to [Assignment: organization-defined personnel or roles]:",
            "characteristics": [
                {
                    "name": "baseline-impact",
                    "values": ["LOW","MODERATE","HIGH"]
                },
                {
                    "name": "priority",
                    "values": ["P1"]
                }
            ]
        }
        {
            "id": "AC-2 (1)",
            "name": "AUTOMATED SYSTEM ACCOUNT MANAGEMENT",
            "parent_id": "FAMILY-AC",
            "description": "The use of automated mechanisms can include, for example: using email or text messaging to automatically notify account managers when users are terminated or transferred; using the information system to monitor account usage; and using telephonic notification to report atypical system account usage.",
            "characteristics": [
                {
                    "name": "baseline-impact",
                    "values": ["MODERATE","HIGH"]
                },
                {
                    "name": "priority",
                    "values": ["P1"]
                }
            ]
        },
    ]
}
```

## Mapping Format v1.0
This project defines a common format for representing a mapping to a control.  A python class and additional utilities for mapping controls to ATT&CK can be found in [common/classes/mapping.py](common/classes/mapping.py). The format for a single control mapping is as follows:

### Mapping Bundle
A mapping bundle is a collection of individual mappings.

| Name | Type | Required? | Description |
|:----|:----|:----|:----|
| name | string | no | the name of the mappings bundle |
| description | string | no | A description of what the mapping bundle contains |
| spec_version | string | yes | the version of the mapping format used to create the bundle |
| source | string | no | the control framework the mappings correspond to, e.g "nist800-53 Rev4" |
| target | string | no | the version of MITRE ATT&CK the mappings correspond to, e.g "ATT&CK v6.2" |
| mappings | Mapping[] | yes | list of objects of type Mapping (below) |

### Mapping Object
A mapping object is a mapping from a control to an ATT&CK technique.

| Name | Type | Required? | Description |
|:----|:----|:----|:----|
| source_id | string | yes | the ID of the control, e.g "AC-1" |
| target_id | string | yes | the technique STIXID in format "attack-pattern--..." |
| description | string | no | a text description summarizing the justification of the mapping. |



Example mapping bundle:
```json
{
    "name": "NIST 800-53 Revision 4 to ATT&CK v6.2",
    "description": "NIST 800-53 revision 4 mapped to ATT&CK version 6.2",
    "spec_version": "1.0",
    "source": "nist800-53 rev4",
    "target": "ATT&CK v6.2",
    "mappings": [
        {
            "source_id": "AC-1",
            "target_id": "attack-pattern--4ab929c6-ee2d-4fb5-aab4-b14be2ed7179",
            "description": "example description of why AC-1 maps to T1547.001"
        }
        {
            "source_id": "AU-6a.",
            "target_id": "attack-pattern--b2d03cea-aec1-45ca-9744-9ee583c1e1cc",
            "description": "example description of why AU-6a. maps to T1110.004"
        }
    ]
}
```