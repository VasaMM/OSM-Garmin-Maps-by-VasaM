"""Initialize runtime data without installing anything in the host checkout."""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path('/workspace')
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))
output = Path(os.environ.get('OUTPUT_DIR', 'output'))
output.mkdir(parents=True, exist_ok=True)
os.environ['HOME'] = str((output / 'cache/home').resolve())
Path(os.environ['HOME']).mkdir(parents=True, exist_ok=True)
os.environ['MPLCONFIGDIR'] = str((output / 'cache/matplotlib').resolve())

# Keep the existing generator's relative-path expectations (including osmconvert).
config = {
    'img': str(output / 'maps') + '/',
    'pbf': str(output / 'cache/pbf') + '/',
    'polygons': str(output / 'polygons') + '/',
    'hgt': str(output / 'cache/hgt') + '/',
    'temp': str(output / 'temp') + '/',
    'sea': str(output / 'cache/sea') + '/',
    'bounds': str(output / 'cache/bounds') + '/',
}
for directory in config.values():
    Path(directory).mkdir(parents=True, exist_ok=True)
versions = json.loads(Path('versions.info').read_text())
config.update(versions)
for tool, version in versions.items():
    dest = Path(f'{tool}-r{version}')
    if not dest.exists():
        dest.symlink_to(f'/opt/vasam-tools/{dest.name}', target_is_directory=True)
Path('osmconvert').mkdir(exist_ok=True)
converter = Path('osmconvert/osmconvert64')
if not converter.exists():
    converter.symlink_to('/usr/bin/osmconvert')
Path('userAreas').mkdir(exist_ok=True)
areas = Path('userAreas/myAreas.py')
if not areas.exists():
    areas.write_text('USER_AREAS = {}\n')
Path('gmapmaker.config').write_text(json.dumps(config, indent=2)+'\n')

if sys.argv[1:] == ['--check']:
    import geojson, osmium, pyclipper, pyhgtmap
    subprocess.run(['java', '-version'], check=True)
    subprocess.run(['pyhgtmap', '--version'], check=True)
    for tool,version in versions.items():
        subprocess.run(['java','-jar',f'{tool}-r{version}/{tool}.jar','--version'],check=True)
    print('Container dependencies and host-mounted output initialized successfully.')
    sys.exit(0)

# Help/version should never require multi-gigabyte data downloads.
if any(arg in ('--help', '-h', '--version') for arg in sys.argv[1:]):
    os.execv(sys.executable, [sys.executable, 'gmapmaker.py', *sys.argv[1:]])

# Read worldwide ZIPs directly; retain and resume downloads on the host mount.
from docker.fetch_inputs import fetch_all
inputs = []
for kind in ('sea', 'bounds'):
    archive = Path(config[kind]) / f'{kind}-latest.zip'
    url = os.environ.get(f'{kind.upper()}_URL', f'https://www.thkukuk.de/osm/data/{kind}-latest.zip')
    inputs.append((url, archive))
    config[kind] = str(archive)
fetch_all(inputs)
Path('gmapmaker.config').write_text(json.dumps(config, indent=2)+'\n')
os.execv(sys.executable, [sys.executable, 'gmapmaker.py', *sys.argv[1:]])
