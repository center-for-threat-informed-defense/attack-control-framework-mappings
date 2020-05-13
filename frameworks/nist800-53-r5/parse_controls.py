import pandas as pd
import os
from tqdm import tqdm
import re
import stix2
import itertools
import uuid

id_formats = {
    "control": [                                                # CONTROL FORMATS:
        re.compile("^\w+-\d+\t")                                 # AC-1    [control data]
    ],
    "control_enhancement": [                                    # CONTROL ENHANCEMENT FORMATS:
        re.compile("^(\w+-\d+) ?\(\d+\)\t")                      # AC-1 (1) or AC-1(1) followed by control data
    ],
    "statement": [                                              # STATEMENT FORMATS:
        re.compile("^(\w+\.) (.*)"),                                 # a.  [statement text]
        re.compile("^(\d+\.) (.*)"),                                 # 1.  [statement text]
        re.compile("^(\(\w+\)) (.*)"),                               # (a) [statement text]
    ],
}

def row_type(row):
    """from a pandas series determine if it's a "control", "control_enhancement" or "statement" and return the type as a string"""
    # check all known formats
    for id_format_group in id_formats:
        # test against format
        for id_format in id_formats[id_format_group]:
            if id_format.match(row):
                return id_format_group
    return "freetext" # all other formats are supplemental guidance for the current control




class Statement:
    """helper class defining a statement or substatement"""
    def __init__(self, row):
        """constructor"""
        for id_format in id_formats["statement"]:
            if id_format.match(row):
                matches = id_format.search(row)
                self.external_id = matches.groups()[0]
                self.description = matches.groups()[1]
                break

        self.substatements = []
    
    def add_substatement(self, row):
        """add a substatement to this statement"""
        self.substatements.append(Statement(row))

    def format_statement(self):
        """transform statement into markdown string"""
        formatted = f"* **{self.external_id}** {self.description}"
        # recursively add substatements
        for substatement in self.substatements:
            formatted += f"\n    {substatement.format_statement()}"
        
        return formatted

class Control:
    """helper class defining a Control"""
    def __init__(self, row, columns, control_ids):
        """constructor"""

        def get_column(column):
            """helper function to get the control data for the given column in the tsv"""
            try:
                return row.split("\t")[columns.index(column)].strip('"')
            except:
                return None # column doesn't exist for row 

        self.external_id = get_column("identifier")
        self.name = get_column("name")

        self.related = get_column("related").split(", ") if get_column("related") else []

        self.statements = []
        for fieldname in ["control_text", "discussion"]:
            self.add_statement(get_column(fieldname))

        # try to manually set the STIX ID from the control_ids mapping, if not present it will randomly generate
        self.stix_id = control_ids[self.external_id] if control_ids and self.external_id in control_ids else f"course-of-action--{str(uuid.uuid4())}"
        control_ids[self.external_id] = self.stix_id # update lookup so that subsequent objects can reference for relationships
        
        # if this is a control enhancement, set the parent ID
        self.is_enhancement = row_type(row) == "control_enhancement"
        self.parent_id = id_formats["control_enhancement"][0].search(row).groups()[0] if self.is_enhancement else None

    def add_statement(self, row):
        """add a statement to this control"""
        
        # don't add None statements
        if not row: return

        # sometimes there are multiple statements in a row
        if "\t" in row:
            for subrow in row.split("\t"):
                self.add_statement(subrow.strip('"'))

        # base case, single statement in row
        else:
            # check if it's a statement or a freetext
            if row_type(row) == "statement":
                self.statements.append(Statement(row))
            elif row_type(row) == "freetext":
                self.statements.append(row)
                

    def format_description(self):
        """format and return the control description (statements, etc) as a markdown string"""
        paragraphs = []
        for statement in self.statements:
            text = statement.format_statement() if isinstance(statement, Statement) else statement
            paragraphs.append(text)

        return "\n\n".join(paragraphs)

    def toStix(self):
        """convert to a stix2 Course of Action"""
        return stix2.CourseOfAction(
            id = self.stix_id,
            name = self.name,
            description = self.format_description(),
            external_references = [ {
                "source_name": "NIST 800-53 Revision 5",
                "external_id": self.external_id
            } ]
        )


def parse_controls(controlpath, control_ids={}, relationship_ids={}):
    """parse the NIST800-53 revision 4 controls and return a STIX bundle
    :param controlpath the filepath to the controls TSV file
    :param control_ids is a dict of format {control_name: stixID} which maps control names (e.g AC-1) to desired STIX IDs
    :param relationship_ids is a dict of format {relationship-source-id---relationship-target-id: relationship-id}, same general purpose as control_ids
    """

    tqdmformat = "{desc}: {percentage:3.0f}% |{bar}| {elapsed}<{remaining}{postfix}"

    # controls_df = pd.read_csv(controlpath, sep="\t", keep_default_na=False, header=0)
    with open(controlpath, "r") as controlsfile:
        controls_data = controlsfile.readlines()
    columns = controls_data[0].split("\t")
    controls_data = controls_data[1:]
    controls = []

    for row in tqdm(controls_data, desc="parsing NIST 800-53", bar_format=tqdmformat):
        row = row.strip('"') # remove leading and trailing quotation marks
        rowtype = row_type(row)
        if rowtype == "control" or rowtype == "control_enhancement":
            controls.append(Control(row, columns, control_ids))
        elif rowtype == "statement":
            controls[-1].add_statement(row)
        elif rowtype == "freetext":
            controls[-1].add_statement(row)
    
    # parse controls into stix
    stixcontrols = []
    for control in tqdm(controls, desc="creating controls", bar_format=tqdmformat):
        stixcontrols.append(control.toStix())

    # parse control relationships into stix
    relationships = []
    for control in tqdm(list(filter(lambda c: control.parent_id or len(control.related) > 0, controls)), desc="creating control relationships", bar_format=tqdmformat):
        if control.parent_id: 
            # build subcontrol-of relationships
            target_id = control_ids[control.parent_id]
            source_id = control.stix_id
            joined_id = f"{source_id}---{target_id}"

            relationships.append(stix2.Relationship(
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
                relationships.append(stix2.Relationship(
                    id=relationship_ids[joined_id] if joined_id in relationship_ids else None,
                    source_ref=source_id,
                    target_ref=target_id,
                    relationship_type="related-to"
                ))


    return stix2.Bundle(*itertools.chain(stixcontrols, relationships), spec_version="2.0")

