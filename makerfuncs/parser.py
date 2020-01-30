import os, osmium
from makerfuncs.prints import say, error
from datetime import datetime, timezone

from makerfuncs.State import State
from makerfuncs.states import STATES
from user.myAreas import USER_AREAS



def fileHeader(o):
	say("Parsing file header", o)
	o.area.timestamp = None
	o.area.fileHeader = None
	if os.path.isfile(o.area.mapDataName):
		o.area.fileHeader = osmium.io.Reader(o.area.mapDataName, osmium.osm.osm_entity_bits.NOTHING).header()
		o.area.timestamp = o.area.fileHeader.get("osmosis_replication_timestamp")
		try:
			o.area.timestamp = datetime.strptime(o.area.timestamp, "%Y-%m-%dT%H:%M:%SZ")
			o.area.timestamp = o.area.timestamp.replace(tzinfo=timezone.utc)

		except ValueError:
			error("Date in OSM file header is not in ISO8601 format (e.g. 2015-12-24T08:08Z). Ignored", o)
			o.area.timestamp = None

		say("File from " + str(o.area.timestamp), o)



# Vraci stari v hodinach
def age(age):
	unit = age[-1]

	if unit == 'h':
		return int(age[0:-1]) * 3600
	elif unit == 'd':
		return int(age[0:-1]) * 3600 * 24
	elif unit == 'm':
		return int(age[0:-1]) * 3600 * 24 * 30


def downloadType(data):
	if data == '[f]orce':
		return 'force'
	elif data == '[s]kip':
		return 'skip'
	elif data == '[a]uto':
		return 'auto'



def area(o):
	say('Dekoduji oblast ' + o.area, o)
	# while True:
	# 	if o.state in STATES:
	# 		# doplnim id
	# 		STATES[ o.state ].id = o.state

	# 		# popr. i dataId
	# 		if STATES[ o.state ].dataId is None:
	# 			STATES[ o.state ].dataId = o.state
			
	# 		# Vratim hodnotu
	# 		o.state = STATES[ o.state ]

	# 		say('Area id: ' + o.state.id, o)
	# 		say('Data id: ' + o.state.dataId, o)
	# 		return
		
	# 	else:
	# 		print('Zadejte zkratku statu, pro ktery chcete vytvorit mapu.')
	# 		for o.state in STATES:
	# 			print('  * [' + o.state + '] - ' + STATES[ o.state ].name)

	# 		o.state = input('Vybrana mapa: ')


	def updateState(id, obj):
		# Doplnim id a dataId
		obj.id = id

		if obj.parent is not None:
			say('Oblast je zavisla na datech oblasti ' + obj.parent, o)
			if obj.parent in STATES:
				obj.dataUrl = STATES[obj.parent].dataUrl
			elif obj.parent in USER_AREAS:
				obj.dataUrl = USER_AREAS[obj.parent].dataUrl
			else:
				raise ValueError('Ivalid parent ID \'' + obj.parent + '\' in \'' + id + '\'')

			obj.mapDataName = o.pbf + obj.parent + '.osm.pbf'
		else:
			obj.mapDataName = o.pbf + id + '.osm.pbf'

	if o.area in STATES:
		say('Oblast nalezena v preddefinovanych statech', o)
		updateState(o.area, STATES[o.area])
		o.area = STATES[o.area]

		say('Area id: ' + o.area.id, o)
		return

	elif o.area in USER_AREAS:
		say('Oblast nalezena v uzivatelskych oblastech', o)
		updateState(o.area, USER_AREAS[o.area])
		o.area = USER_AREAS[o.area]

		say('Area id: ' + o.area.id, o)
		return
	
	else:
		raise ValueError('Invalid area ID: \'' + o.area + '\'')

