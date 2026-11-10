"""Measure transparent renders; output ranked metrics and a contact sheet. Requires Pillow."""
import argparse
import json
from pathlib import Path
from PIL import Image,ImageDraw


def measure(image, width_mm=86, border_mm=.5, alpha_threshold=20):
    if width_mm <= 2*border_mm or border_mm < 0:
        raise ValueError('Page width must exceed twice the nonnegative border')
    a=image.convert('RGBA').getchannel('A')
    bbox=a.getbbox()
    if bbox is None:
        return {'empty':True,'clipped':False}
    x0,y0,x1,y1=bbox;w,h=x1-x0,y1-y0
    occupied=sum(v>alpha_threshold for v in a.crop(bbox).getdata())/(w*h)
    height=2*border_mm+(width_mm-2*border_mm)*h/w
    return dict(empty=False,clipped=x0==0 or y0==0 or x1==image.width or y1==image.height,
                bounds_px=list(bbox),occupied_fraction=occupied,
                empty_fraction=1-occupied,height_mm=height,
                approximate_empty_area_mm2=(width_mm-2*border_mm)*(height-2*border_mm)*(1-occupied))


def rank(directory,width_mm=86,border_mm=.5):
    directory=Path(directory);rows=json.loads((directory/'candidates.json').read_text())
    for row in rows:
        with Image.open(directory/row['image']) as im: row.update(measure(im,width_mm,border_mm))
    rows.sort(key=lambda r:(r['empty'] or r['clipped'],r.get('approximate_empty_area_mm2',float('inf'))))
    (directory/'ranked.json').write_text(json.dumps(rows,indent=2)+'\n')
    sheet=Image.new('RGB',(1200,300*((len(rows)+2)//3)),'white');draw=ImageDraw.Draw(sheet)
    for i,r in enumerate(rows):
        x,y=(i%3)*400,(i//3)*300
        label=f"{r['id']}  az {r['azimuth_deg']} / el {r['elevation_deg']}"
        if not r['empty']:label+=f"  H {r['height_mm']:.1f}mm"
        if r['empty'] or r['clipped']:label+='  INVALID'
        draw.text((x+8,y+8),label,fill='black')
        if not r['empty']:
            with Image.open(directory/r['image']) as im:
                crop=im.convert('RGBA').crop(r['bounds_px']);bg=Image.new('RGBA',crop.size,'white');bg.alpha_composite(crop);bg.thumbnail((384,255));sheet.paste(bg.convert('RGB'),(x+8,y+35))
    sheet.save(directory/'comparison.png')
    return rows

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory');p.add_argument('--width-mm',type=float,default=86);p.add_argument('--border-mm',type=float,default=.5);a=p.parse_args();rank(a.directory,a.width_mm,a.border_mm)
