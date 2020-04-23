import sys
sys.path.append("../..")
from common.classes import Control, Mapping
from common import exporters

def parse_controls():
    print("parsing controls", Control())
    return {}
    
def parse_mappings(controls):
    print("parsing mappings", Mapping())
    return {}

if __name__ == "__main__":
    controls = parse_controls()
    mappings = parse_mappings(controls)
    exporters.mappingsToLayer()