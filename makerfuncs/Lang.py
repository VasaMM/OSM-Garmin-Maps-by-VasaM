class LangClass:
	@classmethod
	def __init__(self):
		self.language = 'cs'

	@classmethod
	def bindLanguage(cls, lang):
		cls.language = lang

	@classmethod
	def getLanguage(cls):
		return cls.language

	@classmethod
	def __(cls, text):
		if cls.language == 'cs':
			return text
		elif cls.language == 'en':
			return cls.en[text] if text in cls.en else text

	@classmethod
	def _e(cls, text):
		print(cls.__(text))


	en = {
		' (ocekavana 0)': ' (0 expected)',
		'Afrika': 'Africa',
		'Asie': 'Asia',
		'Austrálie a Oceánie': 'Australia and Oceania',
		'Ctu hlavicku souboru': 'Parsing file header',
		'Datum v hlavicce OSM souboru neni ve formatu ISO8601 (napr. 2015-12-24T08:08Z). Ignoruji': "Date in OSM file header is not in ISO8601 format (e.g. 2015-12-24T08:08Z). Ignored",
		'Dekoduji oblast ': 'Decoding area ',
		'doba behu': 'runtime',
		'Evropa': 'Europe',
		'Generuji mapu': 'Generating map',
		'Generuji vrstevnice': 'Generating contours',
		'ID oblasti: ': 'Area ID: ',
		'Jižní Amerika': 'South America',
		'Mapova data jsou prilis mlada - nestahuji': 'Map data is to young - skip downloading',
		'Mapový soubor NEEXISTUJE!': 'Map file does NOT exist!',
		'maximum jsou 2 GB. Detaily viz GitHub.': 'maximum is 2 GB. See GitHub for details.',
		'Nelze otevrit soubor ': "Cann't open file ",
		'Nelze stahnout mapova data!': 'Cann\'t download map data!',
		'Neplatna oblast ': 'Invalid area',
		'Neplatne ID rodice': 'Ivalid parent ID',
		'Neznam URL adresu - preskakuji': 'I don\'t have data url - skip downloading',
		'Oblast je zavisla na datech oblasti ': 'The area depends on the data of area ',
		'Oblast nalezena v uzivatelskych oblastech': 'Area found in user areas',
		'Pouzivam drive vytvorene vrstevcnice': 'Use previously generated contours',
		'Prejmenuji soubory': 'Rename files',
		'Pripravuji licencni soubor': 'Prepare license file',
		'Rozdeleni souboru - HOTOVO': 'Split files - DONE',
		'Rozsiruji polygon': 'Extending polygon',
		'Rusko': 'Russia',
		'Severní Amerika': 'North America',
		'Soubor pro orez je prilis velky': 'File for crop is too big',
		'Soubor z ': 'File from ',
		'Spoustim rozdeleni souboru': 'Split files start',
		'Spoustim stahovani mapovych dat': 'Start map data download',
		'Spusteno v ': 'Start at ',
		'Stahuji mapova data': 'Downloading map data',
		'Stahuji polygon': 'Download polygon',
		'Stahuji': 'Download',
		'Střední Amerika': 'Central America',
		'Ukonceno uzivatelem': 'Terminated by user',
		'Ukonceno v ': 'End at ',
		'Uzivatel nastavil "--download skip" - nestahuji': 'User set "--download skip" - skip downloading',
		'Uživatelské oblasti': 'User areas',
		'v': 'in',
		'vratil': 'return',
		'Vyberte stat': 'Select a state',
		'Vyberte svetadil': 'Select a continent',
		'Vybrano: ': 'Selected: ',
		'Vytvarim info soubor': 'Make info file',
		'Vytvarim mapu pro Garmin...': 'Make map for Garmin...',
		'Vytvarim vyrez oblasti': 'Creating crop of an area',
		'Vytvarim zip soubor': 'Make zip file',
	}

Lang = LangClass()

def _(text):
	return Lang.__(text)