import pandas as pd
import os
from tqdm import tqdm
import re
from stix2.v20 import CourseOfAction, Relationship, Bundle
import itertools
import uuid
import json

id_formats = {
    "control": [                                                # CONTROL FORMATS:
        re.compile("^\w+-\d+$")                                 # AC-1
    ],
    "control_enhancement": [                                    # CONTROL ENHANCEMENT FORMATS:
        re.compile("^(\w+-\d+) \(\d+\)$")                         # AC-1 (1)
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
        """constructor"""
        self.external_id = row["NAME"]
        self.description = row["DESCRIPTION"]
        self.substatements = []
    
    def add_substatement(self, row):
        """add a substatement to this statement"""
        self.substatements.append(Statement(row))

class Control:
    """helper class defining a Control"""
    def __init__(self, row, control_ids, parent=None):
        """constructor"""
        self.external_id = row["NAME"]
        self.name = row["TITLE"].title() # titlecase
        self.family = row["FAMILY"].title() # titlecase
        self.supplemental = row["SUPPLEMENTAL GUIDANCE"]
        self.impact = row["BASELINE-IMPACT"]
        self.related = row["RELATED"].split(",") if row["RELATED"] else []
        self.is_enhancement = row_type(row) == "control_enhancement"
        self.description = row["DESCRIPTION"]
        self.statements = []
        # parent control
        self.parent_id = parent.external_id if self.is_enhancement else None
        self.priority = parent.priority if self.is_enhancement else row["PRIORITY"] # inherit from parent

        # try to manually set the STIX ID from the control_ids mapping, if not present it will randomly generate
        self.stix_id = control_ids[self.external_id] if control_ids and self.external_id in control_ids else f"course-of-action--{str(uuid.uuid4())}"
        control_ids[self.external_id] = self.stix_id # update lookup so that subsequent objects can reference for relationships

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
                fulldesc += f"* **{statement.external_id}** {statement.description}\n"
                for substatement in statement.substatements:
                    fulldesc += f"    * **{substatement.external_id}** {substatement.description}\n"
        if self.supplemental: fulldesc += "\n" + self.supplemental
        return fulldesc

    def toStix(self, framework_id):
        """convert to a stix2 Course of Action"""
        custom_properties = {}
        if self.impact: custom_properties["x_mitre_impact"] = self.impact.split(",")
        if self.priority: custom_properties["x_mitre_priority"] = self.priority
        if self.family: custom_properties["x_mitre_family"] = self.family

        return CourseOfAction(
            id = self.stix_id,
            name = self.name,
            description = self.format_description(),
            external_references = [ {
                "source_name": framework_id,
                "external_id": self.external_id
            } ],
            custom_properties = custom_properties
        )


def parse_controls(controlpath, control_ids={}, relationship_ids={}):
    """parse the NIST800-53 revision 4 controls and return a STIX bundle
    :param controlpath the filepath to the controls TSV file
    :param control_ids is a dict of format {control_name: stixID} which maps control names (e.g AC-1) to desired STIX IDs
    :param relationship_ids is a dict of format {relationship-source-id---relationship-target-id: relationship-id}, same general purpose as control_ids
    """

    print("reading framework config...", end="", flush=True)
    # load the mapping config
    with open(os.path.join("input", "config.json"), "r") as f:
        config = json.load(f)
        framework_id = config["framework_id"]
    print("done")

    tqdmformat = "{desc}: {percentage:3.0f}% |{bar}| {elapsed}<{remaining}{postfix}"

    controls_df = pd.read_csv(controlpath, sep="\t", keep_default_na=False, header=0)
    
    controls = []
    currentControl = None
    for index, row in tqdm(list(controls_df.iterrows()), desc="parsing NIST 800-53 revision 4", bar_format=tqdmformat):
        rowtype = row_type(row)
        
        if rowtype == "control": 
            controls.append(Control(row, control_ids))
            currentControl = controls[-1] # track current control to pass to enhancements
        if rowtype == "control_enhancement": 
            controls.append(Control(row, control_ids, parent=currentControl))
        if rowtype == "statement":
            controls[-1].add_statement(row)
        if rowtype == "substatement":
            controls[-1].add_substatement(row)
    
    # parse controls into stix
    stixcontrols = []
    for control in tqdm(controls, desc="creating controls", bar_format=tqdmformat):
        stixcontrols.append(control.toStix(framework_id))

    # parse control relationships into stix
    relationships = []
    for control in tqdm(list(filter(lambda c: control.parent_id or len(control.related) > 0, controls)), desc="creating control relationships", bar_format=tqdmformat):
        if control.parent_id: 
            # build subcontrol-of relationships
            target_id = control_ids[control.parent_id]
            source_id = control.stix_id
            joined_id = f"{source_id}---{target_id}"

            relationships.append(Relationship(
                id=relationship_ids[joined_id] if joined_id in relationship_ids else None,
                source_ref=source_id,
                target_ref=target_id,
                relationship_type="subcontrol-of"
            ))

        if len(control.related) > 0:
            # build related-to relationships
            for related_id in control.related:
                if related_id not in control_ids: continue # sometimes related doesn't refer to a control but rather an appendix section
                source_id = control.stix_id
                target_id = control_ids[related_id]
                joined_id = f"{source_id}---{target_id}"
                relationships.append(Relationship(
                    id=relationship_ids[joined_id] if joined_id in relationship_ids else None,
                    source_ref=source_id,
                    target_ref=target_id,
                    relationship_type="related-to"
                ))


    return Bundle(*itertools.chain(stixcontrols, relationships))

