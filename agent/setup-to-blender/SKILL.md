---
name: setup-to-blender
description: Create schematic optical setup figures from component lists and sketches using this repository's Blender library, including its documented paper-setup reconstruction.
---

# Setup to Blender — schematic

Use the active project folder as the repository root. Confirm it contains library/, docs/assets.json and examples/paper-setup/. The distributed skill is in agent/setup-to-blender/; an installed copy may be in .agents/skills/setup-to-blender/. Do not infer the repository root solely from the skill location. Read root AGENTS.md and docs/assets.json. For the paper example read [paper-example.md](references/paper-example.md), then examples/paper-setup/README.md, prompt.md and layout.json. For new setups use [input-template.md](references/input-template.md).

Interpret the list and any user-supplied sketch before writing geometry. Identify sequence, branches, passes, source-image associations and ambiguous labels. If no sketch is available, use the explicit list and record that no visual source check was performed. Never claim to have read an inaccessible DOI or fabricate holograms/detector images. The paper example is a later reconstruction; its models were not used in the paper.

Create a new Figures/YYYY-MM-DD-FIgNN/ using the user's local date. Inspect existing folders to avoid overwriting. Write an explicit setup.json with source facts, assumed dimensions, collection mappings, orientations and beam routes. The example layout is an authoring reference, not an executable schema. Adapt it to the request without treating assumptions as measurements.

Write a self-contained build.py in that figure folder. Resolve the repository via the script path; append collections from the library paths in docs/assets.json using bpy.data.libraries.load, and instantiate collections. Do not execute or depend on the original private project builders. Use the schematic library convention of 1 BU = 10 mm and label spacing as illustrative. Inspect collection front/output axes rather than reusing experimental rotations blindly.

Reuse scripts/gaussian_beam.py for authored volume segments, with the chosen optical height and explicit widths. Rejected orders use the same red hue at lower brightness and end at SF; only the selected order continues. Keep generic lens shapes independent of focal length. Use existing collection instances for pupil and filter; align the beam to the actual opening. For a genuinely missing shape, add a reusable library asset with metadata before using it. Do not silently alter library apertures or claim physical compatibility.

Use orthographic perspective and plan cameras, broad studio lighting and clean renders with no baked text. For the example use 2000 x 1600, 40 Cycles samples and denoising. Build in a separate Blender process. Save the editable scene and repeatable source. Export matched SVGs at the requested width (86 mm default), proportional explicit millimeter dimensions, embedded clean PNG and a separate editable text layer; the unlettered SVG contains no text. Project label anchors with world_to_camera_view. Put only supplied reference images near their instrument.

Inspect both renders. Check asset identities, unit scale, beam continuity and endpoints, apertures, labels, source-image placement, SVG width and text separation, packed image dependencies, and unchanged libraries. Document checks and limitations in the figure README. Do not claim optical simulation, measured distances or mechanical certification. If rendering cannot run, deliver source and explain which outputs are unverified rather than inventing validation.
