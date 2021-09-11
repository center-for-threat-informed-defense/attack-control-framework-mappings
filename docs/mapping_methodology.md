# Mapping Methodology

This document describes the methodology used to map security control frameworks to MITRE ATT&CK®. While the methodology is based upon our experience mapping NIST Special Publication 800-53 to ATT&CK, the methodology was designed to be easily tailored and applied to other security control frameworks. Mapping security control frameworks to ATT&CK provides a powerful way for organizations to see their security control coverage against associated ATT&CK techniques and establishes a means to integrate ATT&CK-based threat information within the risk management process.  

MITRE ATT&CK is a globally-accessible knowledge base of adversary tactics and techniques based on real-world observations. The ATT&CK knowledge base represents adversary goals as tactics and the specific behaviors to achieve those goals (how) as techniques and sub-techniques. ATT&CK's Mitigation structure represents security concepts and classes of tools that may prevent successful execution of a set of techniques or sub-techniques. <sup>[[1]](https://attack.mitre.org/docs/ATTACK_Design_and_Philosophy_March_2020.pdf)</sup> The methodology described below leverages the information in the ATT&CK knowledge base and its underlying data model to create context that is then used to select security controls to map to a given technique or sub-technique.

Much like an ATT&CK mitigation, a mapping between a security control and an ATT&CK technique or sub-technique means that the security control may prevent successful execution of the technique or sub-technique. This methodology does not define degrees of mapping or control effectiveness. Controls are either mapped or not mapped to a given technique or sub-technique. In this way the mappings provide an easily understood foundational resource that is intended to inform risk management decisions. 

ATT&CK’s mitigations are at the core of this methodology and act as a bridge helping to connect adversary behavior (tactics and techniques) to the security controls that mitigate those behaviors. The methodology defines an iterative process that consists of four main steps. Each step incrementally builds understanding allowing the analyst to understand ATT&CK techniques and sub-techniques in the context of a mitigation and then select relevant security controls to map. The four steps are:

1. **ATT&CK Mitigation Review** - Reviewing and analyzing each mitigation.
2. **ATT&CK Technique Review** - Understanding adversary objectives and goals a technique or sub-technique is designed to carry out.
3. **Security Control Review** - Examining security controls in the context of the mitigation and specific technique.
4. **Create a Mapping** - Identifying and creating security control mappings to ATT&CK technique and sub-techniques. 

<img src="/docs/mapping_overview.png" width="900px">

_Above: Security Control Mapping Methodology_

## ATT&CK Mitigation Review: Analyzing ATT&CK mitigations (Step 1)

ATT&CK’s mitigations describe security concepts and classes of tools that may prevent successful execution of a set of techniques or sub-techniques. Studying these mitigations provides concepts and technologies to consider as part of ensuring that relevant and applicable security controls are identified. Understanding the specific context of what a given mitigation is preventing and how a mitigation is associated with or applies to a technique or sub-technique guides the security control analysis and initial selection of candidate security controls.

As an example, consider the ATT&CK mitigation for Credential Access Protection [ID: M1043](https://attack.mitre.org/mitigations/M1043/). This mitigation describes a broad class of capabilities that prevent credential access and credential dumping. M1043 then identifies several techniques and sub-techniques that could be prevented by this class of security capabilities. Due to the generally abstract nature of mitigations in ATT&CK, it is common to find that there is more detailed guidance for each technique or sub-technique to which the mitigation is applied. 

## ATT&CK Technique Review: Understanding adversary objectives and goals (Step 2)

The next step of the security control mapping methodology involves examining each technique and sub-technique that the mitigation under review applies to. Each technique and sub-technique must be considered independently as there may be important differences among them that result in different security control mappings. Understanding what the adversary's goal (tactic) and how (technique) they achieve that goal helps to refine our understanding of the mitigation and builds context as we prepare to study relevant security controls. ATT&CK techniques and sub-techniques provide relevant information such as domain specific and platform specific information, configuration concepts, and tools.

For example, a specific technique addressed by M1043 Credential Access Protection is OS Credential Dumping [ID: T1003](https://attack.mitre.org/techniques/T1003). This technique is used by adversaries attempting to dump credentials to obtain account login and credential material, normally in the form of a hash or a clear text password, from the operating system and software. There is also a more specific behavior under this technique related to M1043, the sub-technique LSASS Memory [ID: T1003.001](https://attack.mitre.org/techniques/T1003/001). This sub-technique involves adversary attempts to access credential material stored in the process memory of the Local Security Authority Subsystem Service (LSASS). 

## Security Control Review: Examining security controls and deconstructing techniques (Step 3)

Next, it is necessary to understand and identify the security concepts and technologies that can be used to prevent a given action from being successfully executed. For each technique or sub-technique examined in the previous step, the context of the mitigation under review is applied as security controls are examined. For each security control, determine if it is aligned with the intent of the mitigation under review and if it is relevant to the technique or sub-technique under review. 

For example, technique T1003 OS Credential Dumping and sub-technique T1003.001 LSASS Memory can be mapped to preventative concepts and technologies provided by NIST 800-53 security control families of Access Control (AC), Configuration Management (CM), Risk Assessment (RA), and System and Information Integrity (SI). Additional contextual information provided identifies specific controls mapped to T1003 and T1003.01: AC-3 and AC-4 for Access Flow Enforcement and Information Flow Enforcement, CM-2 Baseline Configuration and CM-6 Configuration Settings, RA-5 for Vulnerability Scanning, and SI-4 for System Monitoring.

## Create a Mapping: Identifying and creating security control mappings (Step 4)

The previous three steps of the methodology provide the analytical context to identify a list of candidate security controls. Once this candidate list of security controls has been identified, it is further reviewed, analyzed, and tailored in line with the control mapping scoping decisions to fully determine matches to techniques and/or sub-techniques. When this is completed, the security control selection is finalized and the mappings are created and associated with the specific technique or sub-technique.

To continue with the example, further review and analysis confirms the identified control selection and the mappings can be created for the technique T1003 OS Credential Dumping and sub-technique T1003.001 LSASS Memory. The resultant mappings are listed below: 

| Technique | Control(s) |
|---|---|
| T1003 | AC-3, AC-4 |
| T1003	| CM-2, CM-6 |
| T1003	| RA-5 |
| T1003	| SI-4 |
| T1003.001 | AC-3, AC-4 |
| T1003.001	| CM-2, CM-6 |
| T1003.001	| RA-5 |
| T1003.001	| SI-4 |

## Applying the Methodology

This methodology is designed to be tailored as it is applied to security control frameworks. We anticipate that each framework will require its own unique mapping and scoping decisions. These framework specific decisions should be documented in the ReadMe for the framework. As an example, see the [Mapping NIST 800-53 revision 4 to ATT&CK](/frameworks/ATT%26CK-v8.2/nist800-53-r4#mapping-nist-800-53-revision-4-to-attck) section of the NIST 800-53 Rev. 4 mapping documentation. 

## References

1. [Strom, Blake E., et al. (2020, March). MITRE ATT&CK®: Design and Philosophy. Retrieved September 16, 2020.](https://attack.mitre.org/docs/ATTACK_Design_and_Philosophy_March_2020.pdf)
