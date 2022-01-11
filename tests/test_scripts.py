import os
import pathlib
import subprocess
import sys

import pytest

import list_mappings
import mappings_to_heatmaps
import parse_r4
import parse_r5
import substitute


ATTACK_VERSIONS = ["v8.2", "v9.0", "v10.1"]
R4 = "nist800_53_r4"
R5 = "nist800_53_r5"
NIST_REVS = [R4, R5]


@pytest.fixture()
def attack_domain():
    return "enterprise-attack"


@pytest.fixture()
def dir_location():
    cwd = os.getcwd()
    if "tests" in cwd:
        return os.path.dirname(cwd)
    else:
        return cwd


@pytest.mark.parametrize("attack_version", ATTACK_VERSIONS)
@pytest.mark.parametrize("rev", NIST_REVS)
def test_list_mappings(dir_location, attack_domain, attack_version, rev):
    """Tests list_mappings.py with both framework entries"""
    dashed_rev = rev.replace('_', '-')
    attack_version_filepath = attack_version.replace('.', '_')[1:]  # turn v10.1 into 10_1
    rx_controls = pathlib.Path(dir_location, "frameworks", f"attack_{attack_version_filepath}", rev,
                               "stix", f"{dashed_rev}-controls.json")
    rx_mappings = pathlib.Path(dir_location, "frameworks", f"attack_{attack_version_filepath}", rev,
                               "stix", f"{dashed_rev}-mappings.json")
    output_location = pathlib.Path(dir_location, "frameworks", f"attack_{attack_version_filepath}", rev,
                                   f"{dashed_rev}-mappings.xlsx")
    attack_location = pathlib.Path(dir_location, "data", "attack",
                                   f"enterprise-attack-{attack_version}.json")

    list_mappings.main(
        attack=str(attack_location),
        controls=str(rx_controls),
        mappings=str(rx_mappings),
        output=str(output_location)
    )


@pytest.mark.parametrize("attack_version", ATTACK_VERSIONS)
@pytest.mark.parametrize("rev", NIST_REVS)
def test_mappings_to_heatmaps(dir_location, attack_domain, attack_version, rev):
    """Tests mappings_to_heatmaps.py with both framework entries"""
    dashed_rev = rev.replace('_', '-')
    attack_version_filepath = attack_version.replace('.', '_')[1:]  # turn v10.1 into 10_1
    rx_controls = pathlib.Path(dir_location, "frameworks", f"attack_{attack_version_filepath}", rev,
                               "stix", f"{dashed_rev}-controls.json")
    rx_mappings = pathlib.Path(dir_location, "frameworks", f"attack_{attack_version_filepath}", rev,
                               "stix", f"{dashed_rev}-mappings.json")
    output_location = pathlib.Path(dir_location, "frameworks", f"attack_{attack_version_filepath}", rev,
                                   "layers")
    attack_location = pathlib.Path(dir_location, "data", "attack",
                                   f"enterprise-attack-{attack_version}.json")

    mappings_to_heatmaps.main(
        framework=rev,
        attack=str(attack_location),
        controls=str(rx_controls),
        mappings=str(rx_mappings),
        domain=attack_domain,
        version=attack_version,
        output=str(output_location),
        clear=True,
        build_dir=True
    )


@pytest.mark.parametrize("attack_version", ATTACK_VERSIONS)
@pytest.mark.parametrize("rev", NIST_REVS)
def test_substitute(dir_location, attack_domain, attack_version, rev):
    """Tests substitute.py with both frameworks"""
    dashed_rev = rev.replace('_', '-')
    attack_version_filepath = attack_version.replace('.', '_')[1:]  # turn v10.1 into 10_1
    rx_controls = pathlib.Path(dir_location, "frameworks", f"attack_{attack_version_filepath}", rev,
                               "stix", f"{dashed_rev}-controls.json")
    rx_mappings = pathlib.Path(dir_location, "frameworks", f"attack_{attack_version_filepath}", rev,
                               "stix", f"{dashed_rev}-mappings.json")
    output_location = pathlib.Path(dir_location, "frameworks", f"attack_{attack_version_filepath}", rev,
                                   "stix", f"{dashed_rev}-enterprise-attack.json")
    attack_location = pathlib.Path(dir_location, "data", "attack",
                                   f"enterprise-attack-{attack_version}.json")

    substitute.main(
        attack=str(attack_location),
        controls=str(rx_controls),
        mappings=str(rx_mappings),
        output=str(output_location),
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
    rx_input_controls = pathlib.Path(dir_location, "data", f"controls", f"{dashed_rev}-controls.tsv")
    rx_input_mappings = pathlib.Path(dir_location, "frameworks", f"attack_{attack_version_filepath}", rev,
                                     "input", f"{dashed_rev}-mappings.tsv")
    rx_output_controls = pathlib.Path(dir_location, "frameworks", f"attack_{attack_version_filepath}", rev,
                                      "stix", f"{dashed_rev}-controls.json")
    rx_output_mappings = pathlib.Path(dir_location, "frameworks", f"attack_{attack_version_filepath}", rev,
                                      "stix", f"{dashed_rev}-mappings.json")
    config_location = pathlib.Path(dir_location, "frameworks", f"attack_{attack_version_filepath}", rev,
                                   "input", "config.json")
    attack_location = pathlib.Path(dir_location, "data", "attack",
                                   f"enterprise-attack-{attack_version}.json")

    if rev == R4:
        parse = parse_r4
    elif rev == R5:
        parse = parse_r5
    else:
        parse = None

    parse.main(
        in_controls=str(rx_input_controls),
        in_mappings=str(rx_input_mappings),
        out_controls=str(rx_output_controls),
        out_mappings=str(rx_output_mappings),
        config_location=str(config_location),
        attack_location=str(attack_location),
    )
