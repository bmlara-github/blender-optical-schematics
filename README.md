# Blender Optical Schematics

![Library element catalogue](images/catalogue-cover.png)

Reusable Blender collections for optical illustrations, including 22 generic optical and beam assets.

**Authors:** B. M. Rodriguez-Lara. [Citation metadata](CITATION.cff).

## Use the library

1. Open Blender. These assets were prepared with Blender 5.2.3 LTS.
2. In Preferences → File Paths → Asset Libraries, add this repository's `library/` folder.
3. Open the Asset Browser and drag a collection into your scene as an instance. Alternatively use File → Append → a library file → Collection.
4. Use source asset scale, not the normalized display sizes shown on this cover. **1 Blender unit = 10 mm (illustrative scale).**

Read the [user guide](docs/user-guide.pdf), its [LaTeX source](docs/user-guide.tex), and the [asset index](docs/assets.json). The [catalogue SVG](images/catalogue-lettered.svg) has editable lettering; its optical rendering is embedded raster.

## Scope

These are visualization assets. Materials and generic optical shapes are illustrative. Beam envelopes are not diffraction simulations. Focal lengths belong in your scene metadata. Do not interpret the catalogue as a dimensioned optical design.

## License and citation

Original code uses MIT; original authored models and documentation use CC BY 4.0. See [LICENSE](LICENSE). This package includes two supplied SLM/CCD reference images for the example, with their existing rights documented separately; it does not include the manuscript PDF. See [material provenance](docs/provenance.md).

## How to cite

Rodriguez-Lara, B. M. (2026). Blender Optical Schematics (Version v0.1.1) [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.23993948

Cite the version you used. The [v0.1.1 DOI](https://doi.org/10.5281/zenodo.23993948) identifies a fixed release; the [all-versions DOI](https://doi.org/10.5281/zenodo.23993947) identifies the project across releases.

Download [BibTeX](docs/citations/schematics.bib), [RIS](docs/citations/schematics.ris), [CSL-JSON](docs/citations/schematics.csl.json), or [plain text](docs/citations/schematics.txt). See the user guide's “How to cite” section. The library citation is separate from the scientific paper.

## Build the documentation

From `docs/`, run `pdflatex user-guide.tex` twice. The PDF uses the included example preview; no private workspace files are needed.

## Generate the paper setup with the agent

Use the included [setup-to-Blender agent](agent/setup-to-blender/SKILL.md) and paste the [clean example request](examples/paper-setup/prompt.md). [Example instructions and inputs](examples/paper-setup/README.md) explain how to generate a later reconstruction of the paper setup. The agent writes and runs the scene builder; it does not require private project files. The SLM hologram and CCD intensity images are included with the example; additional sketches are optional user-provided inputs.

## First-time setup

Start with the [step-by-step guide](docs/user-guide.pdf). Keep the [agent folder](agent/README.md) beside library/. You can call the agent directly by asking Codex to read agent/setup-to-blender/SKILL.md and execute examples/paper-setup/prompt.md. No hidden-folder installation is needed for this direct call. The optional agent/install.py installs a named skill for this project only.

![Paper-setup reconstruction preview](images/paper-example.png)
