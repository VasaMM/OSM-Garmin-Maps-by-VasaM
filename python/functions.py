import os
# import os, sys, glob, zipfile, hashlib
# import urllib.request
# from shutil import copyfile
from datetime import datetime
import argparse
from argparse import RawTextHelpFormatter

# from python.areas import State, area
from python.download import download
from python.print import say, question, error
import textwrap
# from string input lower





# Ukoncovaci funkce
def end(o):
	time_end = datetime.now()
	runtime = time_end - o.time_start
	say('Konec v ' + str(time_end) + ', beh ' + str(runtime), o)
	print('\007')






# Nactu arumenty
def parse_args(o):
	def checkBool(data):
		if str(data).lower() in ('yes', 'y'):
			return '[y]es'
		elif str(data).lower() in ('no', 'n'):
			return '[n]o'
		else:
			return data


	parser = argparse.ArgumentParser(
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


	parser.add_argument('--area', '-a', help='Id generované oblasti, viz seznam\nId of generated area, see list')
	parser.add_argument('--download', '-d', type=checkBool, choices=['[y]es', '[n]o'], help='Vynuti / zakaze stazeni novych dat. Neni-li definovano, skript zobrazi dotaz.')
	parser.add_argument('--quiet', '-q', action='store_true', help='Zadne vypisy na stdout\nNo messages on stdout')
	parser.add_argument('--no_split', action='store_true', help='Zakaze deleni mapy na podsoubory - vhodne jen pro velmi male oblasti')
	# parser.add_argument('--mapsforge', '-m',action='store_true', help='mapsforge - nenni hotovo')
	parser.add_argument('--logging', '-l',action='store_true', help='Vytvori logovaci soubor makeMap.log')
	

	args = parser.parse_args()

	o.split        = not args.no_split
	# o.mapsforge    = args.mapsforge
	o.state        = args.area
	o.download_map = None if args.download is None else args.download == '[y]es'
	o.quiet        = args.quiet
	o.log_file     = args.logging

	return o



# Vytvorim logovaci soubor, je-li potreba
def make_log_file(o):
	if o.log_file is True:
		try:
			o.log_file = open("makeMap.log", "w+")
		except:
			error("Cann't open file 'makeMap.log'", o)



def download_map_data(o):
	# Zjistim, zda mam stahovat data
	if not o.state.data_url:
		o.download_map = False


	# Data jiz byla stazena
	if os.path.isfile('./pbf/' + o.state.data_id + '.osm.pbf'):
		say('File ' + o.state.data_id + '.osm.pbf found', o)
		
		# Uzivatel nespecifikoval, co se ma stat
		if o.download_map is None and o.state.data_url != False:
			o.download_map = question('Map data has already been download, do you want to use it?')

	else:
		if not o.state.data_url:
			error('Map file does NOT exist!', o)

		o.download_map = True


	# Stahnu data
	if o.download_map:
		try:
			say('Downloading map data', o)
			download(o.state.data_url, './pbf/' + o.state.data_id + '.osm.pbf')
		except:
			error("Cann't download map data!", o)


	# Stahnu polygon
	try:
		if not os.path.isfile('./poly/' + o.state.data_id + '.poly'):
			if o.state.poly_url == False:
				error("Polygon '" + o.state.data_id + "' does NOT exist!", o)

			say('Downloading polygon', o)
			download(o.state.poly_url, './poly/' + o.state.data_id + '.poly')
	except:
		error("Cann't download polygon!", o)




def make_contours(o):
	# Zjistim, zda mam hotove vrstevnice
	try:
		if not os.path.isfile('./pbf/' + o.state.data_id + '-SRTM.osm.pbf'):
			say('Generate contour line', o)
			
			# --no-zero-contour
			os.system(
				'phyghtmap \
				--polygon=./poly/' + o.state.data_id + '.poly \
				-o ./pbf/' + o.state.data_id + '-SRTM \
				--pbf \
				-j 2 \
				-s 10 \
				-c 200,100 \
				--source=view3 \
				--start-node-id=20000000000 \
				--start-way-id=10000000000 \
				--write-timestamp \
				--max-nodes-per-tile=0 \
			')
			os.rename(glob.glob('./pbf/' + o.state.data_id + '-SRTM*.osm.pbf')[0], './pbf/' + o.state.data_id + '-SRTM.osm.pbf')
		else:
			say('Use previously generated contour lines', o)
	except:
		error("Cann't generate contour lines!", o)
