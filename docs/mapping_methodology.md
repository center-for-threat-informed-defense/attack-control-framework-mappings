# Mapping Methodology

This document outlines the methodology used for this project, but it is not the only way such mappings might be created, as other control frameworks may not align well with this process. As such, the methodology described in this document has been shown to be an effective means of creating mappings between security control frameworks, such as NIST 800-53 and MITRE ATT&CK®. Mapping security control frameworks to ATT&CK provides a powerful way for organizations to see their security control coverage against associated ATT&CK techniques and establishes a means to integrate ATT&CK-based threat information within the risk management process.  

The ATT&CK knowledge base and model for cyber adversary behavior reflects the various phases of an adversary’s attack lifecycle and the platforms they are known to target. The basis of ATT&CK is the set of techniques and sub-techniques that represent actions that adversaries can perform to accomplish objectives and goals. Those objectives and goals are represented by the tactic categories that techniques and sub-techniques fall under.<sup>[[1]](https://attack.mitre.org/docs/ATTACK_Design_and_Philosophy_March_2020.pdf)</sup> The methodology described below leverages the information in the ATT&CK knowledge base and its underlying data model to create context that is then used to select security controls to map to a given technique or sub-technique.

ATT&CK’s mitigations are at the core of this methodology and act as a bridge helping to connect adversary behavior (tactics and techniques) to the security controls that mitigate those behaviors. The methodology is an iterative process that consists of four main steps. Each step is designed to apply threat specific information from an adversarial perspective to help align ATT&CK mitigations with a set of relevant security controls to mitigate a given technique or sub-technique. The four steps are:

1. **ATT&CK Mitigation Review** - Analyzing ATT&CK mitigations in relation to the specific techniques and sub-techniques.
2. **ATT&CK Technique Review** - Understanding adversary objectives and goals a technique or sub-technique is designed to carry out.
3. **Security Control Review** - Examining security controls in the context of the mitigation and specific techniques.
4. **Create a Mapping** - Identifying and creating security control mappings to ATT&CK techniques and sub-techniques. 

<img src="/docs/mapping_overview.png" width="900px">

_Above: Security Control Mapping Methodology_

## ATT&CK Mitigation Review: Analyzing ATT&CK mitigations (Step 1)

ATT&CK’s mitigations include configurations, tools, or processes that can prevent adversary techniques and sub-techniques from accomplishing the desired tactical objective and goal. Studying mitigation strategies provides concepts and technologies to consider as part of ensuring that relevant and applicable security controls are identified. Understanding the specific context of what a given mitigation is preventing and how a mitigation is associated with or applies to a technique or sub-technique guides the security control analysis and initial selection of candidate security controls.

As an example, consider the ATT&CK mitigation for Credential Access Protection (ID:M1043). This mitigation identifies several techniques and sub-techniques related to adversaries successfully obtaining account credentials (i.e., login and password information), including several forms of credential dumping. The obtained credentials can then be used to conduct further attacks, such as performing lateral movements and accessing restricted information.

## ATT&CK Technique Review: Understanding adversary objectives and goals (Step 2)

The next step of the security control mapping methodology involves understanding the context of the attack objectives and goals, or “what” an adversary is looking to gain by performing a given action. ATT&CK techniques and sub-techniques represent the individual actions adversaries make and identify what the adversary achieves or pieces of information the adversary learns by performing an action, and can be associated with many ATT&CK mitigations depending on the tactical objective and goal the technique is trying to achieve. Understanding these adversarial techniques, what adversaries will do during an attack, and what goals will be achieved provides meaningful information to begin determining specific security controls to mitigate and defend against specific adversarial actions.

For example, a specific technique addressed by M1043 Credential Access Protection is OS Credential Dumping is (ID: T1003). This technique is used by adversaries attempting to dump credentials to obtain account login and credential material, normally in the form of a hash or a clear text password, from the operating system and software. There is also a more specific behavior under this technique related to M1043, the sub-technique LSASS Memory (ID: T1003.001). This sub-technique involves adversary attempts to access credential material stored in the process memory of the Local Security Authority Subsystem Service (LSASS). 

## Security Control Review: Examining security controls and deconstructing techniques (Step 3)

Next, it is necessary to understand and identify the security concepts and technologies that can be used to prevent a given action from being successfully executed as well. This entails understanding of “how” an adversary achieves its objectives and goals. ATT&CK techniques and sub-techniques provide this relevant contextual information such as technical attributes and domain specific information, platform specific information, configuration concepts, and tools. The context derived from a given action that specifies how that action will be performed helps pinpoint and highlight the selection of security controls to map to a given technique or sub-technique.

For example, technique T1003 OS Credential Dumping and sub-technique T1003.001 LSASS Memory can be mapped to preventative concepts and technologies provided by NIST 800-53 security control families of Access Control (AC), Configuration Management (CM), Risk Assessment (RA), and System and Information Integrity (SI). Additional contextual information provided identifies specific controls mapped to T1003 and T1003.01: AC-3 and AC-4 for Access Flow Enforcement and Information Flow Enforcement, CM-2 Baseline Configuration and CM-6 Configuration Settings, RA-5 for Vulnerability Scanning, and SI-4 for System Monitoring.

## Create a Mapping: Identifying and creating security control mappings (Step 4)

The previous three steps of the methodology provide the analytical context to identify a list of candidate security controls. Additional context and information can be obtained from the ATT&CK knowledge base, including detection methods providing operational attributes of the techniques and references providing attack-specific details based on real-world observations. Once this candidate list of security controls has been identified, it is further reviewed, analyzed, and tailored in line with the control mapping scoping decisions to fully determine matches to techniques and/or sub-techniques. When this is completed, the security control selection is finalized and the mappings are created and associated with the specific technique or sub-technique.

To continue with the example, further review and analysis confirms the identified control selection and the mappings can be created for the technique T1003 OS Credential Dumping and sub-technique T1003.001 LSASS Memory. The resultant mappings in the form of regular expressions (regex) are: 
| Techniques | Controls |
| ---------- | -------- |
| T1003(\.001)?	| AC-(3|4) |
| T1003(\.001)?	| CM-(2|6) |
| T1003(\.001)?	| RA-5 |
| T1003(\.001)?	| SI-4 |


## References

1. [Strom, Blake E., et al. (2020, March). MITRE ATT&CK®: Design and Philosophy. Retrieved September 16, 2020.](https://attack.mitre.org/docs/ATTACK_Design_and_Philosophy_March_2020.pdf)
