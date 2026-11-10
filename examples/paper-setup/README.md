# Paper setup reconstruction (schematic)

Scientific reference: https://doi.org/10.1103/6ftp-svh8 (provided by the author). This is a **later 3D reconstruction**. The paper did not use these Blender models. The article DOI is not the DOI of this library.

## One example, end to end

Follow the [existing user guide](../../docs/user-guide.pdf), steps 1–15. Every illustration uses this original nine-component setup and these same two reference images.

Open `source.blend` for the saved starting scene. `workflow.py` runs the fixed, coarse, refine and compact stages through the existing library helpers. `export.py` exports 86 mm paired SVGs with 0.5 mm borders. `expected/` contains the verified renders, all 15 camera candidates, camera JSON files, rankings and SVG pairs.

In Blender's Python Console, set `ROOT` to the repository and choose a new dated output folder, then run:

```python
import sys
from pathlib import Path
ROOT = Path('/absolute/path/to/blender-optical-schematics')
sys.path.insert(0, str(ROOT / 'examples/paper-setup'))
import workflow
OUT = ROOT / 'Figures/2026-11-10-FIg01'  # use today's date and a new number
workflow.run('fixed', OUT)
workflow.run('coarse', OUT)
workflow.run('refine', OUT)
workflow.run('compact', OUT)
```

Outside Blender, from the repository root:

```sh
python scripts/rank_camera_views.py Figures/2026-11-10-FIg01/coarse
python scripts/rank_camera_views.py Figures/2026-11-10-FIg01/refine
python examples/paper-setup/export.py Figures/2026-11-10-FIg01 fixed
python examples/paper-setup/export.py Figures/2026-11-10-FIg01 compact
```

The compact stage demonstrates applying an alternative preset, not an automatic optimum. It shows the back of the SLM; retain the fixed view when visibility of its active face is required. The guide explains this tradeoff. The source uses library surface beam envelopes for visibility on white; hidden original volume envelopes remain in the scene. Neither is a diffraction calculation.

## Inputs

[layout.json](layout.json) is an authoring plan, not input to an included fixed scene-builder executable. It provides the component list, collection IDs, library files, assumed coordinates and beam routes. The agent must write its build script and verify collection axes and aperture alignment. The order is Laser, P, L1P, L2P, SLM, L2, SF, L1, CCD. P is a circular pupil. SF selects +1; other orders terminate at its mask.

The source figure was identified locally as manuscript Figure 6. The drawn labels put L2 nearest SLM and L1 nearest CCD; previous source notes report conflicting prose. Preserve the figure labels unless the user resolves the discrepancy. Focal lengths and physical separations were not supplied. The experimental 4 mm pupil, 1 mm filter and 120 mm optical height are authored assumptions. Schematic scale/spacing is illustrative.

The two images in [reference-images/](reference-images/) are included for the default example: the hologram goes beside SLM and the recorded intensity beside CCD. Their existing rights are documented separately; they are not Blender simulation outputs. The full paper PDF is not included. Supply a lawful sketch for an actual comparison with the complete original drawing. Without it, report that no full-sketch visual check was performed. Both panels must remain visible in both camera views, with no cable-like connectors.

## Outputs

A new dated figure folder containing build.py, setup.json, the Blender scene, two clean renders, paired SVGs with and without editable lettering, and a README/report. SVG optics remain raster, with vector lettering in a separate layer. Gaussian envelopes are display geometry, not simulated diffraction. Mechanical fits are not certified.
