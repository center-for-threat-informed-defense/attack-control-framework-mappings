import pandas as pd
import os
from tqdm import tqdm
import re
import stix2


# AC-1            is a   CONTROL                                    ^\w+-\d+$
# AC-1a.          is a   STATEMENT             about   AC-1         ^\w+-\d+\w+.$
# AC-1a.1         is a   SUB-STATEMENT         of      AC-1a.       ^\w+-\d+\w+.\d+.$
# ...
# AC-2            is a   CONTROL                                    ^\w+-\d+$
# AC-2 (7)        is a   CONTROL ENHANCEMENT   of      AC-2         ^\w+-\d+ \(\d+\)$
# AC-2 (7)(a)     is a   STATEMENT             about   AC-2 (7)     ^\w+-\d+ \(\d+\)\(\w\)$
# AC-19 (4)(b)(1) is a   SUB-STATEMENT         of      AC-19 (4)(b) ^\w+-\d+ \(\d+\)\(\w\)\(\d\)$

id_formats = {
    "control": [                                                # CONTROL FORMATS:
        re.compile("^\w+-\d+$")                                 # AC-1
    ],
    "control_enhancement": [                                    # CONTROL ENHANCEMENT FORMATS:
        re.compile("^\w+-\d+ \(\d+\)$")                         # AC-1 (1)
    ],
    "statement": [                                              # STATEMENT FORMATS:
        re.compile("^\w+-\d+\w+\.$"),                           # AC-1a.
        re.compile("^\w+-\d+ \(\d+\)\(\w\)$"),                  # AC-1 (1)(a)
    ],
    "substatement": [                                           # SUB-STATEMENT FORMATS:
        re.compile("^\w+-\d+\w+\.\d+\.$"),                      # AC-1a.1
        re.compile("^\w+-\d+ \(\d+\)\(\w\)\(\d\)$")             # AC-1 (1)(a)(1)
    ]
}

def row_type(row):
    """from a pandas series determine if it's a "control", "control_enhancement" or "statement" and return the type as a string"""
    # check all known formats
    for id_format_group in id_formats:
        # test against format
        for id_format in id_formats[id_format_group]:
            if id_format.match(row["NAME"]):
                return id_format_group
    raise RuntimeError(f"unknown control name format for control {row['NAME']}")

class Statement:
    """helper class defining a statement or substatement"""
    def __init__(self, row):
        self.external_id = row["NAME"]
        self.description = row["DESCRIPTION"]
        self.substatements = []
    
    def add_substatement(self, row):
        self.substatements.append(Statement(row))

class Control:
    """helper class defining a Control"""
    def __init__(self, row, control_ids):
        """constructor"""
        self.external_id = row["NAME"]
        self.name = row["TITLE"].title() # titlecase
        self.family = row["FAMILY"].title() # titlecase
        self.supplemental = row["SUPPLEMENTAL GUIDANCE"]
        self.impact = row["BASELINE-IMPACT"]
        self.priority = row["PRIORITY"]
        self.related = row["RELATED"].split(",")
        self.enhancement = row_type(row) == "control_enhancement"
        self.description = row["DESCRIPTION"]
        self.statements = []
        # try to manually set the STIX ID from the control_ids mapping, if not present it will randomly generate
        self.stix_id = control_ids[self.external_id] if control_ids and self.external_id in control_ids else None

    def add_statement(self, row):
        """add a statement to this control"""
        self.statements.append(Statement(row))

    def add_substatement(self, row):
        """add a substatement to the most recently defined statement of this control"""
        self.statements[-1].add_substatement(row)

    def format_description(self):
        """format and return the description, supplemental guidance and statements as a markdown string"""
        fulldesc = self.description
        if len(self.statements) > 0:
            fulldesc += "\n\n"
            for statement in self.statements:
                fulldesc += f"- *{statement.external_id}*: {statement.description}\n"
                for substatement in statement.substatements:
                    fulldesc += f"    - *{substatement.external_id}*: {substatement.description}\n"
        if self.supplemental: fulldesc += "\n" + self.supplemental
        return fulldesc

    def toStix(self):
        return stix2.CourseOfAction(
            id = self.stix_id,
            name = self.name,
            description = self.format_description(),
            external_references = [ {
                "source_name": "NIST 800-53",
                "external_id": self.external_id
            } ]
        )


def parse_controls(controlpath, control_ids=None):
    """parse the NIST800-53 controls and return a STIX bundle
    :param controlpath the filepath to the controls TSV file
    :param control_ids is a dict of format {control_name: stixID} which maps control names (e.g AC-1) to desired STIX IDs
    """

    print("parsing controls")
    print(control_ids)
    
    controls_df = pd.read_csv(controlpath, sep="\t", keep_default_na=False)
    
    controls = []
    for index, row in tqdm(list(controls_df.iterrows()), desc="parsing NIST 800-53"):
        rowtype = row_type(row)
        if rowtype == "control" or rowtype == "control_enhancement":
            controls.append(Control(row, control_ids))
        elif rowtype == "statement":
            controls[-1].add_statement(row)
        elif rowtype == "substatement":
            controls[-1].add_substatement(row)
    
    stixcontrols = []
    for control in tqdm(controls, desc="creating STIX"):
        stixcontrols.append(control.toStix())
    bundle = stix2.Bundle(*stixcontrols, spec_version="2.0")
    return bundle