# Finish after selecting the POV

Use steps 11a–11b of [the user guide](user-guide.pdf), with the same original paper example. In Blender run `workflow.finish('compact', OUT)` after saving the selected camera. This writes separate outputs under `OUT/finished`; use that directory for the SVG exporter.

The reusable `scripts/finish_scene.py` restores the translucent beam material and shaded core, then places key, fill and rim lights in the selected camera frame. All area lights point at the setup target. Powers and world strength are keyword arguments. For manual position changes, edit camera-frame offsets in the helper. Reapply after camera changes, along with the panel placement callback.

Keep optical transforms fixed. Judge lens-edge reflections and housing contrast on white. Reduce fill/world illumination if flat; increase fill if dark faces disappear; reduce or move the rim if highlights hide apertures. `library/beam-appearance.json` records the beam style, and `library/beam_envelope.py` provides reusable envelope and core geometry. These are illustrative beam representations.
