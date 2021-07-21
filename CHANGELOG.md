<!--    CHANGELOG FORMAT                                                -->

<!--    Completed Entry template:                                       -->
<!--                                                                    -->
<!--    # Date in DD MMM YYYY format                                    -->
<!--    ### New Features                                                -->
<!--    ### Improvements                                                -->
<!--    ### Fixes                                                       -->

<!--    Entries for pull request template:                              -->
<!--                                                                    -->
<!--    # Changes staged on develop                                     -->
<!--    ### New Features                                                -->
<!--    ### Improvements                                                -->
<!--    ### Fixes                                                       -->

# 19 July 2021
## nist800-53-r4 v2.0 and nist800-53-r5 v2.0
### Fixes
- Release of the security control mappings and tools updated with ATT&CK-v9.0, including layers and stix data
- Update project structure to hold prior mappings created for this repo (ATT&CK-v8.2)
- Update project structure and scripts, code quality updates, tests, coverage


# 18 May 2021
### Fixes
- NIST 800-53 R4 layers updated with attack-navigator 4.3. See issue [#65](https://github.com/center-for-threat-informed-defense/attack-control-framework-mappings/issues/65).
- NIST 800-53 R5 layers updated with attack-navigator 4.3. See issue [#65](https://github.com/center-for-threat-informed-defense/attack-control-framework-mappings/issues/65).
- mappingsToHeatmaps.py also updated to indicate attack-navigator version 4.3.

# 5 April 2021
## nist800-53-r5 v1.3
### Fixes
- Fixed a bug where subcontrol-of relationships were not being created between controls and enhancements in nist-800-53-r5. See issue [#61](https://github.com/center-for-threat-informed-defense/attack-control-framework-mappings/issues/61).
- Updates to mappings in nist-800-53-r5 to address withdrawn controls (SA family) and to remove policy control (XX-1) mappings.

# 3 February 2021
## nist800-53-r4 v1.2 and nist800-53-r5 v1.2
### Fixes
- Fixes parse_mappings.py for nist800-53-r4 and nist800-53-r5 to remove duplicate mappings. See issue [#58](https://github.com/center-for-threat-informed-defense/attack-control-framework-mappings/issues/58).

# 7 January 2021
## nist800-53-r4 v1.1 and nist800-53-r5 v1.1
### Fixes
- Fixed broken regex which was leading to erroneous mappings, in particular mappings to control enhancements. See issue [#56](https://github.com/center-for-threat-informed-defense/attack-control-framework-mappings/issues/56).

# 15 December 2020
## nist800-53-r4 v1.0 and nist800-53-r5 v1.0
- Initial release of security control framework mapping methodology and tools. 
- Initial release of NIST 800-53 R4 mappings to ATT&CK version 8.1.
- Initial release of NIST 800-53 R5 mappings to ATT&CK version 8.1.
