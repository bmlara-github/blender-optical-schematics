# Paper setup reconstruction (schematic)

Scientific reference: https://doi.org/10.1103/6ftp-svh8 (provided by the author). This is a **later 3D reconstruction**. The paper did not use these Blender models. The article DOI is not the DOI of this library.

## One example, end to end

Follow the [existing user guide](../../docs/user-guide.pdf), steps 1–15. Every illustration uses this original example updated with the collimator, pinhole and adjustable iris and these same two reference images.

Open `source.blend` for the saved starting scene. `workflow.py` runs the fixed, coarse, refine and compact stages through the existing library helpers. `export.py` exports 86 mm paired SVGs with 0.5 mm borders. `expected/` contains the verified renders, all 15 camera candidates, camera JSON files, rankings and SVG pairs.

In Blender's Python Console, set `ROOT` to the repository and choose a new dated output folder, then run:

```python
import sys
from pathlib import Path
ROOT = Path('/absolute/path/to/blender-optical-schematics')
sys.path.insert(0, str(ROOT / 'examples/paper-setup'))
import workflow
OUT = ROOT / 'Figures/2026-11-10-Fig03'  # use today's date and a new number
workflow.run('fixed', OUT)
workflow.run('coarse', OUT)
workflow.run('refine', OUT)
workflow.run('compact', OUT)
workflow.finish('fixed', OUT)
workflow.finish('compact', OUT, version=4, source_version=3)
```

Outside Blender, from the repository root:

```sh
python scripts/rank_camera_views.py Figures/2026-11-10-Fig03/coarse
python scripts/rank_camera_views.py Figures/2026-11-10-Fig03/refine
python examples/paper-setup/export.py Figures/2026-11-10-Fig03 fixed --version 4
python examples/paper-setup/export.py Figures/2026-11-10-Fig03 compact --version 4
```

The compact stage demonstrates applying an alternative preset, not an automatic optimum. It shows the back of the SLM; retain the fixed view when visibility of its active face is required. The guide explains this tradeoff. The source uses library surface beam envelopes for visibility on white; hidden original volume envelopes remain in the scene. Neither is a diffraction calculation.

## Inputs

[layout.json](layout.json) is an authoring plan, not input to an included fixed scene-builder executable. It provides the component list, collection IDs, library files, assumed coordinates and beam routes. The agent must write its build script and verify collection axes and aperture alignment. The order is Laser, Collimator, P, L1P, L2P, SLM, L2, SF, L1, CCD. P is a pinhole (SO_Pinhole), imaged on the SLM by L1P/L2P. SF is the current adjustable iris (SO_Iris); it passes +1 and blocks the rejected orders.

The source figure was identified locally as manuscript Figure 6. The drawn labels put L2 nearest SLM and L1 nearest CCD; previous source notes report conflicting prose. Preserve the figure labels unless the user resolves the discrepancy. Focal lengths and physical separations were not supplied. No experimental aperture diameter is assigned by this example. Schematic scale/spacing is illustrative.

The two images in [reference-images/](reference-images/) are included for the default example: the hologram goes beside SLM and the recorded intensity beside CCD. Their existing rights are documented separately; they are not Blender simulation outputs. The full paper PDF is not included. Supply a lawful sketch for an actual comparison with the complete original drawing. Without it, report that no full-sketch visual check was performed. Both panels must remain visible in both camera views, with no cable-like connectors.

## Outputs

One dated figure folder with python/, blender/, json/, md/, txt/, source/, renders/, svg/ and FinalFigure/. Working filenames end in _vXX. See [figure workflow](../../docs/figure-workflow.md). SVG optics remain raster, with vector lettering in a separate layer. Gaussian envelopes are display geometry, not simulated diffraction. Mechanical fits are not certified.

After selecting the POV, follow [the finishing steps](../../docs/scene-finishing.md) to preserve the approved beams and position studio illumination relative to the camera. After visual approval, run `python scripts/finalize_figure.py Figures/2026-11-10-Fig03 --stage compact --version 4 --approved`.

Asset audit: local and published SO_Iris and SO_Pinhole geometry match; see `../../docs/asset-audit.json`. The saved scene now uses those assets plus SO_Collimator. `scene-validation.json` verifies both 5/10/5 BU relays, the open pinhole center, and iris rejection. Historical dated figure folders preserve earlier versions; this bundled source and expected/ are the current example.
