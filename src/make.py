import json
import os
import subprocess
import sys

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


def find_file_with_suffix(suffix, folder):
    """find a file with the given suffix in the folder"""
    for f in os.listdir(folder):
        if f.endswith(suffix):
            return f
    raise ValueError(f"Could not locate file with suffix of {suffix} in {folder}")


def main():
    """rebuild all control frameworks from the input data"""

    for attack_version in [ATTACK_10_1, ]:  # [ATTACK_8_2, ATTACK_9_0, ATTACK_10_1]:
        for framework in [R4, R5]:
            # move to the framework folder
            versioned_folder = f"attack_{attack_version}"
            framework_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frameworks",
                                            versioned_folder, framework)

            # read the framework config
            config_path = os.path.join(framework_folder, "input", "config.json")
            if not os.path.exists(config_path):
                raise FileExistsError(f"Config file does not exist: {config_path}")
            with open(config_path, "r") as f:
                config = json.load(f)

            # build the controls and mappings STIX
            parse = parse_lookup[attack_version][framework]

            dashed_framework = framework.replace('_', '-')
            in_controls = os.path.join(framework_folder, "input", f"{dashed_framework}-controls.tsv")
            in_mappings = os.path.join(framework_folder, "input", f"{dashed_framework}-mappings.tsv")
            out_controls = os.path.join(framework_folder, "stix", f"{dashed_framework}-controls.json")
            out_mappings = os.path.join(framework_folder, "stix", f"{dashed_framework}-mappings.json")
            config_location = os.path.join(framework_folder, "input", "config.json")

            parse.main(in_controls=in_controls,
                       in_mappings=in_mappings,
                       out_controls=out_controls,
                       out_mappings=out_mappings,
                       config_location=config_location)

            # find the mapping and control files that were generated
            controls_file = find_file_with_suffix("-controls.json", os.path.join(framework_folder, "stix"))
            mappings_file = find_file_with_suffix("-mappings.json", os.path.join(framework_folder, "stix"))

            # run the utility scripts
            subprocess.run([   # TODO: Refactor
                sys.executable, "src/mappings_to_heatmaps.py",
                "-controls", os.path.join(framework_folder, "stix", controls_file),
                "-mappings", os.path.join(framework_folder, "stix", mappings_file),
                "-output", os.path.join(framework_folder, "layers"),
                "-domain", config["attack_domain"],
                "-version", config["attack_version"],
                "-framework", framework,
                "--clear",
                "--build-directory"
            ])
            subprocess.run([   # TODO: Refactor
                sys.executable, "src/substitute.py",
                "-controls", os.path.join(framework_folder, "stix", controls_file),
                "-mappings", os.path.join(framework_folder, "stix", mappings_file),
                "-output", os.path.join(framework_folder, "stix", f"{dashed_framework}-enterprise-attack.json"),
                "-domain", config["attack_domain"],
                "-version", config["attack_version"]
            ])
            subprocess.run([  # TODO: Refactor
                sys.executable, "src/list_mappings.py",
                "-controls", os.path.join(framework_folder, "stix", controls_file),
                "-mappings", os.path.join(framework_folder, "stix", mappings_file),
                "-output", os.path.join(framework_folder, f"{dashed_framework}-mappings.xlsx"),
                "-domain", config["attack_domain"],
                "-version", config["attack_version"]
            ])


if __name__ == "__main__":
    main()
