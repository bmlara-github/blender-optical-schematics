# Adjustable iris diaphragm

Reuse the asset collection `SO_Iris` from `library/Bllas_Schematic_Optics_v01.blend`. It is the generic iris used for SF in the illuminated FIg01 setup. The current paper example uses SO_Pinhole for upstream P. The older circular pupil asset remains a distinct component.

The iris has a graphite annular housing, stylized blade seams, a satin-metal rim, a teal adjustment tab and an actual central opening. Its origin is the aperture center; local Y is the optical axis, and the detailed front faces -Y. One Blender unit represents 10 mm in the library convention. The source opening radius is 0.47 BU and the housing radius is 1.25 BU. These are illustrative dimensions, not a product specification.

Add the library folder to Blender Asset Libraries and select `SO_Iris`, or append that collection from the Blender file. Use collection instances so the source stays reusable. The FIg01 example uses a 1.3 scale instance at the shared focal plane of its return 4f relay. The pinhole is the input 4F object plane. Depicted iris hardware is adjustable, but the schematic asset has no mechanical animation rig. A different aperture setting is an instance/configuration variant, not a new library element.
