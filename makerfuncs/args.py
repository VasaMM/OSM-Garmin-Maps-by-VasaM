import textwrap, argparse, re
from argparse import RawTextHelpFormatter
from makerfuncs import parser

def _downloadType(data):
	if str(data).lower() in ('force', 'f'):
		return '[f]orce'
	elif str(data).lower() in ('skip', 's'):
		return '[s]kip'
	elif str(data).lower() in ('auto', 'a'):
		return '[a]uto'
	else:
		return data


def _ageType(data):
	if re.match(r'^\d+[hdm]$', data):
		return data



# Nactu arumenty
def parse(o):
	argParser = argparse.ArgumentParser(
		#prog = 'makeMap2',
		formatter_class = argparse.RawTextHelpFormatter,
		description = textwrap.dedent('''\
CZ: Skript pro generovani OSM map pro navigace Garmin
EN: Script for generating OSM maps for Garmin navigations

Author: VasaM
License: CC BY 3.0 CZ
Date: 26. 09. 2019
Web: https://github.com/VasaMM/OSM-Garmin-Maps-by-VasaM''')
		)


	argParser.add_argument(
		'--area', '-a',
		help='Id generované oblasti, viz seznam\nId of generated area, see list'
	)
	argParser.add_argument(
		'--code-page', '-c',
		choices=['unicode', 'ascii', '1250', '1252'],
		default='1250',
		help='Kódová stránka ve vygenerované mapě\nCode page in the generated map'
	)
	# argParser.add_argument(
	# 	'--map-language', '-g',
	# 	choices=['cs'],
	# 	default='cs',
	# 	help='Jazyk mapy\nLanguage of map'
	# )
	argParser.add_argument(
		'--download', '-d',
		type=_downloadType,
		choices=['[f]orce', '[s]kip', '[a]uto'],
		default='[a]uto',
		help='force - Mapová data se při každém spuštění znovu stáhnou | Every time it starts, the data is downloaded again\n\
skip - Mapová data se nebudou stahovat | Map data will not be downloaded\n\
auto - Mapová data se stáhnou pouze pokud jsou starší než --maximum-date-age | Map data will be downloaded only if they is older than --maximum-date-age'
	)
	argParser.add_argument(
		'--maximum-data-age',
		type=_ageType,
		default='1d',
		help='Maximalni stari mapovych dat pri automatickem stahovani. Hodnoty ve tvaru [0-9]+[hdm], kde h znaci hodinu, d znaci den (24 hodin) a m znaci mesic (30 dni)\n\
Maximum age of map data for automatic download. Value in the form [0-9]+[hdm], where h is hour, d is day (24 hours) and m is month (30 days)'
	)
	argParser.add_argument(
		'--quiet', '-q',
		action='store_true',
		help='Zadne vypisy na stdout\nNo messages on stdout'
	)
	argParser.add_argument(
		'--no_split',
		action='store_true',
		help='Zakaze deleni mapy na podsoubory - vhodne jen pro velmi male oblasti'
	)
	argParser.add_argument(
		'--logging', '-l',
		action='store_true',
		help='Vytvori logovaci soubor makeMap.log'
	)
	

	args = argParser.parse_args()



	o.split          = not args.no_split
	o.state          = args.area
	o.downloadMap    = parser.downloadType(args.download)
	o.maximumDataAge = parser.age(args.maximum_data_age)
	o.quiet          = args.quiet
	o.logFile        = args.logging
	o.code           = args.code_page

	return o

