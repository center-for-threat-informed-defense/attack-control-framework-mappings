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
# 5 April 2021
### Fixes
- Fixed a bug where subcontrol-of relationships were not being created between controls and enhancements in nist-800-53-r5.
- Updates to mappings in nist-800-53-r5 to address withdrawn controls (SA family) and to remove policy control (XX-1) mappings.

# 12 January 2021
### Fixes
- Fixes parse_mappings.py for nist800-53-r4 and nist800-53-r5 to remove duplicate entries in "mitigates"
- Rerun make.py to update all content based on the fix
