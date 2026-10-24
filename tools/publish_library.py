"""Copy only validated, non-sensitive practice packs into the public static library."""
import argparse,hashlib,json,re,shutil,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def build(paths):
    packs=[];sections=[];pairs=[];seen=set();groups=set()
    for source in paths:
        raw=source.read_bytes();digest=hashlib.sha256(raw).hexdigest()
        with zipfile.ZipFile(source) as z:
            if len(z.namelist())!=len(set(z.namelist())):raise ValueError('Duplicate archive paths')
            manifest=z.read('manifest.json')
            if any(marker in manifest.lower() for marker in [b'http:',b'https:',b'/users/',b'api_key',b'api-key',b'client_secret',b'refresh_token']):raise ValueError('Do not publish private metadata')
            m=json.loads(manifest);pid=m['packId'];assert re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',pid)
            audio_dir=ROOT/'audio'/pid;audio_dir.mkdir(parents=True,exist_ok=True)
            for p in m['pairs']:
                assert p['id'] not in seen;seen.add(p['id'])
                audio=p['audio'];assert re.fullmatch(r'audio/pair-\d{3,4}\.mp3',audio)
                content=z.read(audio);assert hashlib.sha256(content).hexdigest()==p['sha256']
                name=Path(audio).name;dest=audio_dir/name;dest.write_bytes(content)
                pairs.append(dict(id=p['id'],packId=pid,section=p['section'],english=p['english'],roman=p['roman'],hindi=p['hindi'],englishEndMs=p['englishEndMs'],hindiStartMs=p['hindiStartMs'],durationMs=p['durationMs'],audio=f'audio/{pid}/{name}'))
            for l in m['lessons']:
                if not l['id'].startswith('section-'):continue
                group=int(l['id'].split('-')[1]);assert group not in groups;groups.add(group)
                sections.append(dict(id=group,packId=pid,title=l['title'],subtitle=l['subtitle'],pairIds=l['pairIds']))
        name=f'{pid}-v{m["contentVersion"]}-{digest[:12]}.zip';dest=ROOT/'packs'/name;dest.parent.mkdir(exist_ok=True);shutil.copyfile(source,dest)
        packs.append(dict(packId=pid,title=m['title'],contentVersion=m['contentVersion'],pairs=len(m['pairs']),sha256=digest,bytes=len(raw),path='packs/'+name))
    assert all(p['section'] in groups for p in pairs)
    (ROOT/'catalog.json').write_text(json.dumps(dict(schemaVersion=1,packs=packs),ensure_ascii=False,indent=2)+'\n')
    (ROOT/'library.json').write_text(json.dumps(dict(version=1,packs=[dict(id=p['packId'],title=p['title'],count=p['pairs']) for p in packs],sections=sections,pairs=pairs),ensure_ascii=False,separators=(',',':'))+'\n')
    (ROOT/'.nojekyll').touch()
    print(f'Prepared {len(packs)} packs, {len(sections)} sections and {len(pairs)} pairs. No credentials or private document links published.')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('packs',type=Path,nargs='+');args=ap.parse_args();build(args.packs)
