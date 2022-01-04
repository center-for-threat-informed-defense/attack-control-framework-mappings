## How to Update the NIST 800-53 Mappings
This document is intended for developers who wish to update the mappings

Instructions to do a release with new NIST 800-53 mappings

### Preconditions
1.	Mapping team has created two spreadsheets; one for NIST 800-53 r4 and r5


### Steps:
1. Set up a new folder (e.g., ATT&CK400.0). Its contents should look like this:
```
frameworks/
├── ATT&CKv10.1/ <--- Existing folder (not expanded)
└── ATT&CKvX.Y/ <-- New Folder Structure
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
  a. Copy the 800-53-r4 spreadsheet to `frameworks/ATT&CKvX.Y/nist800-53-r4/nist800-53-r4-mappings.xlsx`  
  b. Copy a prior version readme file to `frameworks/ATT&CKvX.Y/nist800-53-r4/README.md` and perform the following edits:  
      i. Line 3: Change the ATT&CK version to the correct one  
      ii. Line 7: Change mappings version to 1.0  
      iii. Line 7: Change last updated to today's date (e.g., 22 December 2021)  
      iv. Line 7: Change the ATT&CK version to the correct one  
  c. Copy a prior version parse.py file to `frameworks/ATT&CKvX.Y/nist800-53-r4/parse.py` and do not make any edits  
  d. Copy a prior version parse_controls.py file to `frameworks/ATT&CKvX.Y/nist800-53-r4/parse_controls.py` and do not make any edits  
  e. Copy a prior version parse_mappings.py file to `frameworks/ATT&CKvX.Y/nist800-53-r4/parse_mappings.py` and do not make any edits  
  f. Copy a prior version nist800-53-r4-controls.tsv to `frameworks/ATT&CKvX.Y/nist800-53-r4/input/nist800-53-r4-controls.tsv` and do not make any edits  
  g. Save a copy of `frameworks/ATT&CKvX.Y/nist800-53-r4/nist800-53-r4-mappings.xlsx` as a tab separated format in `frameworks/ATT&CKvX.Y/nist800-53-r4/input/nist800-53-r4-mappings.tsv`  
      i. Depending on your setup, you may have to save the file as .txt and then rename to .tsv  
  h. Copy a prior version `input/README.md` to `frameworks/ATT&CKvX.Y/nist800-53-r4/input/README.md` and do not make any edits  
  i. Copy a prior version `input/config.json` to `frameworks/ATT&CKvX.Y/nist800-53-r4/input/config.json` and make the following changes:  
      i. Line 4: Change the ATT&CK version to be correct  
      ii. Line 5: Change the mappings_version to be `1.0`  
3. Repeat the prior steps for NIST 800-53 r5  
4. Set up and activate the project’s virtual environment  
```
virtualenv venv  
source venv/bin/activate  
pip install -r requirements/requirements.txt
```  
5. Edit src/make.py:  
  a. Append “vX.Y” to the ATT&CK version list on line 18  
6. Run python src/make.py  
  a. Error Q&A:  
      i. NOTE WELL: Any changes to the spreadsheet will require re-creating the .tsv file  
      ii. ERROR: cannot find techniqueID T1547(.\011)  
          Answer: A regex in the spreadsheet did not match an ATT&CK technique. In the above case, the regex was incorrect (should have been “\.011”) and the spreadsheet needed to be corrected  
