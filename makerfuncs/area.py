import os
from makerfuncs.prints import say


class State:
	def __init__(self, name, number, data_url = None, poly_url = None, data_id = None, pois = None):
		self.data_url = data_url      # map data url address (*.osm.pbf file)
		self.poly_url = poly_url      # polygon url address (*.poly or *.geojson file)
		self.name     = name          # Full name of map
		self.number   = number        # Map number id
		self.pois     = pois          # List of files with pois
		self.data_id  = data_id       # If you want use another id
		# self.code     = ' --code-page=1250 + code + ' '
		
		# if len(lang) > 0:
		# 	self.lang = ' --name-tag-list='
		# 	for l in lang:
		# 		self.lang += 'name:' + l + ','
	
		# 	self.lang = self.lang[ 0 : -1 ] + ' '
		# else:
		# 	self.lang = ' '


STATES = {
	'OL': State(
		name     = 'Olomouc',
		number   = 8800,
		# code     = 'unicode',
	),

	#Stredni Evropa ID: 8801 - 8810
	'CZ': State(
		data_url = 'http://download.geofabrik.de/europe/czech-republic-latest.osm.pbf',
		poly_url = 'http://download.geofabrik.de/europe/czech-republic.poly',
		name     = 'Ceska republika',
		number   = 8801,
		pois     = ('chs',),
	),

	'SK': State(
		data_url = 'http://download.geofabrik.de/europe/slovakia-latest.osm.pbf',
		poly_url = 'http://download.geofabrik.de/europe/slovakia.poly',
		name     = 'Slovenska republika',
		number   = 8802,
	),

	'PL': State(
		data_url = 'http://download.geofabrik.de/europe/poland-latest.osm.pbf',
		poly_url = 'http://download.geofabrik.de/europe/poland.poly',
		name     = 'Polsko',
		number   = 8803,
	),

	'DE': State(
		data_url = 'http://download.geofabrik.de/europe/germany-latest.osm.pbf',
		poly_url = 'http://download.geofabrik.de/europe/germany.poly',
		name     = 'Nemecko',
		number   = 8804,
	),

	'AT': State(
		data_url = 'http://download.geofabrik.de/europe/austria-latest.osm.pbf',
		poly_url = 'http://download.geofabrik.de/europe/austria.poly',
		name     = 'Rakousko',
		number   = 8805,
	),

	#Ostatni Evropa ID: 8811 - 8840
	'UA': State(
		data_url = 'http://download.geofabrik.de/europe/ukraine-latest.osm.pbf',
		poly_url = 'http://download.geofabrik.de/europe/ukraine.poly',
		name     = 'Ukrajina',
		number   = 8811,
	),

	'RO': State(
		data_url = 'http://download.geofabrik.de/europe/romania-latest.osm.pbf',
		poly_url = 'http://download.geofabrik.de/europe/romania.poly',
		name     = 'Rumunsko',
		number   = 8812,
	),

	'HR': State(
		data_url = 'http://download.geofabrik.de/europe/croatia-latest.osm.pbf',
		poly_url = 'http://download.geofabrik.de/europe/croatia.poly',
		name     = 'Chorvatsko',
		number   = 8813,
	),

	'NO': State(
		data_url = 'http://download.geofabrik.de/europe/norway-latest.osm.pbf',
		poly_url = 'http://download.geofabrik.de/europe/norway.poly',
		name     = 'Norsko',
		number   = 8814,
	),

	'DK': State(
		data_url = 'http://download.geofabrik.de/europe/denmark-latest.osm.pbf',
		poly_url = 'http://download.geofabrik.de/europe/denmark.poly',
		name     = 'Dansko',
		number   = 8815,
	),

	'SI': State(
		data_url = 'http://download.geofabrik.de/europe/slovenia-latest.osm.pbf',
		poly_url = 'http://download.geofabrik.de/europe/slovenia.poly',
		name     = 'Slovinsko',
		number   = 8816,
	),

	'GR': State(
		data_url = 'http://download.geofabrik.de/europe/greece-latest.osm.pbf',
		poly_url = 'http://download.geofabrik.de/europe/greece.poly',
		name     = 'Recko',
		number   = 8817,
	),

	'HU': State(
		data_url = 'http://download.geofabrik.de/europe/hungary-latest.osm.pbf',
		poly_url = 'http://download.geofabrik.de/europe/hungary.poly',
		name     = 'Madarsko',
		number   = 8818,
	),

	'ES': State(
		data_url = 'http://download.geofabrik.de/europe/spain-latest.osm.pbf',
		poly_url = 'http://download.geofabrik.de/europe/spain.poly',
		name     = 'Spanelsko',
		number   = 8819,
	),

	'IT': State(
		data_url = 'http://download.geofabrik.de/europe/italy-latest.osm.pbf',
		poly_url = 'http://download.geofabrik.de/europe/italy.poly',
		name     = 'Italie',
		number   = 8820,
	),

	'NL': State(
		data_url = 'http://download.geofabrik.de/europe/netherlands-latest.osm.pbf',
		poly_url = 'http://download.geofabrik.de/europe/netherlands.poly',
		name     = 'Nizozemsko',
		number   = 8821,
	),

	'AD': State(
		data_url = 'http://download.geofabrik.de/europe/andorra-latest.osm.pbf',
		poly_url = 'http://download.geofabrik.de/europe/andorra.poly',
		name     = 'Andorra',
		number   = 8822,
	),

	'BG': State(
		data_url = 'http://download.geofabrik.de/europe/bulgaria-latest.osm.pbf',
		poly_url = 'http://download.geofabrik.de/europe/bulgaria.poly',
		name     = 'Bulharsko',
		number   = 8823,
	),

	'CH': State(
		data_url = 'http://download.geofabrik.de/europe/switzerland-latest.osm.pbf',
		poly_url = 'http://download.geofabrik.de/europe/switzerland.poly',
		name     = 'Svycarsko',
		number   = 8824,
	),

	'GB': State(
		data_url = 'http://download.geofabrik.de/europe/great-britain-latest.osm.pbf',
		poly_url = 'http://download.geofabrik.de/europe/great-britain.poly',
		name     = 'Velka Britanie',
		number   = 8825,
	),


	#Ostatni ID: 8831 - 8890
	'KG': State(
		data_url = 'http://download.geofabrik.de/asia/kyrgyzstan-latest.osm.pbf',
		poly_url = 'http://download.geofabrik.de/asia/kyrgyzstan.poly',
		name     = 'Kyrgyzstan',
		number   = 8841,
	),

	'KZ': State(
		data_url = 'http://download.geofabrik.de/asia/kazakhstan-latest.osm.pbf',
		poly_url = 'http://download.geofabrik.de/asia/kazakhstan.poly',
		name     = 'Kazachstan',
		number   = 8842,
	),

	'NP': State(
		data_url = 'http://download.geofabrik.de/asia/nepal-latest.osm.pbf',
		poly_url = 'http://download.geofabrik.de/asia/nepal.poly',
		name     = 'Nepal',
		number   = 8843,
	),

	'MA': State(
		data_url = 'http://download.geofabrik.de/africa/morocco-latest.osm.pbf',
		poly_url = 'http://download.geofabrik.de/africa/morocco.poly',
		name     = 'Maroko',
		number   = 8844,
	),

	'TJ': State(
		data_url = 'http://download.geofabrik.de/asia/tajikistan-latest.osm.pbf',
		poly_url = 'http://download.geofabrik.de/asia/tajikistan.poly',
		name     = 'Tadzikistan',
		number   = 8845,
	),

	'NY': State(
		data_url = 'http://download.geofabrik.de/north-america/us/new-york-latest.osm.pbf',
		poly_url = 'http://download.geofabrik.de/north-america/us/new-york.poly',
		name     = 'New York',
		number   = 8846,
	),

	'VN': State(
		data_url = 'https://download.geofabrik.de/asia/vietnam-latest.osm.pbf',
		poly_url = 'https://download.geofabrik.de/asia/vietnam.poly',
		name     = 'Vietnam',
		number   = 8847,
	),

	'IR': State(
		data_url = 'https://download.geofabrik.de/asia/iran-latest.osm.pbf',
		poly_url = 'https://download.geofabrik.de/asia/iran.poly',
		name     = 'Iran',
		number   = 8848,
		# code     = 'unicode',
		# lang     = ['cs','en'],
	),
	
	'IR_en': State(
		data_url = 'https://download.geofabrik.de/asia/iran-latest.osm.pbf',
		poly_url = 'https://download.geofabrik.de/asia/iran.poly',
		data_id  = 'IR',
		name     = 'Iran - en',
		number   = 8849,
		# code     = 'unicode',
		# lang     = ['cs','en'],
	),
	
	'Canary_islands': State(
		data_url = 'https://download.geofabrik.de//africa/canary-islands-latest.osm.pbf',
		poly_url = 'https://download.geofabrik.de//africa/canary-islands.poly',
		name     = 'Kanarske ostrovy',
		number   = 8850,
	),
}


def get(o):
	while True:
		if o.state in STATES:
			# doplnim id
			STATES[ o.state ].id = o.state

			# popr. i data_id
			if STATES[ o.state ].data_id is None:
				STATES[ o.state ].data_id = o.state
			
			# Vratim hodnotu
			o.state = STATES[ o.state ]

			say('Area id: ' + o.state.id, o)
			say('Data id: ' + o.state.data_id, o)
			return
		
		else:
			print('Zadejte zkratku statu, pro ktery chcete vytvorit mapu.')
			for o.state in STATES:
				print('  * [' + o.state + '] - ' + STATES[ o.state ].name)

			o.state = input('Vybrana mapa: ')

