# TODO Change to Configuration class
from datetime import datetime
from makerfuncs.Area import Area

class Options:
    JAVAMEM: str
    MAX_JOBS: int
    VERSION: int

    img: str
    pbf: str
    polygons: str
    hgt: str
    temp: str
    sea: str
    bounds: str
    splitter: int
    mkgmap: int

    split: bool
    areaId: str
    downloadMap: str
    maximumDataAge: int
    extend: float
    quiet: bool
    logFile: bool
    code: str
    crop: bool
    mapNumber: int
    variant: str
    en: bool
    sufix: str

    timeStart: datetime
    downloaded: bool
    area: Area
    polygon: list[tuple[float, float]]