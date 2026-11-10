# Finish after selecting the POV

Follow steps 11a–12a of [the user guide](user-guide.pdf), using the same original paper example. In Blender run `workflow.finish('compact', OUT, version=4, source_version=3)` after saving the selected camera. This writes `blender/compact_v04.blend`, `renders/compact_v04.png`, and `json/compact-lighting_v04.json` inside the same figure folder. It preserves geometry, camera and approved beam materials and packs reference images.

The reusable `scripts/finish_scene.py` places key, fill and rim lights in the selected camera frame. All area lights point at the setup target. Powers and world strength are keyword arguments. Pass `restore_beams=False` for illumination-only changes; `True` intentionally restores the translucent envelope and shaded core. For position adjustments edit the camera-frame offsets in the helper. Reapply lights and panel placement after changing the camera.

Judge lens-edge reflections and housing contrast on white. Reduce fill/world illumination if flat; increase fill if dark faces disappear; reduce or move the rim if highlights hide apertures. Preserve approved beam appearance. These are illustrative beam representations, not diffraction simulations.

A selected POV is not a final figure. Export the matching SVG pair, inspect it, and obtain visual approval before using `scripts/finalize_figure.py --approved`. See [the complete workflow](figure-workflow.md). Keep earlier versions and close task-opened windows after saving.
