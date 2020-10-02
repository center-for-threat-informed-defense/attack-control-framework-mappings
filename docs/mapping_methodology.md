# Mapping Methodology

This document outlines the methodology used for this project, but it is not the only way such mappings might be created, as other control frameworks may not align well with this process. As such, the methodology described in this document has been shown to be an effective means of creating mappings between security control frameworks, such as NIST 800-53 and MITRE ATT&CK®.  Mapping security control frameworks to ATT&CK provides a powerful way for organizations to see their security control coverage against associated ATT&CK techniques and establishes a means to integrate ATT&CK-based threat information within the risk management process.  

The ATT&CK knowledge base and model for cyber adversary behavior reflects the various phases of an adversary’s attack lifecycle and the platforms they are known to target. The basis of ATT&CK is the set of techniques and sub-techniques that represent actions that adversaries can perform to accomplish objectives and goals. Those objectives and goals are represented by the tactic categories that techniques and sub-techniques fall under.<sup>[[1]](https://attack.mitre.org/docs/ATTACK_Design_and_Philosophy_March_2020.pdf)</sup> The methodology described below leverages the information in the ATT&CK knowledge base and its underlying data model to create context that is then used to select security controls to map to a given technique or sub-technique.

The methodology consists of four main phases. Each phase is designed to apply threat specific information from an adversarial perspective to help align ATT&CK mitigations with a set of relevant security controls to mitigate a given technique or sub-technique.   The four phases include the following:

1. **Understanding adversary objectives and goals** a technique or sub-technique is designed to carry out.
2. **Deconstructing the technique and sub-technique** to understand how an adversary will achieve its intended goal and objective.
3. **Analyzing ATT&CK mitigations in relation** to the specific techniques and sub-techniques.
4. **Identifying and creating security control** mappings to ATT&CK techniques and sub-techniques.

## Understanding adversary objectives and goals 

The first phase of the security control mapping methodology involves understanding the  objectives and goals of an attack, or “what” an adversary is looking to gain in performing a given action. Understanding what adversaries will do during an operation provide meaningful information that can be used to identify applicable security controls to defend against specific  actions such as (but not limited to), lateral movement, data exfiltration, information discovery and defense evasion.

<img src="/docs/mapping_overview.png" width="900px">

_Above: Security Control Mapping Methodology_

## Deconstructing the technique and sub-technique

Once the objectives and goals are understood, it is necessary to understand “how” an adversary achieves its objectives and goals. Understanding the intended goal and objectives is necessary for determining which security controls can be implemented to help mitigate adversary actions. ATT&CK techniques and sub-techniques provide relevant contextual information such as technical attributes and domain specific information, platform specific information, configuration concepts, and tools. The context derived from a given action that specifies how that action will be performed helps pinpoint and highlight a subset or candidate list of security controls to map to a given technique or sub-technique. 

## Analyzing ATT&CK mitigations

Once techniques and sub-techniques are understood, it is necessary to understand the security concepts and technologies that can be used to prevent a given action from being successfully executed. ATT&CK’s mitigations include configurations, tools, or processes that can prevent adversary techniques and sub-techniques from accomplishing the desired tactical objective and goal.  Outlining mitigation strategies provides concepts and technologies to consider as part of ensuring that relevant and applicable security controls are identified.  Understanding the specific context and how a mitigation is associated with or applies to a technique or sub-technique guides the security control analysis and initial selection of candidate security controls.   The security control analysis should take into consideration that a technique or sub-technique can be associated with many ATT&CK mitigations depending on the tactical objective and goal the technique is trying to achieve.  

## Identifying and creating security control mappings

Use the derived context from the first three phases of the methodology to do a security control analysis to identify a list of candidate security controls. If additional context and information is needed, read the references provided in the ATT&CK knowledge base to understand attack details and review detection methods to determine operational attributes associated with the techniques.  Once this candidate list of security controls has been identified, they need to be reviewed, analyzed, and tailored to fully determine implicit or explicit match to techniques and/or sub-techniques.  Once this is completed, the security control selection can be finalized, and the mappings can be created and associated with the specific technique or sub-technique.

## References

1. [Strom, Blake E., et al. (2020, March). MITRE ATT&CK®: Design and Philosophy. Retrieved September 16, 2020.](https://attack.mitre.org/docs/ATTACK_Design_and_Philosophy_March_2020.pdf)
