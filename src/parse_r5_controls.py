import itertools
import re
import uuid

from stix2.v20 import Bundle, CourseOfAction, Relationship
from tqdm import tqdm


id_formats = {
    "control": [                                                # CONTROL FORMATS:
        re.compile(r"^\w+-\d+\t")                                 # AC-1    [control data]
    ],
    "control_enhancement": [                                    # CONTROL ENHANCEMENT FORMATS:
        re.compile(r"^(\w+-\d+) ?\(\d+\)\t")                      # AC-1 (1) or AC-1(1) followed by control data
    ],
    "statement": [                                              # STATEMENT FORMATS:
        re.compile(r"^(\w+\.) (.*)"),                             # a.  [statement text]
        re.compile(r"^(\d+\.) (.*)"),                             # 1.  [statement text]
        re.compile(r"^(\(\w+\)) (.*)"),                           # (a) [statement text]
    ],
}


def row_type(row):
    """from a pandas series determine if it's a "control", "control_enhancement"
    or "statement" and return the type as a string"""
    # check all known formats
    for id_format_group in id_formats:
        # test against format
        for id_format in id_formats[id_format_group]:
            if id_format.match(row):
                return id_format_group
    return "freetext"  # all other formats are supplemental guidance for the current control


class Control:
    """helper class defining a Control"""
    def __init__(self, row, columns, control_ids):
        """constructor"""

        def get_column(column):
            """helper function to get the control data for the given column in the tsv"""
            try:
                return row.split("\t")[columns.index(column)].strip('"')
            except (KeyError, ValueError):
                return None  # column doesn't exist for row

        self.external_id = get_column("Control Identifier")
        # print("id:", self.external_id)
        self.name = get_column("Control (or Control Enhancement) Name")
        # print("name:", self.name)
        self.text = get_column("Control (or Control Enhancement)")
        # print("text:", self.text)
        self.discussion = get_column("Discussion")
        # print("discussion:", self.discussion)
        self.related = get_column("Related Controls").split(", ") if get_column("Related Controls") else []
        # print("related:", self.related)

        # try to manually set the STIX ID from the control_ids mapping, if not present it will randomly generate
        if control_ids and self.external_id in control_ids:
            self.stix_id = control_ids[self.external_id]
        else:
            self.stix_id = f"course-of-action--{uuid.uuid4()}"

        # update lookup so that subsequent objects can reference for relationships
        control_ids[self.external_id] = self.stix_id

        # if this is a control enhancement, set the parent ID
        self.is_enhancement = row_type(row) == "control_enhancement"
        # print("enhancement:", self.is_enhancement)
        self.parent_id = id_formats["control_enhancement"][0].search(row).groups()[0] if self.is_enhancement else None
        # print("parentID:", self.parent_id)

    def format_description(self):
        """format and return the control description (statements, etc) as a markdown string"""
        description = []
        if self.text:
            description.append(self.text)
        if self.discussion:
            description.append(self.discussion)
        return "\n\n".join(description)

    def to_stix(self, framework_id):
        """convert to a stix2 Course of Action"""
        return CourseOfAction(
            id=self.stix_id,
            name=self.name,
            description=self.format_description(),
            external_references=[
                {
                    "source_name": framework_id,
                    "external_id": self.external_id,
                }
            ]
        )


def parse_controls(control_path, control_ids, relationship_ids, framework_id):
    """parse the NIST800-53 revision 4 controls and return a STIX bundle
    :param control_path: the filepath to the controls TSV file
    :param control_ids: is a dict of format {control_name: stixID} which maps
                        control names (e.g AC-1) to desired STIX IDs
    :param relationship_ids: is a dict of format {relationship-source-id---relationship-target-id: relationship-id},
                        same general purpose as control_ids
    :param framework_id: the framework id - e.g., "NIST 800-53 Revision 4".
    """

    tqdmformat = "{desc}: {percentage:3.0f}% |{bar}| {elapsed}<{remaining}{postfix}"

    # controls_df = pd.read_csv(control_path, sep="\t", keep_default_na=False, header=0)
    with open(control_path, "r") as controlsfile:
        controls_data = controlsfile.read().split("\n")
    columns = controls_data[0].split("\t")
    controls_data = controls_data[1:]
    controls = []

    current_control = []
    for row in tqdm(controls_data, desc="parsing NIST 800-53 revision 5", bar_format=tqdmformat):
        row = row.strip('"')  # remove leading and trailing quotation marks
        returned_type = row_type(row)
        if returned_type == "control" or returned_type == "control_enhancement":
            if current_control:  # otherwise first row creates an empty control
                controls.append(Control("\n".join(current_control), columns, control_ids))  # finish previous control
            current_control = [row]  # start a new control
        else:
            current_control.append(row)  # append line to current control

    # finish last control
    controls.append(Control("\n".join(current_control), columns, control_ids))

    # parse controls into stix
    stix_controls = []
    for control in tqdm(controls, desc="creating controls", bar_format=tqdmformat):
        stix_controls.append(control.to_stix(framework_id))

    # parse control relationships into stix
    relationships = []
    for control in tqdm(list(filter(lambda c: control.parent_id or len(control.related) > 0, controls)),
                        desc="creating control relationships",
                        bar_format=tqdmformat):
        if control.parent_id:
            # build subcontrol-of relationships
            target_id = control_ids[control.parent_id]
            source_id = control.stix_id
            joined_id = f"{source_id}---{target_id}"
            rel_type = "subcontrol-of"
            subcontrols_refs = relationship_ids.get(rel_type, {})

            relationships.append(Relationship(
                id=subcontrols_refs[joined_id] if joined_id in subcontrols_refs else None,
                source_ref=source_id,
                target_ref=target_id,
                relationship_type=rel_type
            ))

        if len(control.related) > 0:
            # build related-to relationships
            for related_id in control.related:
                if related_id not in control_ids:
                    continue  # sometimes related doesn't refer to a control but rather an appendix section
                source_id = control.stix_id
                target_id = control_ids[related_id]
                joined_id = f"{source_id}---{target_id}"
                rel_type = "related-to"
                related_refs = relationship_ids.get(rel_type, {})

                relationships.append(Relationship(
                    id=related_refs[joined_id] if joined_id in related_refs else None,
                    source_ref=source_id,
                    target_ref=target_id,
                    relationship_type=rel_type
                ))

    return Bundle(*itertools.chain(stix_controls, relationships))
