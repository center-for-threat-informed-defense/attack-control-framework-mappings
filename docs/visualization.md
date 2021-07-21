# Visualization
This repository includes several ways to visualize the mappings. 

## ATT&CK Navigator Layers

This project provides [ATT&CK Navigator](https://github.com/mitre-attack/attack-navigator) Layers representing the mappings to ATT&CK. You can find the Layer files in the `/frameworks/` folder:
- [NIST 800-53 Revision 4 Layers](/frameworks/nist800-53-r4/layers)
- [NIST 800-53 Revision 5 Layers](/frameworks/nist800-53-r5/layers)

## Mappings Spreadsheet

An excel spreadsheet is provided listing all of the mappings for each framework in a tabular format. You can find the spreadsheets within the `/frameworks/` folder:
- [NIST 800-53 Revision 4 Mappings Spreadsheet](/frameworks/nist800-53-r4/nist800-53-r4-mappings.xlsx)
- [NIST 800-53 Revision 5 Mappings Spreadsheet](/frameworks/nist800-53-r5/nist800-53-r5-mappings.xlsx)

The [listMappings](/src/) script can be used to generate this same information in additional formats:
- Excel spreadsheet
- CSV
- HTML table
- Markdown table

## Substituting Controls for ATT&CK Mitigations

The [substitute.py](/src/substitute.py) utility script builds ATT&CK STIX bundles where controls and mappings take the place of ATT&CK mitigations, thereby enabling construction of the ATT&CK Website and ATT&CK Navigator with controls taking the place of mitigations. This section describes the usage of these specialty bundles, which can be found on this repo alongside their data in the framework `stix` folders:
- [NIST 800-53 Revision 4 Substituted STIX bundle](/frameworks/nist800-53-r4/stix/nist800-53-r4-enterprise-attack.json)
- [NIST 800-53 Revision 5 Substituted STIX bundle](/frameworks/nist800-53-r5/stix/nist800-53-r5-enterprise-attack.json)

_Note: substitute.py is implemented such that only controls with mappings to ATT&CK Techniques are present in the substituted STIX bundle. If you want to build the substituted bundle with the full set of controls, run substitute.py with the `--allow-unmapped` flag._ 

### Constructing the ATT&CK Navigator with controls as mitigations
The ATT&CK Navigator can be constructed with controls as mitigations by following the below methodology. Controls will be shown in the place of mitigations in the multi-select interface, allowing users to quickly select the techniques mapped to each control listed in that UI.
1. Clone the [attack-navigator](https://github.com/mitre-attack/attack-navigator) github repository.
2. Put the substituted STIX data in the `nav-app/src/assets` folder.
3. in `nav-app/src/assets/config.json`, replace the default `enterprise_attack_url` value with `"assets/[substituted-stix-bundle-name]"`.
4. Follow the [Install and Run](https://github.com/mitre-attack/attack-navigator#install-and-run) instructions of the ATT&CK Navigator documentation. 

### Constructing the ATT&CK Website with controls as mitigations
The ATT&CK Website can be constructed with controls as mitigations by following the below methodology. The mitigation pages on the website will instead contain controls, and the mappings of mitigations to ATT&CK Techniques will be replaced with the control mappings.
1. Clone the [attack-website](https://github.com/mitre-attack/attack-website) github repository.
2. Replace `data/stix/enterprise-attack.json` with the substituted STIX data (renaming the substituted STIX file to be `enterprise-attack.json`).
3. In `modules/config.py`, append the control framework identifier to the `source_names` array. The framework identifier can be found in the `framework_id` field of the framework's `input/config.json` file.
    - For NIST 800-53 Revision 4, the source name to append is `"NIST 800-53 Revision 4"`
    - For NIST 800-53 Revision 5, the source name to append is `"NIST 800-53 Revision 5"`
4. Follow the [Install and Build](https://github.com/mitre-attack/attack-website#install-and-build) instructions of the ATT&CK Website documentation.

## See also
- [Mapping Methodology](/docs/mapping_methodology.md) for a description of the general process used to create the control mappings.
- [STIX Format](/docs/STIX_format.md) for more information about the STIX representation of the controls and mappings.
