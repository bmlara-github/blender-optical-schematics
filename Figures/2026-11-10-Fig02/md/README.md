# Current original-example revision

Updates the existing paper example with the current SO_Iris at SF, SO_Pinhole at P, and SO_Collimator before P. Both relays use 5/10/5 schematic BU spans. The input relay images P onto the SLM active plane with magnification -1. No measured focal length is inferred.

scene-validation.json records aperture ray checks and both 4F conjugate checks. source.blend in examples/paper-setup is the current starting scene. Run workflow.run for fixed/coarse/refine/compact then workflow.finish for fixed/compact. Finished results are in finished/; original historical revisions remain untouched. All SVGs are 86 mm wide with .5 mm borders, embedded raster optics and separately editable text.


## File organization

Use `python/` for scripts, `blender/` for scenes and Blender backups, `json/` for structured settings and validation, `md/` for notes, and `txt/` for logs. Keep images in the existing `source/`, `renders/`, and `svg/` folders. Preserve `_vXX` filenames. After selecting a scene, copy its final Blender scene and paired SVG exports into `FinalFigure/`; working versions remain in their type folders.
