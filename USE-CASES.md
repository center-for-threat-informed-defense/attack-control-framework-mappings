# Use Cases

## Introduction

This document is intended to express some hypothetical use cases of the ATT&CK Control Framework Mappings. These use cases are expressed as user stories, and a short exploration of how a user story may be achieved follows each story.

## Use Cases — as a user of the ATT&CK Security Control Framework Mappings...

### 1. I want to be able to determine the technique coverage of a control or set of controls

With control mappings implemented at a technique level, this is as simple as following the mappings from the control(s) to the associated techniques. Additionally, ATT&CK Navigator integration will easily support visualizations of such coverage.

In the context of this project, a mapping from a control to a technique is meant to convey at least a partial mitigation of the given technique. Therefore the “coverage” of a set of techniques isn’t meant to mean they’re completely defended against, but rather that the given controls provide some mitigation against the successful execution of the technique(s). 

### 2. I want to be able to tell what security controls to select/implement in order to mitigate a specific set of techniques

This is essentially the reverse direction of [use case 1](#TODO). Use the mappings to trace backwards from techniques to a set of associated controls.  

Because techniques can map to multiple controls, it is likely that there will be multiple combinations of controls which could mitigate the techniques. Given a way of ranking the possible solutions (e.g minimize the number of controls, maximize the baseline-impact of controls) a dynamic programming algorithm can be implemented to determine the optimal set of controls required to mitigate the techniques. 

### 3. I want to be able to determine what security controls I should use to implement a given ATT&CK mitigation

Mitigations in ATT&CK are mapped to techniques, and techniques are mapped to security controls. One possible interpretation of “implementing” a mitigation may be finding the set of security controls that mitigates the techniques that are mapped to the mitigation. This then resolves to an extension of [use case 2](#TODO), above, where the set of techniques is those associated with the ATT&CK Mitigation. 

Visualization of this indirect mapping should be undertaken with care. It should not be implied that a security control maps directly to a mitigation or vice versa, since that is firstly inaccurate to the data model and some of those derived “mappings” could be confusing in certain cases. The intermediate step of the technique must therefore always be shown in visualizations of these two-step mappings. ATT&CK Mitigations should be interpreted as a “contextual grouping” of techniques, and the visualization should convey that the actual mappings happen with the contextually-grouped techniques, not the mitigation or other grouping object.

### 4. I want to be able to determine what security controls I can use to defend against a given group or software.

Groups and Software in ATT&CK are mapped to techniques. Therefore, this use case can be achieved in the exact manner as use case 3 (above) — determine the set of security controls that mitigate the techniques mapped to the group or software. 

The visualization of such a use case could be implemented the same way as in [use case 3](#TODO), except with Groups or Software as the “contextual grouping” instead of mitigations. Such a visualization could be implemented to give the user choice of what type to use for contextual grouping (mitigation, group, software, even tactic) and therefore achieve several use cases with a single implementation.
