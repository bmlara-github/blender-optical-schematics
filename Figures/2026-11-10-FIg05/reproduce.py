"""Run in Blender with a fresh output directory; see the user guide."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'examples/paper-setup'))
import workflow

def reproduce(output):
    for stage in ['fixed','compact']:
        workflow.run(stage,output)
        workflow.finish(stage,output)
