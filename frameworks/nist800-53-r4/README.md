# NIST 800-53 Revision 4 Control Mappings

This folder contains data and parsers for the NIST 800-53 Revision 4 control framework, and the mappings of that framework to ATT&CK.


| Data ||
|------|------|
| [spreadsheet](nist800-53-r4-mappings.xlsx) | Lists all of the mappings for this control framework.
| [layers](layers) | [ATT&CK Navigator](https://github.com/mitre-attack/attack-navigator) layers showing the mappings in the context of the ATT&CK Matrix. |
| [stix](stix) | Output STIX 2.0 json data. See the README in that folder for more information. |
| [input](input) | Input spreadsheets from which the STIX is built. To rebuild the STIX data from the input spreadsheets, run `python3 parse.py`.See the README in that folder for more information. |

## Extended Fields

The NIST 800-53 Revision 4 STIX data extends the controls format with the following properties:

| STIX field | type | description |
|:-----------|:-----|:------------|
| `x_mitre_impact` | list of strings | the baseline-impact of the control or enhancement. Values include `"LOW"`, `"MODERATE"`, `"HIGH"`. |
| `x_mitre_family` | string | The family to which the control belongs. |
| `x_mitre_priority` | string | The priority of the control. Control enhancements inherit this value from their parent control. |

## Mappings Methodology

This methodology provides guidance and outlines the process for mapping security control frameworks such as NIST 800-53 revision 4 to MITRE ATT&CK®. Mapping security control frameworks to ATT&CK provides a powerful way for organizations to see their security control coverage against associated ATT&CK techniques and establishes a means to integrate ATT&CK-based threat information within the risk management process.

The ATT&CK knowledge base and model for cyber adversary behavior, reflects the various phases of an adversary’s attack lifecycle and the platforms they are known to target. The basis of ATT&CK is the set of techniques and sub-techniques that represent actions that adversaries can perform to accomplish objectives. Those objectives are represented by the tactic categories that techniques and sub-techniques fall under.<sup>[[1]](https://attack.mitre.org/docs/ATTACK_Design_and_Philosophy_March_2020.pdf)</sup> This methodology leverages the information in the ATT&CK knowledge base and its underlying data model to create context that is then used to select security controls to map to a given technique or sub-technique. 

The methodology consists of four main phases. Each phase is designed to apply threat specific information from an adversarial perspective to help identify ATT&CK mitigations for mapping to a set of security controls. The four phases include the following:

1. **Understanding adversary objectives** for which a technique or sub-technique is designed to carry out.
2. **Deconstructing the technique and sub-technique** to understand how an adversary will achieve its intended goal and objective.  
3. **Analyzing ATT&CK mitigations in relation** to the specific technique and sub-technique.
4. **Analyzing and identifying security controls** for mappings to ATT&CK techniques. 

<img src="/docs/nist-800-53-r4-methodology.png" width="900px">

*Above: Security Control Mapping Methodology*

### Understanding adversary objectives

The first phase of the security control mapping methodology involves understanding the adversary’s objectives and goals during an attack, or “what” the adversary is looking to gain in performing a given action. It provides context for understanding adversary behavior and identifying what an adversary is looking to achieve during a given operation.  ATT&CK tactics provide meaningful information that can be used to identify applicable security controls, such as “What is the adversary trying to achieve?”, “Is the adversary trying to move laterally?”, or “Is the adversary trying to exfiltrate data, discover information, or evade defenses?”. The ATT&CK tactic also provides additional details regarding the platform and domain the adversary is operating within, which helps in deconstructing techniques and sub-techniques and identifying potential ATT&CK mitigations to defend against those adversary actions.  

### Deconstructing the technique and sub-technique

Once the adversary’s objectives are understood, it is necessary to understand “how” an adversary achieves its objectives. ATT&CK techniques and sub-techniques provide relevant contextual information such as technical attributes and domain specific information, platform specific information, configuration concepts, and tools. This additional information about how and adversary may achieve its intended goal and objectives is necessary for understanding which security controls can be implemented to help mitigate adversary actions. The context derived from a given action performed by an adversary to achieve its objectives helps pinpoint and highlight a subset or candidate list of security controls to map to a given technique or sub-technique. 

### Analyzing ATT&CK mitigations

Once the adversary’s techniques are understood, it is necessary to understand the security concepts and technologies that can be used to prevent adversary operations from being successfully executed. ATT&CK’s mitigations include configurations, tools, or processes that can prevent adversary techniques and sub-techniques from accomplishing the desired tactical objective.  Outlining mitigation strategies provides concepts and technologies to consider as part of the adversary operational and behavioral analysis to ensure relevant and applicable security controls are identified.  The derived context also helps outline mitigation strategies that can be used to identify a candidate list of security controls to defend against a given action or set of actions by an adversary.  In addition, a technique or sub-technique can be associated with many mitigations depending on the tactical objective the technique is trying to achieve. Therefore, understanding the specific context and how that mitigation is associated with or applies to a technique, sub-technique guides the security control analysis and initial selection of candidate security controls.

### Analyzing and identifying security controls 

Finally, the candidate list of security controls needs to be further reviewed, analyzed, and tailored to fully determine implicit or explicit match to techniques and/or sub-techniques.  For additional context and information, research references provided in the ATT&CK knowledge base to understand attack details and review detection methods to determine operational attributes associated with the techniques. Once this is complete, the security control selection can be finalized and the mappings can be associated with the specific technique or sub-technique.

### Mapping NIST 800-53 revision 4 to ATT&CK

During the customized analysis and mapping of ATT&CK techniques and sub-techniques to NIST 800-53 revision 4 controls, several decision points were made regarding applicability and relevance. Specifically, the following was considered as part of the decision points:

- A threat-based approach was used to determine the functionality of security controls in mitigating an adversary technical objective.  
- A large focus of this effort is focused on the technical and operational elements and did not typically take into account the management elements which are often focused on organization specific policies and procedures. 
- Alignment of ATT&CK mitigations with a candidate list of security controls to identify and finalize the most applicable and relevant set for threat mitigation.
- Identify top-level applicable security control families, and then pinpoint specific with control enhancements for accuracy and fidelity.  

### References

1. [Strom, Blake E., et al. (2020, March). MITRE ATT&CK®: Design and Philosophy. Retrieved September 16, 2020.](https://attack.mitre.org/docs/ATTACK_Design_and_Philosophy_March_2020.pdf)
