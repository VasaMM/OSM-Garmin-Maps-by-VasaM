from makerfuncs.State import State


STATES = {
	#Stredni Evropa ID: 8801 - 8810
	'CZ': State(
		dataUrl = 'http://download.geofabrik.de/europe/czech-republic-latest.osm.pbf',
		polyUrl = 'http://download.geofabrik.de/europe/czech-republic.poly',
		name    = 'Ceska republika',
		number  = 8801,
		pois    = ['./pois/chs.osm.xml',],
	),

	'SK': State(
		dataUrl = 'http://download.geofabrik.de/europe/slovakia-latest.osm.pbf',
		polyUrl = 'http://download.geofabrik.de/europe/slovakia.poly',
		name    = 'Slovenska republika',
		number  = 8802,
	),

	'PL': State(
		dataUrl = 'http://download.geofabrik.de/europe/poland-latest.osm.pbf',
		polyUrl = 'http://download.geofabrik.de/europe/poland.poly',
		name    = 'Polsko',
		number  = 8803,
	),

	'DE': State(
		dataUrl = 'http://download.geofabrik.de/europe/germany-latest.osm.pbf',
		polyUrl = 'http://download.geofabrik.de/europe/germany.poly',
		name    = 'Nemecko',
		number  = 8804,
	),

	'AT': State(
		dataUrl = 'http://download.geofabrik.de/europe/austria-latest.osm.pbf',
		polyUrl = 'http://download.geofabrik.de/europe/austria.poly',
		name    = 'Rakousko',
		number  = 8805,
	),

	#Ostatni Evropa ID: 8811 - 8840
	'UA': State(
		dataUrl = 'http://download.geofabrik.de/europe/ukraine-latest.osm.pbf',
		polyUrl = 'http://download.geofabrik.de/europe/ukraine.poly',
		name    = 'Ukrajina',
		number  = 8811,
	),

	'RO': State(
		dataUrl = 'http://download.geofabrik.de/europe/romania-latest.osm.pbf',
		polyUrl = 'http://download.geofabrik.de/europe/romania.poly',
		name    = 'Rumunsko',
		number  = 8812,
	),

	'HR': State(
		dataUrl = 'http://download.geofabrik.de/europe/croatia-latest.osm.pbf',
		polyUrl = 'http://download.geofabrik.de/europe/croatia.poly',
		name    = 'Chorvatsko',
		number  = 8813,
	),

	'NO': State(
		dataUrl = 'http://download.geofabrik.de/europe/norway-latest.osm.pbf',
		polyUrl = 'http://download.geofabrik.de/europe/norway.poly',
		name    = 'Norsko',
		number  = 8814,
	),

	'DK': State(
		dataUrl = 'http://download.geofabrik.de/europe/denmark-latest.osm.pbf',
		polyUrl = 'http://download.geofabrik.de/europe/denmark.poly',
		name    = 'Dansko',
		number  = 8815,
	),

	'SI': State(
		dataUrl = 'http://download.geofabrik.de/europe/slovenia-latest.osm.pbf',
		polyUrl = 'http://download.geofabrik.de/europe/slovenia.poly',
		name    = 'Slovinsko',
		number  = 8816,
	),

	'GR': State(
		dataUrl = 'http://download.geofabrik.de/europe/greece-latest.osm.pbf',
		polyUrl = 'http://download.geofabrik.de/europe/greece.poly',
		name    = 'Recko',
		number  = 8817,
	),

	'HU': State(
		dataUrl = 'http://download.geofabrik.de/europe/hungary-latest.osm.pbf',
		polyUrl = 'http://download.geofabrik.de/europe/hungary.poly',
		name    = 'Madarsko',
		number  = 8818,
	),

	'ES': State(
		dataUrl = 'http://download.geofabrik.de/europe/spain-latest.osm.pbf',
		polyUrl = 'http://download.geofabrik.de/europe/spain.poly',
		name    = 'Spanelsko',
		number  = 8819,
	),

	'IT': State(
		dataUrl = 'http://download.geofabrik.de/europe/italy-latest.osm.pbf',
		polyUrl = 'http://download.geofabrik.de/europe/italy.poly',
		name    = 'Italie',
		number  = 8820,
	),

	'NL': State(
		dataUrl = 'http://download.geofabrik.de/europe/netherlands-latest.osm.pbf',
		polyUrl = 'http://download.geofabrik.de/europe/netherlands.poly',
		name    = 'Nizozemsko',
		number  = 8821,
	),

	'AD': State(
		dataUrl = 'http://download.geofabrik.de/europe/andorra-latest.osm.pbf',
		polyUrl = 'http://download.geofabrik.de/europe/andorra.poly',
		name    = 'Andorra',
		number  = 8822,
	),

	'BG': State(
		dataUrl = 'http://download.geofabrik.de/europe/bulgaria-latest.osm.pbf',
		polyUrl = 'http://download.geofabrik.de/europe/bulgaria.poly',
		name    = 'Bulharsko',
		number  = 8823,
	),

	'CH': State(
		dataUrl = 'http://download.geofabrik.de/europe/switzerland-latest.osm.pbf',
		polyUrl = 'http://download.geofabrik.de/europe/switzerland.poly',
		name    = 'Svycarsko',
		number  = 8824,
	),

	'GB': State(
		dataUrl = 'http://download.geofabrik.de/europe/great-britain-latest.osm.pbf',
		polyUrl = 'http://download.geofabrik.de/europe/great-britain.poly',
		name    = 'Velka Britanie',
		number  = 8825,
	),


	#Ostatni ID: 8831 - 8890
	'KG': State(
		dataUrl = 'http://download.geofabrik.de/asia/kyrgyzstan-latest.osm.pbf',
		polyUrl = 'http://download.geofabrik.de/asia/kyrgyzstan.poly',
		name    = 'Kyrgyzstan',
		number  = 8841,
	),

	'KZ': State(
		dataUrl = 'http://download.geofabrik.de/asia/kazakhstan-latest.osm.pbf',
		polyUrl = 'http://download.geofabrik.de/asia/kazakhstan.poly',
		name    = 'Kazachstan',
		number  = 8842,
	),

	'NP': State(
		dataUrl = 'http://download.geofabrik.de/asia/nepal-latest.osm.pbf',
		polyUrl = 'http://download.geofabrik.de/asia/nepal.poly',
		name    = 'Nepal',
		number  = 8843,
	),

	'MA': State(
		dataUrl = 'http://download.geofabrik.de/africa/morocco-latest.osm.pbf',
		polyUrl = 'http://download.geofabrik.de/africa/morocco.poly',
		name    = 'Maroko',
		number  = 8844,
	),

	'TJ': State(
		dataUrl = 'http://download.geofabrik.de/asia/tajikistan-latest.osm.pbf',
		polyUrl = 'http://download.geofabrik.de/asia/tajikistan.poly',
		name    = 'Tadzikistan',
		number  = 8845,
	),

	'NY': State(
		dataUrl = 'http://download.geofabrik.de/north-america/us/new-york-latest.osm.pbf',
		polyUrl = 'http://download.geofabrik.de/north-america/us/new-york.poly',
		name    = 'New York',
		number  = 8846,
	),

	'VN': State(
		dataUrl = 'https://download.geofabrik.de/asia/vietnam-latest.osm.pbf',
		polyUrl = 'https://download.geofabrik.de/asia/vietnam.poly',
		name    = 'Vietnam',
		number  = 8847,
	),

	'IR': State(
		dataUrl = 'https://download.geofabrik.de/asia/iran-latest.osm.pbf',
		polyUrl = 'https://download.geofabrik.de/asia/iran.poly',
		name    = 'Iran',
		number  = 8848,
	),
	
	'Canary_islands': State(
		dataUrl = 'https://download.geofabrik.de//africa/canary-islands-latest.osm.pbf',
		polyUrl = 'https://download.geofabrik.de//africa/canary-islands.poly',
		name    = 'Kanarske ostrovy',
		number  = 8850,
	),
}