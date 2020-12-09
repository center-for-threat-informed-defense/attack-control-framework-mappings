import json
import os
import subprocess
import sys


def findFileWithSuffix(suffix, folder):
    """find a file with the given suffix in the folder"""
    for f in os.listdir(folder):
        if f.endswith(suffix): return f
    return None


def main():
    """rebuild all control frameworks from the input data"""
    for framework in ["nist800-53-r4", "nist800-53-r5"]:
        # move to the framework folder
        frameworkfolder = os.path.join("frameworks", framework)
        os.chdir(frameworkfolder)

        # read the framework config
        configpath = os.path.join("input", "config.json")
        if not os.path.exists(configpath):
            print("WARNING: framework has no config file, skipping")
            os.chdir(os.path.join("..", ".."))
            continue
        with open(configpath, "r") as f:
            config = json.load(f)

        # build the controls and mappings STIX
        subprocess.run([sys.executable, "parse.py"])
        os.chdir(os.path.join("..", ".."))

        # find the mapping and control files that were generated
        controlsFile = findFileWithSuffix("-controls.json", os.path.join(frameworkfolder, "stix"))
        mappingsFile = findFileWithSuffix("-mappings.json", os.path.join(frameworkfolder, "stix"))
        
        # run the utility scripts
        os.chdir("util")
        subprocess.run([
            sys.executable, "mappingsToHeatmaps.py",
            "-controls", os.path.join("..", frameworkfolder, "stix", controlsFile),
            "-mappings", os.path.join("..", frameworkfolder, "stix", mappingsFile),
            "-output", os.path.join("..", frameworkfolder, "layers"),
            "-domain", config["attack_domain"],
            "-version", config["attack_version"],
            "-framework", framework,
            "--clear",
            "--build-directory"
        ])
        subprocess.run([
            sys.executable, "substitute.py",
            "-controls", os.path.join("..", frameworkfolder, "stix", controlsFile),
            "-mappings", os.path.join("..", frameworkfolder, "stix", mappingsFile),
            "-output", os.path.join("..", frameworkfolder, "stix", f"{framework}-enterprise-attack.json"),
            "-domain", config["attack_domain"],
            "-version", config["attack_version"]
        ])
        subprocess.run([
            sys.executable, "listMappings.py",
            "-controls", os.path.join("..", frameworkfolder, "stix", controlsFile),
            "-mappings", os.path.join("..", frameworkfolder, "stix", mappingsFile),
            "-output", os.path.join("..", frameworkfolder, f"{framework}-mappings.xlsx"),
            "-domain", config["attack_domain"],
            "-version", config["attack_version"]
        ])
        # reset
        os.chdir("..")


if __name__ == "__main__":
    main()
