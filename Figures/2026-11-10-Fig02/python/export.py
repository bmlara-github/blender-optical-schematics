"""Export a worked-example PNG as paired SVGs. Run outside Blender with Pillow."""
import argparse,base64,html,json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[3]
LABELS={'fixed': [('Laser', 250, 865, 38), ('Collimator', 500, 1040, 32), ('P', 625, 775, 38), ('L1P', 875, 710, 38), ('L2P', 1340, 590, 38), ('SLM', 1530, 540, 38), ('L2', 1590, 815, 38), ('SF', 1500, 1040, 38), ('L1', 1290, 1175, 38), ('CCD', 1160, 1350, 38)], 'compact': [('Laser', 970, 515, 38), ('Collimator', 900, 790, 32), ('P', 1080, 805, 38), ('L1P', 1260, 720, 38), ('L2P', 1580, 875, 38), ('SLM', 1745, 875, 38), ('L2', 1455, 1160, 38), ('SF', 1195, 1130, 38), ('L1', 925, 1070, 38), ('CCD', 640, 1050, 38)]}

def export(output,stage,width_mm=86,border_mm=.5):
    out=Path(output)
    if not out.is_absolute():out=ROOT/out
    if stage not in LABELS:raise ValueError('Choose fixed or compact')
    if width_mm<=2*border_mm or border_mm<0:raise ValueError('Invalid width or border')
    im=Image.open(out/'renders'/(stage+'.png')).convert('RGBA');bbox=im.getchannel('A').getbbox()
    if bbox is None:raise ValueError('Empty render')
    x0,y0,x1,y1=bbox
    for t,x,y,size in LABELS[stage]:
        half=len(t)*size*.35
        x0=min(x0,int(x-half));x1=max(x1,int(x+half+1))
        y0=min(y0,int(y-size));y1=max(y1,int(y+size*.25+1))
    if x0==0 or y0==0 or x1==im.width or y1==im.height:raise ValueError('Clipped render: reframe before export')
    crop=im.crop(bbox);w,h=crop.size;k=(width_mm-2*border_mm)/w;H=2*border_mm+h*k
    png=out/'renders'/(stage+'-cropped.png');crop.save(png);enc=base64.b64encode(png.read_bytes()).decode();(out/'svg').mkdir(exist_ok=True)
    for labeled in [True,False]:
        text=''
        if labeled:
            for t,x,y,size in LABELS[stage]:
                text+=f'<text x="{border_mm+(x-x0)*k:.6f}" y="{border_mm+(y-y0)*k:.6f}" font-size="{size*k:.6f}">{html.escape(t)}</text>'
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" width="{width_mm}mm" height="{H:.9f}mm" viewBox="0 0 {width_mm} {H:.9f}"><desc>Embedded raster optical scene with editable vector lettering.</desc><rect width="{width_mm}" height="{H:.9f}" fill="white"/><g id="render" inkscape:groupmode="layer" inkscape:label="Raster render"><image x="{border_mm}" y="{border_mm}" width="{width_mm-2*border_mm}" height="{h*k:.9f}" href="data:image/png;base64,{enc}"/></g><g id="lettering" inkscape:groupmode="layer" inkscape:label="Editable lettering" font-family="Arial, sans-serif" text-anchor="middle" fill="#202c34">{text}</g></svg>'
        (out/'svg'/(stage+('_lettered.svg' if labeled else '_unlettered.svg'))).write_text(svg)
    report=dict(width_mm=width_mm,height_mm=H,borders_mm=[border_mm]*4,raster_render=True,editable_lettering=True)
    (out/(stage+'-export.json')).write_text(json.dumps(report,indent=2));return report

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('output');p.add_argument('stage',choices=['fixed','compact']);p.add_argument('--width-mm',type=float,default=86);p.add_argument('--border-mm',type=float,default=.5);a=p.parse_args();print(export(a.output,a.stage,a.width_mm,a.border_mm))
