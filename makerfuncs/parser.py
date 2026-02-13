import os, osmium
from makerfuncs.prints import say, error
from datetime import datetime, timezone

from makerfuncs.Area import Area
from makerfuncs.states import STATES
from userAreas.myAreas import USER_AREAS
from makerfuncs.Lang import Lang, _



def fileHeader(o):
	say(_('Ctu hlavicku souboru'), o)
	o.area.timestamp = None
	o.area.fileHeader = None
	if os.path.isfile(o.area.mapDataName):
		o.area.fileHeader = osmium.io.Reader(o.area.mapDataName, osmium.osm.osm_entity_bits.NOTHING).header()
		o.area.timestamp = o.area.fileHeader.get("osmosis_replication_timestamp")
		try:
			o.area.timestamp = datetime.strptime(o.area.timestamp, "%Y-%m-%dT%H:%M:%SZ")
			o.area.timestamp = o.area.timestamp.replace(tzinfo=timezone.utc)

		except ValueError:
			error(_('Datum v hlavicce OSM souboru neni ve formatu ISO8601 (napr. 2015-12-24T08:08Z). Ignoruji'), o)
			o.area.timestamp = None

		say(_("Soubor z ") + str(o.area.timestamp), o)



# Vraci stari v hodinach
def age(age):
	unit = age[-1]

	if unit == 'h':
		return int(age[0:-1]) * 3600
	elif unit == 'd':
		return int(age[0:-1]) * 3600 * 24
	elif unit == 'm':
		return int(age[0:-1]) * 3600 * 24 * 30


def CodePage(data):
	if data == 'unicode':
		return '65001'
	elif data == 'ascii':
		return '0'
	elif data in 'latin1':
		return '1252'
	elif data == 'latin2':
		return '1250'
	else:
		return data


def downloadType(data):
	if data == '[f]orce':
		return 'force'
	elif data == '[s]kip':
		return 'skip'
	elif data == '[a]uto':
		return 'auto'


def _findState(id):
	for area in STATES:
		if id in STATES[area]:
			return STATES[area][id], area
	return None


def _makeAreaObject(id, obj, options, continent = None):
	# Doplnim id a dataId
	obj.id = id

	if hasattr(obj, 'parent') and obj.parent is not None:
		say(_('Oblast je zavisla na datech oblasti ') + obj.parent, options)

		state = _findState(obj.parent)
		if state is not None:
			obj.url = "http://download.geofabrik.de/%s/%s-latest.osm.pbf" % (state[1], state[0].url)

		elif obj.parent in USER_AREAS:
			obj.url = USER_AREAS[obj.parent].url

		else:
			raise ValueError(_('Neplatne ID rodice') + ' \'' + obj.parent + '\' ' + _('v') + ' \'' + id + '\'')

		obj.mapDataName = options.pbf + obj.parent + '.osm.pbf'

	else:
		obj.url = "http://download.geofabrik.de/%s/%s-latest.osm.pbf" % (continent, obj.url)
		obj.mapDataName = options.pbf + id + '.osm.pbf'

	if continent is not None:
		obj.continent = continent

	return obj





def area(o):
	if o.area is None:
		while True:
			print('\n' + _('Vyberte svetadil'))
			for continent in STATES:
				print(continent)

			continent = input(_('Vybrano: '))
			if continent not in STATES:
				continue
			else:
				break

		while True:
			print('\n' + _('Vyberte stat'))
			for state in STATES[continent]:
				if Lang.getLanguage() == 'cs':
					print(state, ' (', STATES[continent][state].nameCs, ')', sep='')
				else:
					print(state, ' (', STATES[continent][state].nameEn, ')', sep='')

			state = input(_('Vybrano: '))
			if state not in STATES[continent]:
				continue
			else:
				o.area = state
				break

	say(_('Dekoduji oblast ') + o.area, o)

	if o.area in USER_AREAS:
		say(_('Oblast nalezena v uzivatelskych oblastech'), o)
		o.area = _makeAreaObject(id = o.area, obj = USER_AREAS[o.area], options = o)


	else:
		state = _findState(o.area)
		if state is not None:
			o.area = _makeAreaObject(id = o.area, obj = state[0], options = o, continent = state[1])

		else:
			raise ValueError(_('Neplatna oblast ') + o.area)

	if o.mapNumber is not None:
		o.area.number = o.mapNumber

	if o.variant is not None:
		o.area.number += int(o.variant)

	say(str(o.area), o)
	say(_('ID oblasti: ') + o.area.id, o)
