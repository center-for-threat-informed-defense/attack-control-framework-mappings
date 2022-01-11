import os

import list_mappings
import mappings_to_heatmaps
import substitute

import parse_r4
import parse_r5

ATTACK_8_2 = "8_2"
ATTACK_9_0 = "9_0"
ATTACK_10_1 = "10_1"

R4 = "nist800_53_r4"
R5 = "nist800_53_r5"

parse_lookup = {
    ATTACK_8_2: {
        R4: parse_r4,
        R5: parse_r5,
    },
    ATTACK_9_0: {
        R4: parse_r4,
        R5: parse_r5,
    },
    ATTACK_10_1: {
        R4: parse_r4,
        R5: parse_r5,
    }
}

framework_id_lookup = {
    R4: "NIST 800-53 Revision 4",
    R5: "NIST 800-53 Revision 5"
}


def find_file_with_suffix(suffix, folder):
    """find a file with the given suffix in the folder"""
    for f in os.listdir(folder):
        if f.endswith(suffix):
            return f
    raise ValueError(f"Could not locate file with suffix of {suffix} in {folder}")


def main():
    """rebuild all control frameworks from the input data"""

    for attack_version in [ATTACK_8_2, ATTACK_9_0, ATTACK_10_1]:
        for framework in [R4, R5]:
            versioned_folder = f"attack_{attack_version}"
            framework_id = framework_id_lookup[framework]
            framework_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frameworks",
                                            versioned_folder, framework)
            attack_resources_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data",
                                                   "attack")

            # build the controls and mappings STIX
            parse = parse_lookup[attack_version][framework]

            # find local attack copy location
            attack_version_string = "v" + attack_version.replace("_", ".") + ".json"
            attack_file = find_file_with_suffix(
                f"-{attack_version_string}",
                attack_resources_folder
            )

            dashed_framework = framework.replace('_', '-')
            dashed_attack_version = attack_version.replace('_', '-')
            in_controls = os.path.join("data", "controls", f"{dashed_framework}-controls.tsv")
            in_mappings = os.path.join("data", "mappings",
                                       f"attack-{dashed_attack_version}-to-{dashed_framework}-mappings.tsv")
            out_controls = os.path.join(framework_folder, "stix", f"{dashed_framework}-controls.json")
            out_mappings = os.path.join(framework_folder, "stix", f"{dashed_framework}-mappings.json")
            attack_location = os.path.join(attack_resources_folder, attack_file)

            parse.main(in_controls=in_controls,
                       in_mappings=in_mappings,
                       out_controls=out_controls,
                       out_mappings=out_mappings,
                       framework_id=framework_id,
                       attack_location=attack_location)

            # find the mapping and control files that were generated
            controls_file = find_file_with_suffix("-controls.json", os.path.join(framework_folder, "stix"))
            mappings_file = find_file_with_suffix("-mappings.json", os.path.join(framework_folder, "stix"))

            controls = os.path.join(framework_folder, "stix", controls_file)
            mappings = os.path.join(framework_folder, "stix", mappings_file)
            out_layers = os.path.join(framework_folder, "layers")
            out_enterprise = os.path.join(framework_folder, "stix", f"{dashed_framework}-enterprise-attack.json")
            out_xlsx = os.path.join(framework_folder, f"{dashed_framework}-mappings.xlsx")

            # run the utility scripts
            mappings_to_heatmaps.main(
                framework=framework,
                attack=attack_location,
                controls=controls,
                mappings=mappings,
                domain="enterprise-attack",
                version=attack_version_string,
                output=out_layers,
                clear=True,
                build_dir=True
            )

            substitute.main(
                attack=attack_location,
                controls=controls,
                mappings=mappings,
                allow_unmapped=False,
                output=out_enterprise
            )

            list_mappings.main(
                attack=attack_location,
                controls=controls,
                mappings=mappings,
                output=out_xlsx
            )


if __name__ == "__main__":
    main()
