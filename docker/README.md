# Docker build on macOS / Linux

The generator stays in this checkout. Python, Java, contour generation, osmconvert,
mkgmap and splitter run inside a locally built Linux image. No Homebrew or host pip
installation is needed. Docker Desktop must already be running.

```sh
docker build -t vasam-generator:local .
./docker/run.sh --check
./docker/run.sh                         # full Czech map, Unicode, contours and DEM
```

The default command is equivalent to:

```sh
./docker/run.sh --area CZ --code-page unicode --en --logging
```

Outputs and downloads persist in the host checkout:

- `output/maps/CZ_VasaM.img`: device map.
- `output/maps/CZ_VasaM.zip`: BaseCamp/MapSource files.
- `output/maps/CZ_VasaM.info`: source timestamp and output hashes.
- `output/cache/`: reusable OSM, elevation, boundary and sea inputs.
- `output/polygons/`, `output/temp/`: region definitions and intermediates.

Do not run two generators in the same checkout at once; they share temporary files.
The wrapper names the container `vasam-cz`. Inspect progress using
`docker logs -f vasam-cz` from another terminal. Ctrl-C stops a foreground run;
cached completed inputs survive for the next run. Boundary/sea downloads also resume
partial byte ranges and discard cached chunks if the remote revision changes.
Completed boundary/sea ZIPs are reused until you remove them to refresh the data.

The container uses your host UID/GID for files on the bind mount. It is limited to
7 GiB and 4 CPUs by default, with a 5 GiB Java heap and two compiler workers:

```sh
DOCKER_MEMORY=7g JAVA_MEM=-Xmx5g MAX_JOBS=2 ./docker/run.sh
```

Docker Desktop needs enough memory assigned to accommodate the container limit.
Allow at least 20 GiB of free host disk space for a full country build, including
the image, world inputs, cached elevation, intermediate tiles and output archives. The world boundary
and sea ZIPs are read directly instead of being extracted into another copy.
`docker/entrypoint.py` initializes the ignored runtime configuration and links tools
from the image; custom `userAreas/myAreas.py` is preserved if already present.

This setup follows the mounted-output approach proposed in
[VasaM issue #27](https://github.com/VasaMM/OSM-Garmin-Maps-by-VasaM/issues/27) and
[JanC's unfinished Docker branch](https://github.com/JanC/OSM-Garmin-Maps-by-VasaM/tree/docker).
It uses the current upstream generator and pyhgtmap rather than importing the fork's
older map styles or downloading an x86-only osmconvert binary. Debian's osmctools
supplies an architecture-native converter, so Apple Silicon needs no emulation.

For a first Czech build, optionally prefetch all large inputs in parallel:

```sh
docker run --rm --init --user "$(id -u):$(id -g)" \
  -v "$PWD:/workspace" --entrypoint python vasam-generator:local \
  docker/fetch_inputs.py
./docker/run.sh --area CZ --code-page unicode --download skip --en --logging
```

Use `--download skip` only when the intended OSM input is already cached. The
normal command checks its age and refreshes it when necessary. Sea/boundary URLs
can be overridden with `SEA_URL` and `BOUNDS_URL` on the wrapper command.

To check the download-resume behavior without contacting external providers:

```sh
docker run --rm -v "$PWD:/workspace" --entrypoint python \
  vasam-generator:local -m unittest docker.test_fetch_inputs
```

Run `gmapmaker.py` through this wrapper for local builds. The upstream `make.py`
is a batch publishing script and includes an upload step.

## Verified Czech build

On 2026-10-20 this setup completed a full Czech Unicode build on Apple Silicon
using Python 3.12, Java 17, pyhgtmap 4.1, splitter 654 and mkgmap 4924. The OSM
snapshot was 2026-10-18T20:25:06Z. Splitting, compilation and packaging took
10m36s with the above limits, after downloads and contour generation were cached.

The generated device IMG was 585,924,608 bytes, with 72 decodable tiles (64 OSM
and 8 contour tiles). The local Garmin renderer loaded its routing graph:
2,608,333 nodes and 7,487,500 arcs, with zero unsupported routing tiles. Country
and Prague-area renders succeeded. The BaseCamp ZIP passed a full CRC check and
both generated files matched the hashes in the `.info` file.

Local test evidence is retained under the ignored `output/` directory:
`build-CZ.log`, `input-manifest.json`, `python-packages.txt`, `docker-image.txt`,
`inspect-CZ.txt`, `routing-CZ.txt`, `validation-CZ.txt` and the preview PNGs.
