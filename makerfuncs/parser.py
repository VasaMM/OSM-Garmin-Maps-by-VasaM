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
	o.area.timestamp = None
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
			return

		o.area.file = True

		try:
			timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
			o.area.timestamp = timestamp.replace(tzinfo=timezone.utc)

		except ValueError:
			error(_('Date in OSM file header is not in ISO8601 format (e.g. 2015-12-24T08:08Z). Ignored'), o)
			o.area.timestamp = None

		say(_("File from ") + str(o.area.timestamp), o)



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
	if data == '[f]orce':
		return 'force'
	elif data == '[s]kip':
		return 'skip'
	elif data == '[a]uto':
		return 'auto'


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
			raise ValueError(_('Ivalid parent ID') + ' \'' + obj.parent + '\' ' + _('in') + ' \'' + id + '\'')

		obj.mapDataName = os.path.join(options.pbf, obj.parent + '.osm.pbf')

	else:
		obj.url = "http://download.geofabrik.de/%s/%s-latest.osm.pbf" % (continent, obj.url)
		obj.mapDataName = os.path.join(options.pbf, id + '.osm.pbf')

	if continent is not None:
		obj.continent = continent

	return obj


def area(o: Options) -> None:
	if o.areaId is None:
		while True:
			print('\n' + _('Select a continent'))
			for continent in STATES:
				print(continent)

			continent = input(_('Selected: '))
			if continent not in STATES:
				continue
			else:
				break

		while True:
			print('\n' + _('Select a state'))
			for state in STATES[continent]:
				if Lang.getLanguage() == 'cs':
					print(state, ' (', STATES[continent][state].nameCs, ')', sep='')
				else:
					print(state, ' (', STATES[continent][state].nameEn, ')', sep='')

			state = input(_('Selected: '))
			if state not in STATES[continent]:
				continue
			else:
				o.areaId = state
				break

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
