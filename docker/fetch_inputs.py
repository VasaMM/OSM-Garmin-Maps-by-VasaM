"""Resumable bounded-parallel public input downloads; Python standard library only."""
from concurrent.futures import ThreadPoolExecutor
from itertools import zip_longest
from pathlib import Path
import json
import shutil
import urllib.request

CHUNK = 64 * 1024 * 1024

def prepare(url, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return None, []
    with urllib.request.urlopen(urllib.request.Request(url, method='HEAD'), timeout=60) as r:
        total = int(r.headers['Content-Length'])
        tag = r.headers.get('ETag')
    parts = path.with_name(path.name + '.parts')
    parts.mkdir(exist_ok=True)
    # A new remote revision must never reuse chunks from the old revision.
    identity = {'url': url, 'size': total, 'etag': tag}
    metadata = parts / 'source.json'
    if metadata.exists() and json.loads(metadata.read_text()) != identity:
        shutil.rmtree(parts)
        parts.mkdir()
    metadata.write_text(json.dumps(identity))
    jobs = [(url,path,parts,index,total,tag) for index in range((total+CHUNK-1)//CHUNK)]
    return (path,parts,total), jobs

def transfer(job):
    url,path,parts,index,total,tag = job
    segment = parts / str(index)
    end = min(total,(index+1)*CHUNK)-1
    expected = end-index*CHUNK+1
    for attempt in range(3):
        size = segment.stat().st_size if segment.exists() else 0
        if size == expected: return
        start = index*CHUNK+size
        try:
            request = urllib.request.Request(url,headers={'Range': f'bytes={start}-{end}'})
            with urllib.request.urlopen(request,timeout=90) as r:
                if r.status != 206 or r.headers.get('Content-Range') != f'bytes {start}-{end}/{total}':
                    raise RuntimeError('Server did not honor the requested byte range')
                if tag and r.headers.get('ETag') != tag:
                    raise RuntimeError('Remote input changed during download; retry with a fresh cache')
                with segment.open('ab') as out:
                    while data := r.read(1024*1024): out.write(data)
            if segment.stat().st_size != expected: raise IOError('Truncated segment')
            print(path.name, 'completed chunk',index+1,'of',(total+CHUNK-1)//CHUNK,flush=True)
            return
        except Exception:
            if attempt == 2: raise

def fetch_all(items):
    plans,jobs=[],[]
    for url,path in items:
        plan,group=prepare(url,path)
        if plan: plans.append(plan)
        jobs.append(group)
    ordered=[job for row in zip_longest(*jobs) for job in row if job is not None]
    with ThreadPoolExecutor(max_workers=6) as pool: list(pool.map(transfer,ordered))
    for path,parts,total in plans:
        partial=path.with_suffix(path.suffix+'.part')
        with partial.open('wb') as out:
            for i in range((total+CHUNK-1)//CHUNK):
                with (parts/str(i)).open('rb') as source: shutil.copyfileobj(source,out,1024*1024)
        if partial.stat().st_size != total: raise IOError('Wrong assembled size')
        partial.replace(path)
        shutil.rmtree(parts)
        print('Complete',path,total,flush=True)

if __name__ == '__main__':
    root=Path('/workspace/output/cache')
    fetch_all([
        ('https://www.thkukuk.de/osm/data/bounds-latest.zip',root/'bounds/bounds-latest.zip'),
        ('https://www.thkukuk.de/osm/data/sea-latest.zip',root/'sea/sea-latest.zip'),
        ('https://download.geofabrik.de/europe/czech-republic-latest.osm.pbf',root/'pbf/CZ.osm.pbf'),
    ])
