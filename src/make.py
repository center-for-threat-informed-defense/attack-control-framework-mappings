import json
import pathlib

import list_mappings
import mappings_to_heatmaps
import substitute

import parse

ATTACK_8_2 = "8_2"
ATTACK_9_0 = "9_0"
ATTACK_10_1 = "10_1"
ATTACK_12_1 = "12_1"

R4 = "nist800_53_r4"
R5 = "nist800_53_r5"

framework_id_lookup = {
    R4: "NIST 800-53 Revision 4",
    R5: "NIST 800-53 Revision 5"
}


def main():
    """rebuild all control frameworks from the input data"""

    for attack_version in [ATTACK_8_2, ATTACK_9_0, ATTACK_10_1, ATTACK_12_1]:
        for framework in [R4, R5]:
            # TODO: Lots of variable setting. Clean up
            versioned_folder = f"attack_{attack_version}"
            dashed_framework = framework.replace('_', '-')
            dashed_attack_version = attack_version.replace('_', '-')

            framework_id = framework_id_lookup[framework]
            project_folder = pathlib.Path(__file__).absolute().parent.parent
            framework_folder = project_folder / "frameworks" / versioned_folder / framework

            dist_folder = project_folder / "dist"
            dist_prefix = f"attack-{dashed_attack_version}-to-{dashed_framework}-"
            attack_version_string = "v" + attack_version.replace("_", ".")

            # Create the dist/ directory if not already present, if already present, do not raise an error.
            dist_folder.mkdir(exist_ok=True)

            attack_data = project_folder / "data" / "attack" / f"enterprise-attack-{attack_version_string}.json"
            with attack_data.open("r") as f:
                attack_data = json.load(f)["objects"]

            in_controls = project_folder / "data" / "controls" / f"{dashed_framework}-controls.tsv"
            in_mappings = (project_folder / "data" / "mappings" /
                           f"attack-{dashed_attack_version}-to-{dashed_framework}-mappings.tsv")
            out_controls = framework_folder / "stix" / f"{dashed_framework}-controls.json"
            out_mappings = framework_folder / "stix" / f"{dashed_framework}-mappings.json"

            parse.main(in_controls=in_controls,
                       in_mappings=in_mappings,
                       out_controls=out_controls,
                       out_mappings=out_mappings,
                       framework_id=framework_id,
                       attack_data=attack_data)

            controls = framework_folder / "stix" / f"{dashed_framework}-controls.json"
            with controls.open("r") as f:
                controls = json.load(f)["objects"]

            mappings = framework_folder / "stix" / f"{dashed_framework}-mappings.json"
            with mappings.open("r") as f:
                mappings = json.load(f)["objects"]

            out_enterprise = framework_folder / "stix" / f"{dashed_framework}-enterprise-attack.json"
            out_layers = framework_folder / "layers"
            out_xlsx = dist_folder / f"{dist_prefix}mappings.xlsx"

            # run the utility scripts
            mappings_to_heatmaps.main(
                framework=framework,
                attack_data=attack_data,
                controls=controls,
                mappings=mappings,
                domain="enterprise-attack",
                version=attack_version_string,
                output=out_layers,
                clear=True,
                build_dir=True
            )

            substitute.main(
                attack_data=attack_data,
                controls=controls,
                mappings=mappings,
                allow_unmapped=False,
                output=out_enterprise
            )

            list_mappings.main(
                attack_data=attack_data,
                controls=controls,
                mappings=mappings,
                output=out_xlsx
            )


if __name__ == "__main__":
    main()
