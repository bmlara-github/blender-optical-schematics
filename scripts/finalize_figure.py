"""Copy an approved version into FinalFigure; never infer approval from a POV selection."""
from pathlib import Path
import argparse,hashlib,json,shutil,xml.etree.ElementTree as ET

def finalize(folder,stage='compact',version=4,approved=False):
    if not approved:raise ValueError('Visual approval is required before finalization')
    root=Path(folder).resolve();tag=f'_v{version:02d}'
    files=[root/'blender'/f'{stage}{tag}.blend']+[root/'svg'/f'{stage}_{kind}{tag}.svg' for kind in ['lettered','unlettered']]
    for p in files:
        if not p.is_file():raise FileNotFoundError(p)
    dimensions=[]
    for p in files[1:]:
        tree=ET.parse(p).getroot();dimensions.append((tree.get('width'),tree.get('height'),tree.get('viewBox')))
    if dimensions[0]!=dimensions[1]:raise ValueError('SVG pair dimensions differ')
    dst=root/'FinalFigure';dst.mkdir(exist_ok=True)
    def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
    for p in files:
        q=dst/p.name
        if q.exists() and digest(p)!=digest(q):raise FileExistsError(f'Preserve approved file: {q}')
    records=[]
    for p in files:
        q=dst/p.name;shutil.copy2(p,q)
        assert digest(p)==digest(q)
        records.append({'file':q.relative_to(root).as_posix(),'sha256':digest(q)})
    (root/'json').mkdir(exist_ok=True)
    (root/'json'/f'{stage}-approval{tag}.json').write_text(json.dumps({'status':'approved final','version':version,'files':records},indent=2))
    return records

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('folder');p.add_argument('--stage',default='compact');p.add_argument('--version',type=int,default=4);p.add_argument('--approved',action='store_true')
    a=p.parse_args();print(json.dumps(finalize(a.folder,a.stage,a.version,a.approved),indent=2))
