# Minimal schematic translation slider

The current SO_Translation_Rail and SO_Translation_Carriage assets contain one mesh each: a rectangular rail and a thin camera platform. There is no pedestal, post, guide rod or detailed mounting hardware. Place the carriage top at the CCD housing bottom and the rail top at the carriage bottom. Optical-axis height remains unchanged.

For an image panel above the rail, call housing_corner(scene, camera, ccd, 'Camera housing', 'rear', 'left', vertical='top'), then place_panel with side='left'. This aligns the panel lower-right corner with the CCD upper-left housing corner. Retain the horizontal silhouette gap and check the panel against all projected component bounds. The default vertical='bottom' preserves other examples.

The active 20 mm relay figure is Figures/2026-11-10-Fig01 in the local schematic project. Versions share the original source/, renders/ and svg/ folders. Former FIg02 files carry _v01, the earlier FIg03 files _v02, and the current slider revision _v03 before each extension. The separate paper-example and experimental figures are not this revision sequence.
