import json
import os
import pathlib
import subprocess
import sys

import pytest

import list_mappings
import mappings_to_heatmaps
import parse
import substitute

ATTACK_8_2 = "v8.2"
ATTACK_9_0 = "v9.0"
ATTACK_10_1 = "v10.1"
ATTACK_VERSIONS = [ATTACK_8_2, ATTACK_9_0, ATTACK_10_1]
R4 = "nist800_53_r4"
R5 = "nist800_53_r5"
NIST_REVS = [R4, R5]


def get_attack_data(data_location, attack_version):
    if attack_version not in ATTACK_VERSIONS:
        raise ValueError(f"Unknown ATT&CK version: {attack_version}")
    attack_data_location = pathlib.Path(data_location, "data", "attack", f"enterprise-attack-{attack_version}.json")
    with attack_data_location.open("r") as f:
        attack_data = json.load(f)["objects"]

    return attack_data


@pytest.fixture
def dir_location():
    cwd = os.getcwd()
    if "tests" in cwd:
        return os.path.dirname(cwd)
    else:
        return cwd


@pytest.mark.parametrize("attack_version", ATTACK_VERSIONS)
@pytest.mark.parametrize("rev", NIST_REVS)
def test_list_mappings(dir_location, attack_version, rev):
    """Tests list_mappings.py with both framework entries"""
    dashed_rev = rev.replace('_', '-')
    attack_version_filepath = attack_version.replace('.', '_')[1:]  # turn v10.1 into 10_1
    controls_location = pathlib.Path(dir_location, "frameworks", f"attack_{attack_version_filepath}", rev,
                                     "stix", f"{dashed_rev}-controls.json")
    with open(controls_location, "r") as f:
        controls = json.load(f)["objects"]
    mappings_location = pathlib.Path(dir_location, "frameworks", f"attack_{attack_version_filepath}", rev,
                                     "stix", f"{dashed_rev}-mappings.json")
    with open(mappings_location, "r") as f:
        mappings = json.load(f)["objects"]
    output_location = pathlib.Path(dir_location, "frameworks", f"attack_{attack_version_filepath}", rev,
                                   f"{dashed_rev}-mappings.xlsx")
    attack_data = get_attack_data(dir_location, attack_version)

    list_mappings.main(
        attack_data=attack_data,
        controls=controls,
        mappings=mappings,
        output=output_location
    )


@pytest.mark.parametrize("attack_version", ATTACK_VERSIONS)
@pytest.mark.parametrize("rev", NIST_REVS)
def test_mappings_to_heatmaps(dir_location, attack_version, rev):
    """Tests mappings_to_heatmaps.py with both framework entries"""
    dashed_rev = rev.replace('_', '-')
    attack_version_filepath = attack_version.replace('.', '_')[1:]  # turn v10.1 into 10_1
    controls_location = pathlib.Path(dir_location, "frameworks", f"attack_{attack_version_filepath}", rev,
                                     "stix", f"{dashed_rev}-controls.json")
    with open(controls_location, "r") as f:
        controls = json.load(f)["objects"]
    mappings_location = pathlib.Path(dir_location, "frameworks", f"attack_{attack_version_filepath}", rev,
                                     "stix", f"{dashed_rev}-mappings.json")
    with open(mappings_location, "r") as f:
        mappings = json.load(f)["objects"]
    output_location = pathlib.Path(dir_location, "frameworks", f"attack_{attack_version_filepath}", rev,
                                   "layers")
    attack_data = get_attack_data(dir_location, attack_version)

    mappings_to_heatmaps.main(
        framework=rev,
        attack_data=attack_data,
        controls=controls,
        mappings=mappings,
        domain="enterprise-attack",
        version=attack_version,
        output=output_location,
        clear=True,
        build_dir=True
    )


@pytest.mark.parametrize("attack_version", ATTACK_VERSIONS)
@pytest.mark.parametrize("rev", NIST_REVS)
def test_substitute(dir_location, attack_version, rev):
    """Tests substitute.py with both frameworks"""
    dashed_rev = rev.replace('_', '-')
    attack_version_filepath = attack_version.replace('.', '_')[1:]  # turn v10.1 into 10_1
    rx_controls = pathlib.Path(dir_location, "frameworks", f"attack_{attack_version_filepath}", rev,
                               "stix", f"{dashed_rev}-controls.json")
    with open(rx_controls, "r") as f:
        rx_controls = json.load(f)["objects"]
    rx_mappings = pathlib.Path(dir_location, "frameworks", f"attack_{attack_version_filepath}", rev,
                               "stix", f"{dashed_rev}-mappings.json")
    with open(rx_mappings, "r") as f:
        rx_mappings = json.load(f)["objects"]
    output_location = pathlib.Path(dir_location, "frameworks", f"attack_{attack_version_filepath}", rev,
                                   "stix", f"{dashed_rev}-enterprise-attack.json")
    attack_data = get_attack_data(dir_location, attack_version)

    substitute.main(
        attack_data=attack_data,
        controls=rx_controls,
        mappings=rx_mappings,
        output=output_location,
        allow_unmapped=True
    )


def test_make(dir_location):
    """Test the main make.py script"""
    script_location = f"{dir_location}/src/make.py"
    child_process = subprocess.Popen([
        sys.executable, script_location,
    ])
    child_process.wait(timeout=1080)
    assert child_process.returncode == 0


@pytest.mark.parametrize("attack_version", ATTACK_VERSIONS)
@pytest.mark.parametrize("rev", NIST_REVS)
def test_parse_framework(dir_location, attack_version, rev):
    """Tests parse_r4.py.bak.bak.bak with both frameworks"""
    dashed_rev = rev.replace('_', '-')
    attack_version_filepath = attack_version.replace('.', '_')[1:]  # turn v10.1 into 10_1
    dashed_attack_version = attack_version_filepath.replace('_', '-')
    rx_input_controls = pathlib.Path(dir_location, "data", "controls", f"{dashed_rev}-controls.tsv")
    rx_input_mappings = pathlib.Path(dir_location, "data", "mappings",
                                     f"attack-{dashed_attack_version}-to-{dashed_rev}-mappings.tsv")
    rx_output_controls = pathlib.Path(dir_location, "frameworks", f"attack_{attack_version_filepath}", rev,
                                      "stix", f"{dashed_rev}-controls.json")
    rx_output_mappings = pathlib.Path(dir_location, "frameworks", f"attack_{attack_version_filepath}", rev,
                                      "stix", f"{dashed_rev}-mappings.json")
    attack_data = get_attack_data(dir_location, attack_version)
    if rev == R4:
        framework_id = "NIST 800-53 Revision 4"
    elif rev == R5:
        framework_id = "NIST 800-53 Revision 5"
    else:
        raise ValueError(f"Unknown revision: {rev}")

    parse.main(
        in_controls=rx_input_controls,
        in_mappings=rx_input_mappings,
        out_controls=rx_output_controls,
        out_mappings=rx_output_mappings,
        framework_id=framework_id,
        attack_data=attack_data,
    )
