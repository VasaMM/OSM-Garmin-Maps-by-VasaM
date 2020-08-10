import textwrap, argparse, re
from argparse import RawTextHelpFormatter
from makerfuncs import parser
from makerfuncs.prints import say

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
		prog = 'gmapmaker',
		formatter_class = argparse.RawTextHelpFormatter,
		description = textwrap.dedent('''\
CZ: Skript pro generovani OSM map pro navigace Garmin
EN: Script for generating OSM maps for Garmin navigations

Author: VasaM
License: CC BY 4.0
Date: 10. 08. 2020
Web: https://github.com/VasaMM/OSM-Garmin-Maps-by-VasaM''')
		)


	argParser.add_argument(
		'--area', '-a',
		help='Id generovane oblasti, viz states.py\nId of generated area, see states.py'
	)
	argParser.add_argument(
		'--code-page', '-c',
		choices=['unicode', 'ascii', '1250', '1252', 'latin2'],
		default='1250',
		help='Kódova stranka ve vygenerovane mape\nCode page in the generated map'
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
		help='force - Mapova data se pri každem spusteni znovu stahnou | Every time it starts, the data is downloaded again\n\
skip - Mapova data se nebudou stahovat | Map data will not be downloaded\n\
auto - Mapova data se stahnou pouze pokud jsou starsi než --maximum-date-age <vychozi>| Map data will be downloaded only if they is older than --maximum-date-age <default>'
	)
	argParser.add_argument(
		'--maximum-data-age',
		type=_ageType,
		default='1d',
		help='Maximalni stari mapovych dat pri automatickem stahovani. Hodnoty ve tvaru [0-9]+[hdm], kde h znaci hodinu, d znaci den (24 hodin) a m znaci mesic (30 dni) <vychozi hodnota 1d>\n\
Maximum age of map data for automatic download. Value in the form [0-9]+[hdm], where h is hour, d is day (24 hours) and m is month (30 days) <default value is 1d>'
	)
	argParser.add_argument(
		'--map-number',
		type=int,
		help='Vynuti konkretni map ID'
	)
	argParser.add_argument(
		'--variant',
		choices=['0', '1', '2', '3', '4'],
		help='Vynuti konkretni cislo varianty (jinak automaticky)'
	)
	argParser.add_argument(
		'--extend', '-e',
		type=float,
		help='Zvetsi polygon o zadany pocet kilometrů\nExtend the polygon by the specified number of kilometers'
	)
	argParser.add_argument(
		'--sufix',
		type=str,
		help='Pripona za jmenem mapy'
	)
	argParser.add_argument(
		'--crop', '-r',
		action='store_true',
		help='Orizne mapovy soubor podle polygonu\nCrop the map file by the polygon'
	)
	argParser.add_argument(
		'--no-split',
		action='store_true',
		help='Zakaze deleni mapy na podsoubory - vhodne jen pro velmi male oblasti'
	)
	argParser.add_argument(
		'--quiet', '-q',
		action='store_true',
		help='Zadne vypisy na stdout\nNo messages on stdout'
	)
	argParser.add_argument(
		'--logging', '-l',
		action='store_true',
		help='Vytvori logovaci soubor makeMap.log'
	)
	

	args = argParser.parse_args()



	o.split          = not args.no_split
	o.area           = args.area
	o.downloadMap    = parser.downloadType(args.download)
	o.maximumDataAge = parser.age(args.maximum_data_age)
	o.extend         = args.extend
	o.quiet          = args.quiet
	o.logFile        = args.logging
	o.code           = args.code_page
	o.crop           = args.crop
	o.mapNumber      = args.map_number
	o.variant        = args.variant
	o.sufix          = '_VasaM' if args.sufix is None else '_' + args.sufix + '_VasaM'

