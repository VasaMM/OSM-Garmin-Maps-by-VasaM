import os, re
from datetime import datetime, timezone

from makerfuncs.generator import run, getActualOsmconvert
from makerfuncs.prints import say, error
from makerfuncs.Options import Options
from makerfuncs.Lang import Lang, _
from makerfuncs.Area import State, Area
from makerfuncs.states import STATES
from userAreas.myAreas import USER_AREAS



def fileHeader(o: Options) -> None:
	say(_('Parsing file header'), o)
	timestamp: datetime
	o.area.timestamp = datetime.fromtimestamp(0).replace(tzinfo=timezone.utc)

	o.area.file = False
	if os.path.isfile(o.area.mapDataName):

		# osmconvert\osmconvert64.exe pbf\AD.osm.pbf --out-statistics
		try:
			version = run([os.path.join('osmconvert', getActualOsmconvert()),
				o.area.mapDataName,
				'--out-statistics'
				]
				, o)
			match = re.search("timestamp max: (.*)", version)
			if match:
				timestamp = match.group(1)
		except:
			say(_('Unknown file age.'), o)
			return

		o.area.file = True

		try:
			timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
			o.area.timestamp = timestamp.replace(tzinfo=timezone.utc)

		except ValueError:
			error(_('Date in OSM file header is not in ISO8601 format (e.g. 2015-12-24T08:08Z). Ignored'), o)

		say(_('File from ') + str(o.area.timestamp), o)


def maximumDataAge(age):
	if age == 'Jsou-li starší než týden':
		return 7 * 24 * 3600
	elif age == 'Jsou-li starší než 3 dny':
		return 3 * 24 * 3600
	else:
		return 1 * 24 * 3600


# Return old in hours
def age(age: str) -> int:
	unit = age[-1]

	if unit == 'h':
		return int(age[0:-1]) * 3600
	elif unit == 'd':
		return int(age[0:-1]) * 3600 * 24
	elif unit == 'm':
		return int(age[0:-1]) * 3600 * 24 * 30


def downloadType(data: str) -> str:
	if data in ['[f]orce', 'Vždy']:
		return 'force'
	elif data in ['[s]kip', 'Nikdy']:
		return 'skip'
	elif data in ['[a]uto', 'Jsou-li starší než 1 den', 'Jsou-li starší než 3 dny', 'Jsou-li starší než týden']:
		return 'auto'


def codePage(codePage):
	if codePage == 'Windows-1250':
		return '1250'
	elif codePage == 'Windows-1252':
		return '1252'
	elif codePage == 'Latin-2':
		return 'latin2'
	elif codePage == 'Unicode':
		return 'unicode'
	else:
		return 'ascii'


def _findState(id: str) -> State:
	for area in STATES:
		if id in STATES[area]:
			return STATES[area][id], area
	return None


def _makeAreaObject(id: str, obj: object, options: Options, continent: str = None) -> Area:
	# Fill id a dataId
	obj.id = id

	if hasattr(obj, 'parent') and obj.parent is not None:
		say(_('The area depends on the data of area ') + obj.parent, options)

		state = _findState(obj.parent)
		if state is not None:
			obj.url = "http://download.geofabrik.de/%s/%s-latest.osm.pbf" % (state[1], state[0].url)

		elif obj.parent in USER_AREAS:
			obj.url = USER_AREAS[obj.parent].url

		else:
			raise ValueError(_('Invalid parent ID') + ' \'' + obj.parent + '\' ' + _('in') + ' \'' + id + '\'')

		obj.mapDataName = os.path.join(options.pbf, obj.parent + '.osm.pbf')

	else:
		obj.url = "http://download.geofabrik.de/%s/%s-latest.osm.pbf" % (continent, obj.url)
		obj.mapDataName = os.path.join(options.pbf, id + '.osm.pbf')

	if continent is not None:
		obj.continent = continent

	return obj


def area(o: Options) -> None:
	if o.areaId is None:
		raise ValueError(_('Area isn\'t set!'))

	say(_('Decoding area ') + o.areaId, o)

	if o.areaId in USER_AREAS:
		say(_('Area found in user areas'), o)
		o.area = _makeAreaObject(id = o.areaId, obj = USER_AREAS[o.areaId], options = o)


	else:
		state = _findState(o.areaId)
		if state is not None:
			o.area = _makeAreaObject(id = o.areaId, obj = state[0], options = o, continent = state[1])
		else:
			raise ValueError(_('Invalid area ') + o.areaId)

	if o.mapNumber is not None:
		o.area.number = o.mapNumber

	if o.variant is not None:
		o.area.number += int(o.variant)

	say(str(o.area), o)
	say(_('Area ID: ') + o.area.id, o)
