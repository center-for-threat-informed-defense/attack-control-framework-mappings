import pandas as pd
import os
from tqdm import tqdm
import re
from stix2.v20 import Bundle, Relationship, CourseOfAction
import itertools
import uuid
import json

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
        # print("id:", self.external_id)
        self.name = get_column("name")
        # print("name:", self.name)
        self.text = get_column("control_text")
        # print("text:", self.text)
        self.discussion = get_column("discussion")
        # print("discussion:", self.discussion)
        self.related = get_column("related").split(", ") if get_column("related") else []
        # print("related:", self.related)

        # try to manually set the STIX ID from the control_ids mapping, if not present it will randomly generate
        self.stix_id = control_ids[self.external_id] if control_ids and self.external_id in control_ids else f"course-of-action--{str(uuid.uuid4())}"
        control_ids[self.external_id] = self.stix_id # update lookup so that subsequent objects can reference for relationships

        # if this is a control enhancement, set the parent ID
        self.is_enhancement = row_type(row) == "control_enhancement"
        # print("enhancement:", self.is_enhancement)
        self.parent_id = id_formats["control_enhancement"][0].search(row).groups()[0] if self.is_enhancement else None
        # print("parentID:", self.parent_id)


    def format_description(self):
        """format and return the control description (statements, etc) as a markdown string"""
        return "\n\n".join([self.text, self.discussion])

    def toStix(self, framework_id):
        """convert to a stix2 Course of Action"""
        return CourseOfAction(
            id = self.stix_id,
            name = self.name,
            description = self.format_description(),
            external_references = [ {
                "source_name": framework_id,
                "external_id": self.external_id
            } ]
        )


def parse_controls(controlpath, control_ids={}, relationship_ids={}):
    """parse the NIST800-53 revision 4 controls and return a STIX bundle
    :param controlpath the filepath to the controls TSV file
    :param control_ids is a dict of format {control_name: stixID} which maps control names (e.g AC-1) to desired STIX IDs
    :param relationship_ids is a dict of format {relationship-source-id---relationship-target-id: relationship-id}, same general purpose as control_ids
    """

    print("reading framework config...", end="", flush=True)
    # load the mapping config
    with open(os.path.join("data", "config.json"), "r") as f:
        config = json.load(f)
        framework_id = config["framework_id"]
    print("done")

    tqdmformat = "{desc}: {percentage:3.0f}% |{bar}| {elapsed}<{remaining}{postfix}"

    # controls_df = pd.read_csv(controlpath, sep="\t", keep_default_na=False, header=0)
    with open(controlpath, "r") as controlsfile:
        controls_data = controlsfile.read().split("\n")
    columns = controls_data[0].split("\t")
    controls_data = controls_data[1:]
    controls = []

    currentControl = []
    for row in tqdm(controls_data, desc="parsing NIST 800-53 revision 5", bar_format=tqdmformat):
        row = row.strip('"') # remove leading and trailing quotation marks
        rowtype = row_type(row)
        if rowtype == "control" or rowtype == "control_enhancement":
            if currentControl: # otherwise first row creates an empty control
                controls.append(Control("\n".join(currentControl), columns, control_ids)) # finish previous control
            currentControl = [row] # start a new control
        else:
            currentControl.append(row) # append line to current control
        
    # finish last control
    controls.append(Control("\n".join(currentControl), columns, control_ids))

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

