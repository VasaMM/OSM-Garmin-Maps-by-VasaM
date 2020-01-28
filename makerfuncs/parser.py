import os, osmium
from makerfuncs.prints import say, error
from datetime import datetime, timezone


def fileHeader(o):
	say("Parsing file header", o)
	o.state.timestamp = None
	if os.path.isfile(o.pbf + o.state.data_id + '.osm.pbf'):
		o.state.fileHeader = osmium.io.Reader(o.pbf + o.state.id + '.osm.pbf', osmium.osm.osm_entity_bits.NOTHING).header()
		o.state.timestamp = o.state.fileHeader.get("osmosis_replication_timestamp")
		try:
			o.state.timestamp = datetime.strptime(o.state.timestamp, "%Y-%m-%dT%H:%M:%SZ")
			o.state.timestamp = o.state.timestamp.replace(tzinfo=timezone.utc)

		except ValueError:
			error("Date in OSM file header is not in ISO8601 format (e.g. 2015-12-24T08:08Z). Ignored", o)
			o.state.timestamp = None

		say("File from " + str(o.state.timestamp), o)



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