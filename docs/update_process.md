## How to Update the NIST 800-53 Mappings
This document is intended for developers who wish to update the mappings

Instructions to do a release with new NIST 800-53 mappings

### Preconditions
1.	Mapping team has created two spreadsheets; one for NIST 800-53 r4 and r5


### Steps:
1. Set up a new folder (e.g., ATT&CK-v400.0). Its contents should look like this:
   ```
   frameworks/
   ├── ATT&CK-v10.1/ <--- Existing folder (not expanded)
   └── ATT&CK-vX.Y/  <--- New Folder Structure
       ├── nist800-53-r4/
       │   ├── input/
       │   ├── layers/
       │   └── stix/
       └── nist800-53-r5/
           ├── input/
           ├── layers/
           └── stix/
   ```
2. Populate the NIST 800-53 r4 folder:
   1. Copy the 800-53-r4 spreadsheet to `frameworks/ATT&CK-vX.Y/nist800-53-r4/nist800-53-r4-mappings.xlsx`
   2. Copy a prior version readme file to `frameworks/ATT&CK-vX.Y/nist800-53-r4/README.md` and perform the following edits:
      1. Line 3: Change the ATT&CK version to the correct one
      2. Line 7: Change mappings version to 1.0
      3. Line 7: Change last updated to today's date (e.g., 22 December 2021)
      4. Line 7: Change the ATT&CK version to the correct one
   3. Copy a prior version parse.py file to `frameworks/ATT&CK-vX.Y/nist800-53-r4/parse.py` and do not make any edits
   4. Copy a prior version parse_controls.py file to `frameworks/ATT&CK-vX.Y/nist800-53-r4/parse_controls.py` and do not make any edits
   5. Copy a prior version parse_mappings.py file to `frameworks/ATT&CK-vX.Y/nist800-53-r4/parse_mappings.py` and do not make any edits
   6. Copy a prior version nist800-53-r4-controls.tsv to `frameworks/ATT&CK-vX.Y/nist800-53-r4/input/nist800-53-r4-controls.tsv` and do not make any edits
   7. Save a copy of `frameworks/ATT&CK-vX.Y/nist800-53-r4/nist800-53-r4-mappings.xlsx` as a tab separated format in `frameworks/ATT&CK-vX.Y/nist800-53-r4/input/nist800-53-r4-mappings.tsv`
      1. Depending on your setup, you may have to save the file as .txt and then rename to .tsv
   8. Copy a prior version `input/README.md` to `frameworks/ATT&CK-vX.Y/nist800-53-r4/input/README.md` and do not make any edits
   9. Copy a prior version `input/config.json` to `frameworks/ATT&CK-vX.Y/nist800-53-r4/input/config.json` and make the following changes:
      1. Line 4: Change the ATT&CK version to be correct
      2. Line 5: Change the mappings_version to be `1.0`
3. Repeat the prior steps for NIST 800-53 r5
4. Set up and activate the project’s virtual environment
   ```
   virtualenv venv
   source venv/bin/activate
   pip install -r requirements/requirements.txt
   ```
5. Edit src/make.py:
   1. Append "vX.Y" to the ATT&CK version list on line 18
6. Run python src/make.py
   1. Error Q&A:
      1. NOTE WELL: Any changes to the spreadsheet will require re-creating the .tsv file
      2. ERROR: cannot find techniqueID T1547(.\011)
         - Answer: A regex in the spreadsheet did not match an ATT&CK technique. In the above case, the regex was incorrect (should have been "\.011") and the spreadsheet needed to be corrected
