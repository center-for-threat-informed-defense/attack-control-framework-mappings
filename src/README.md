# Utility Scripts

This folder contains framework-agnostic utility scripts for Security Control Framework Mappings to ATT&CK. 

| Script | Purpose |
|:-------|:--------|
| list_mappings.py | Creates a human readable list of mappings from the STIX mapping data. This script is capable of generating outputs in xlsx, csv, html, and markdown formats. |
| make.py | Rebuilds all the data in the repository based on the state of the mappings file. This will create new layers, overwrite the ATT&CK Enterprise data, mappings and controls. |
| mappings_to_heatmaps.py | Enables visualization of the control mappings in the ATT&CK Matrix. Builds [ATT&CK Navigator](https://github.com/mitre-attack/attack-navigator) heatmap layers. These layers can also be found in the `layers` folder of each control framework. |
| substitute.py | Enables construction of the ATT&CK Website and ATT&CK Navigator with controls taking the place of mitigations. Uses the ATT&CK STIX content from [MITRE/CTI](https://github.com/mitre/cti) and substitutes the controls and mappings for the ATT&CK mitigations. The output STIX bundle can be used as input to the [ATT&CK Navigator](https://github.com/mitre-attack/attack-navigator) or [ATT&CK website](https://github.com/mitre-attack/attack-website). The output of this script can also be found in the `data` folder of each control framework. See [Substituting Controls for ATT&CK Mitigations](/docs/visualizations.md#substituting-controls-for-attck-mitigations) for more information on how to use the substituted data. |
