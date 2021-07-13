import os
import pathlib
import subprocess
import sys

import pytest


@pytest.fixture()
def attack_domain():
    return "enterprise-attack"


@pytest.fixture()
def attack_version():
    return "v8.2"


@pytest.fixture()
def dir_location():
    cwd = os.getcwd()
    if "tests" in cwd:
        return os.path.dirname(cwd)
    else:
        return cwd


@pytest.mark.parametrize("rev", ["nist800-53-r4", "nist800-53-r5"])
def test_list_mappings(dir_location, attack_domain, attack_version, rev):
    """Tests list_mappings.py with both framework entries"""
    rx_controls = pathlib.Path(dir_location, "frameworks", rev, "stix", f"{rev}-controls.json")
    rx_mappings = pathlib.Path(dir_location, "frameworks", rev, "stix", f"{rev}-mappings.json")
    output_location = pathlib.Path(dir_location, "frameworks", rev, f"{rev}-mappings.xlsx")
    script_location = f"{dir_location}/src/list_mappings.py"
    child_process = subprocess.Popen([
        sys.executable, script_location,
        "-controls", str(rx_controls),
        "-mappings", str(rx_mappings),
        "-domain", attack_domain,
        "-version", attack_version,
        "-output", str(output_location),
    ])
    child_process.wait(timeout=90)
    assert child_process.returncode == 0


@pytest.mark.parametrize("rev", ["nist800-53-r4", "nist800-53-r5"])
def test_mappings_to_heatmaps(dir_location, attack_domain, attack_version, rev):
    """Tests mappings_to_heatmaps.py with both framework entries"""
    rx_controls = pathlib.Path(dir_location, "frameworks", rev, "stix", f"{rev}-controls.json")
    rx_mappings = pathlib.Path(dir_location, "frameworks", rev, "stix", f"{rev}-mappings.json")
    output_location = pathlib.Path(dir_location, "frameworks", rev, "layers")
    script_location = f"{dir_location}/src/mappings_to_heatmaps.py"
    child_process = subprocess.Popen([
        sys.executable, script_location,
        "-framework", rev,
        "-controls", str(rx_controls),
        "-mappings", str(rx_mappings),
        "-domain", attack_domain,
        "-version", attack_version,
        "-output", str(output_location),
        "--clear",
        "--build-directory",
    ])
    child_process.wait(timeout=90)
    assert child_process.returncode == 0


@pytest.mark.parametrize("rev", ["nist800-53-r4", "nist800-53-r5"])
def test_substitute(dir_location, attack_domain, attack_version, rev):
    """Tests substitute.py with both frameworks"""
    rx_controls = pathlib.Path(dir_location, "frameworks", rev, "stix", f"{rev}-controls.json")
    rx_mappings = pathlib.Path(dir_location, "frameworks", rev, "stix", f"{rev}-mappings.json")
    output_location = pathlib.Path(dir_location, "frameworks", rev, "stix", f"{rev}-enterprise-attack.json")
    script_location = f"{dir_location}/src/substitute.py"
    child_process = subprocess.Popen([
        sys.executable, script_location,
        "-controls", str(rx_controls),
        "-mappings", str(rx_mappings),
        "-domain", attack_domain,
        "-version", attack_version,
        "-output", str(output_location),
        "--allow-unmapped",
    ])
    child_process.wait(timeout=90)
    assert child_process.returncode == 0


def test_make(dir_location):
    """Test the main make.py script"""
    script_location = f"{dir_location}/src/make.py"
    child_process = subprocess.Popen([
        sys.executable, script_location,
    ])
    child_process.wait(timeout=360)
    assert child_process.returncode == 0


@pytest.mark.parametrize("rev", ["nist800-53-r4", "nist800-53-r5"])
def test_parse_framework(dir_location, rev):
    """Tests parse.py with both frameworks"""
    rx_input_controls = pathlib.Path(dir_location, "frameworks", rev, "input", f"{rev}-controls.tsv")
    rx_input_mappings = pathlib.Path(dir_location, "frameworks", rev, "input", f"{rev}-mappings.tsv")
    rx_output_controls = pathlib.Path(dir_location, "frameworks", rev, "stix", f"{rev}-controls.json")
    rx_output_mappings = pathlib.Path(dir_location, "frameworks", rev, "stix", f"{rev}-mappings.json")
    config_location = pathlib.Path(dir_location, "frameworks", rev, "input", "config.json")
    script_location = f"{dir_location}/frameworks/{rev}/parse.py"
    child_process = subprocess.Popen([
        sys.executable, script_location,
        "-input-controls", str(rx_input_controls),
        "-input-mappings", str(rx_input_mappings),
        "-output-controls", str(rx_output_controls),
        "-output-mappings", str(rx_output_mappings),
        "-config-location", str(config_location),
    ])
    child_process.wait(timeout=90)
    assert child_process.returncode == 0
