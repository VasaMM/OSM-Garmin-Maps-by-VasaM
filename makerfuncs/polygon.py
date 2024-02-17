# https://wiki.openstreetmap.org/wiki/Osmosis/Polygon_Filter_File_Python_Parsing
import pyclipper, re, os, geojson, functools
from geojson import Polygon, Feature, FeatureCollection
from makerfuncs.Options import Options
from makerfuncs.prints import say
from makerfuncs.Lang import _


def _loadPoly(fileName: str) -> list[tuple[float, float]]:
	# https://github.com/ustroetz/polygon2osm/blob/master/polygon2geojson.py
	coordinates = None
	with open(fileName) as polyFile:
		coordinates = polyFile.readlines()[2:][:-2]

	coordinates = [re.split(r'[\s\t]+', item) for item in coordinates]
	coordinates = [list(filter(None, item)) for item in coordinates]
	coordinates = functools.reduce(lambda a,b: a[-1].pop(0) and a if len(a[-1]) == 1 and a[-1][0] == 'END' else a.append(['END']) or a if b[0].startswith('END') else a[-1].append(b) or a, [[[]]] + coordinates)
	coordinates = [[(float(item[0]), float(item[1])) for item in coordgroup] for coordgroup in coordinates]

	return coordinates[0]


def _loadGeojson(fileName: str) -> list[tuple[float, float]]:
	with open(fileName) as geojsonFile:
		data = geojson.load(geojsonFile)

		# Load first polygon
		for feature in data['features']:
			for key,value in feature.items():
				if key == 'geometry' and value['type'] == 'Polygon':
					return value['coordinates'][0]


def _savePoly(fileName: str, polygon: list[tuple[float, float]]) -> None:
	if not os.path.exists(os.path.dirname(fileName)):
		os.makedirs(os.path.dirname(fileName))

	with open(fileName, 'w') as polyFile:
		polyFile.write('None' + "\n")
		polyFile.write('1' + "\n")
		for coord in polygon:
			polyFile.write("\t" + str(coord[0]) + "\t" + str(coord[1]) + "\n")
		polyFile.write('END' + "\n")
		polyFile.write('END' + "\n")


def _saveGeojson(fileName: str, polygon: list[tuple[float, float]]) -> None:
	if not os.path.exists(os.path.dirname(fileName)):
		os.makedirs(os.path.dirname(fileName))

	feature = Feature(geometry=Polygon([polygon]))
	collection = FeatureCollection([feature])

	with open(fileName, 'w') as polyFile:
		polyFile.write(geojson.dumps(collection))



def _extend(o: Options) -> None:
	say(_('Extending polygon'), o)
	# [[17.25743, 49.58712], [17.24355, 49.58712], [17.24355, 49.5964], [17.25743, 49.5964], [17.25743, 49.58712]]

	extender = pyclipper.PyclipperOffset()

	MULTIPLIER = 100000
	path = []
	for point in o.polygon:
		path.append([int(point[0] * MULTIPLIER), int(point[1] * MULTIPLIER)])


	# http://www.angusj.com/delphi/clipper/documentation/Docs/Units/ClipperLib/Classes/ClipperOffset/Methods/AddPath.htm
	extender.AddPath(path, pyclipper.JT_MITER, pyclipper.ET_CLOSEDPOLYGON)
	solution = extender.Execute(1600 * o.extend)[0]   # FIXME Value 1600 experimentally works for CZ

	for i in range(len(solution)):
		point = solution[i]
		solution[i] = [point[0]/MULTIPLIER, point[1]/MULTIPLIER]

	solution.append(solution[0])

	o.polygon = solution


def load(o: Options):
	polyPath = os.path.join(o.polygons, o.area.id + '.poly')
	jsonPath = os.path.join(o.polygons, o.area.id + '.geojson')

	# Doesn't exist *.poly file, create it from *.geojson
	if not os.path.isfile(polyPath):
		# Doesn't either *.geojson -> error
		if not os.path.isfile(jsonPath):
			raise ValueError(o.area.id + '.poly ' + _('or') + ' ' + o.area.id + '.geojson ' + _('missing') + '!')

		o.polygon = _loadGeojson(jsonPath)
		_savePoly(polyPath, o.polygon)

	# Exist *.poly file, create *.geojson, if it doesn't exist yet
	elif not os.path.isfile(jsonPath):
		o.polygon = _loadPoly(polyPath)
		_saveGeojson(jsonPath, o.polygon)

	# Exist *.poly and *.geojson, load geojson
	else:
		o.polygon = _loadGeojson(jsonPath)

	if o.extend is not None:
		_extend(o)
		o.crop = True

	_savePoly(os.path.join(o.temp, 'polygon.poly'), o.polygon)
