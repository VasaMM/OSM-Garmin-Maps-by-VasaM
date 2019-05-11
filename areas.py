class State:
	def __init__( self, name, number, data_url = False, poly_url = False, data_id = None, pois = None, code = 'code-page=1250', lang = [] ):
		self.data_url = data_url
		self.poly_url = poly_url
		self.name     = name
		self.number   = number
		self.pois     = pois
		self.id       = ''
		self.data_id  = data_id
		self.code     = ' --' + code + ' '
		
		if len( lang ) > 0:
			self.lang = ' --name-tag-list='
			for l in lang:
				self.lang += 'name:' + l + ','
	
			self.lang = self.lang[ 0 : -1 ] + ' '
		else:
			self.lang = ' '


STATES = {
	'OL': State(
		data_url = False,
		poly_url = False,
		name     = 'Olomouc',
		number   = 8800,
		code     = 'unicode',
	),

	#Stredni Evropa ID: 8801 - 8810
	'CZ': State(
		data_url = 'http://download.geofabrik.de/europe/czech-republic-latest.osm.pbf',
		poly_url = 'http://download.geofabrik.de/europe/czech-republic.poly',
		name     = 'Ceska republika',
		number   = 8801,
		pois     = ( 'chs', ),
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
		code     = 'unicode',
		lang     = ['cs','en'],
	),
	
	'IR_en': State(
		data_url = 'https://download.geofabrik.de/asia/iran-latest.osm.pbf',
		poly_url = 'https://download.geofabrik.de/asia/iran.poly',
		data_id  = 'IR',
		name     = 'Iran - en',
		number   = 8849,
		code     = 'unicode',
		lang     = ['cs','en'],
	),
}


def area( state ):
	while True:
		if state in STATES:
			STATES[ state ].id = state
			if STATES[ state ].data_id is None:
				STATES[ state ].data_id = state
			return STATES[ state ]
		else:
			print( 'Zadejte zkratku statu, pro ktery chcete vytvorit mapu.' )
			for state in STATES:
				print( '  * [' + state + '] - ' + STATES[ state ].name )

			state = input( 'Vybrana mapa: ' )
