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
		if cls.language == 'en':
			return text
		elif cls.language == 'cs':
			return cls.cs[text] if text in cls.cs else text

	@classmethod
	def _e(cls, text):
		print(cls.__(text))


	cs = {
		' (0 expected)': ' (ocekavana 0)',
		'Area found in user areas': 'Oblast nalezena v uzivatelskych oblastech',
		'Area ID: ': 'ID oblasti: ',
		'Cann\'t download map data!': 'Nelze stahnout mapova data!',
		'Cann\'t open file ': 'Nelze otevrit soubor ',
		'Creating crop of an area': 'Vytvarim vyrez oblasti',
		'Date in OSM file header is not in ISO8601 format (e.g. 2015-12-24T08:08Z). Ignored': 'Datum v hlavicce OSM souboru neni ve formatu ISO8601 (napr. 2015-12-24T08:08Z). Ignoruji',
		'Decoding area ': 'Dekoduji oblast ',
		'Download polygon': 'Stahuji polygon',
		'Download': 'Stahuji',
		'Downloading map data': 'Stahuji mapova data',
		'End at ': 'Ukonceno v ',
		'Extending polygon': 'Rozsiruji polygon',
		'File for crop is too big': 'Soubor pro orez je prilis velky',
		'File from ': 'Soubor z ',
		'Generating contours': 'Generuji vrstevnice',
		'Generating map': 'Generuji mapu',
		'I don\'t have data url - skip downloading': 'Neznam URL adresu - preskakuji',
		'in': 'v',
		'Invalid area': 'Neplatna oblast ',
		'Invalid parent ID': 'Neplatne ID rodice',
		'Make info file': 'Vytvarim info soubor',
		'Make map for Garmin...': 'Vytvarim mapu pro Garmin...',
		'Make zip file': 'Vytvarim zip soubor',
		'Map data is to young - skip downloading': 'Mapova data jsou prilis mlada - nestahuji',
		'Map file does NOT exist!': 'Mapový soubor NEEXISTUJE!',
		'maximum is 2 GB. See GitHub for details.': 'maximum jsou 2 GB. Detaily viz GitHub.',
		'Parsing file header': 'Ctu hlavicku souboru',
		'Prepare license file': 'Pripravuji licencni soubor',
		'Rename files': 'Prejmenuji soubory',
		'return': 'vratil',
		'runtime': 'doba behu',
		'Select a continent': 'Vyberte svetadil',
		'Select a state': 'Vyberte stat',
		'Selected: ': 'Vybrano: ',
		'Split files - DONE': 'Rozdeleni souboru - HOTOVO',
		'Split files start': 'Spoustim rozdeleni souboru',
		'Start at ': 'Spusteno v ',
		'Start map data download': 'Spoustim stahovani mapovych dat',
		'Terminated by user': 'Ukonceno uzivatelem',
		'The area depends on the data of area ': 'Oblast je zavisla na datech oblasti ',
		'Use previously generated contours': 'Pouzivam drive vytvorene vrstevnice',
		'User set "--download skip" - skip downloading': 'Uzivatel nastavil "--download skip" - nestahuji',
	}

Lang = LangClass()

def _(text):
	return Lang.__(text)