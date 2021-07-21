# Use Cases

## Use Cases — as a user of the Security Control Framework Mappings to ATT&CK...

This document describes basic use cases for Security Control Framework Mappings to MITRE ATT&CK. These use cases are expressed as user stories, and a short exploration of how a user story may be achieved follows each story.

### 1. I want to determine the technique coverage of a control or set of controls

With control mappings implemented at a technique level, this is as simple as following the mappings from the control(s) to the associated techniques. Additionally, ATT&CK Navigator integration will easily support visualizations of such coverage.

In the context of this project, a mapping from a control to a technique is meant to convey at least a partial mitigation of the given technique. Therefore the “coverage” of a set of techniques isn’t meant to mean they’re completely defended against, but rather that the given controls provide some mitigation against the successful execution of the technique(s). 

### 2. I want to know what security controls to select/implement in order to mitigate a specific set of techniques

This is essentially the reverse direction of [use case 1](#1-i-want-to-determine-the-technique-coverage-of-a-control-or-set-of-controls). Use the mappings to trace backwards from techniques to a set of associated controls.  

Because techniques can map to multiple controls, it is likely that there will be multiple combinations of controls which could mitigate the techniques. Given a way of ranking the possible solutions (e.g minimize the number of controls, maximize the baseline-impact of controls) a dynamic programming algorithm can be implemented to determine the optimal set of controls required to mitigate the techniques. 

### 3. I want to determine what security controls I should use to implement a given ATT&CK mitigation

Mitigations in ATT&CK are mapped to techniques, and this project maps techniques to security controls. One possible interpretation of “implementing” a mitigation may be finding the set of security controls that mitigates the techniques that are mapped to the mitigation. This then resolves to an extension of [use case 2](#2-i-want-to-know-what-security-controls-to-selectimplement-in-order-to-mitigate-a-specific-set-of-techniques), where the set of techniques is those associated with the ATT&CK Mitigation. 

Visualization of this indirect mapping should be undertaken with care. It should not be implied that a security control maps directly to a mitigation or vice versa, since that is firstly inaccurate to the data model and some of those derived “mappings” could be confusing in certain cases. The intermediate step of the technique must therefore always be shown in visualizations of these two-step mappings. ATT&CK Mitigations should be interpreted as a “contextual grouping” of techniques, and the visualization should convey that the actual mappings happen with the contextually-grouped techniques, not the mitigation or other grouping object.

### 4. I want to determine what security controls I can use to defend against a given group or software.

Groups and Software in ATT&CK are mapped to techniques. Therefore, this use case can be achieved in the exact manner as use case 3 (above) — determine the set of security controls that mitigate the techniques mapped to the group or software. 

The visualization of such a use case could be implemented the same way as in [use case 3](#3-i-want-to-determine-what-security-controls-i-should-use-to-implement-a-given-attck-mitigation), except with Groups or Software as the “contextual grouping” instead of mitigations. Such a visualization could be implemented to give the user choice of what type to use for contextual grouping (mitigation, group, software, even tactic) and therefore achieve several use cases with a single implementation.

---

_The following use cases are intended to capture the operational context of users/roles for consuming threat intelligence data into an operational environment to improve overall risk management activities._

### 5. As an ISSO, I want to (but not limited to)

- Provide input to system developers regarding security requirements and security engineering practices to incorporate into the information system to defend against adversary activity. 
- Understand what security controls to select for securing information systems.
- Assess risk by understanding security control coverage in mitigating techniques associated with adversarial behavior. 
- Perform continuous monitoring activities to check the security posture on endpoints.

#### So that I can

- Support the Security Engineer, system developers, and information system owner’s selection and implementation of security controls most appropriate in mitigating cyber attacks.
- Support the CISO/ISSM in reviewing the adequacy of risk and gaps in overall threat defense; and identify which additional security controls are needed to mitigate cyber attacks.  
- Determine security control suitability and participate in the selection of security controls for securing information systems against cyber attacks.
- Validate NIST 800-53 (or other framework) compliance and maintain/achieve ongoing Approval to Operate (ATO).

### 6. As a Security Engineer, I want to (but not limited to)

- Understand what mitigations are covered by implementing a given set of security controls.
- Understand what adversary behaviors (ATT&CK techniques) are mitigated by implementing a given set of security controls.

#### So that I can

- Select and tailor the security controls for an information system to provide suitable protections and improved threat-informed defense.
- Review the information system’s implemented security controls periodically and update the security control selection/tailoring as needed, as well as identify cybersecurity solutions needed to mitigate cyber attacks.  
- Work with the ISSO to understand residual risk in security control coverage to better align cyber defense to address adversary behaviors.

### 7. As a CISO or ISSM, I want to (but not limited to)

- Understand gaps that exist in mitigation strategies to better assess enterprise risk.  
- Understand risk associated with specific threats/techniques.

#### So that I can

- I can determine which mitigation strategies are most effective against techniques associated with adversarial activities, and which security controls or cyber solutions are needed to improve cyber defense.   
- I can implement/improve continuous monitoring activities commensurate to address the gaps and risks in security control coverage, as well as identify residual risks and develop/implement compensating controls to mitigate most damaging attacks.  

### 8. As the Blue Team, I want to (but not limited to)

- Understand gaps in cyber defense and entry points where attackers may exploit systems. 
- Understand how well my cyber defenses perform against adversary activity to assess cyber resiliency. 
- Understand what security solutions are needed to improve cyber defense. 

#### So that I can

- Design, build, and implement appropriate cyber defenses.
- Measure cyber resiliency and determine what additional coverage is needed to mitigate threats. 
- Develop a comprehensive cyber defense strategy to address adversaries evolving capabilities. 
