#!/usr/bin/env python3

import os, sys, glob, zipfile, hashlib
import urllib.request
from shutil import copyfile
from datetime import datetime


from areas import State, area
from download import download



# Nastevni
JAVAMEM='-Xmx8000m'		# Maximalni velikost RAM, kterou lze pouzit

VERSION=45				# Verze generovane mapy


# Ukoncovaci funkce
def end( time_start ):
	time_end = datetime.now()
	runtime = time_end - time_start
	print( '\nKonec v ', time_end, ', beh ', runtime, sep = '' )
	print( '\007' )
	exit()



# Napoveda
def printHelp():
	print ( '# Skript pro generovani OSM map pro Garmin' )
	print ()
	print ( '## Pozadavky ' )
	print ( '  * Linux ' )
	print ( '  * Java verze 8 ' )
	print ( '  * Python verze 3 (testovano na 3.4) ' )
	print ( '  * Program phyghtmap (http://katze.tfiu.de/projects/phyghtmap/) ' )
	print ( '  * FIXME ' )
	print ()
	print ( '## Pouziti ' )
	print ( '  Skript je nezvykle ukecany (do budoucna je v planu i ticha verze) a na zacatku spusteni se uzivatele pta, co chce udelat. Proto jej staci spustit bez parametru. ' )
	print ( '  Pro bezobsluzne automaticke spousteni lze chovani ovlivnit pomoci parametru: ' )
	print ( '	* -a <stat> | --area <stat> definuje stat/oblast, pro kterou je mapa generovana. Viz seznam statu. ' )
	print ( '	* -dy | --download_yes vynuti vzdy nove stazeni mapovych dat ' )
	print ( '	* -dn | --download_no v pripade, ze byli drive stazena mapova data, nebudou se znovu stahovat. ' )
	print ( '		**POZOR**, neni provadena validace techto dat. Jedna-li se o fragment z prechoziho preruseneho stahovani, dojde k chybe. ' )
	print ( '	* -ns | --no_split zakaze deleni mapovych souboru na mensi dily. Vhodne pouze u velmi malych oblasti a pro pocitace s dostatkem RAM. ' )
	print ( '	* -h | --help zobrazi tuto napovedu. ' )
	print ()
	print ( 'Staty jsou definovany ve skriptu areas.py.' )


def main():
	# Zaznamenam cas spusteni
	time_start = datetime.now()
	print( 'Spusteno v', time_start )

	split = True
	mapsforge = False
	state = None
	download_map = None


	# Nactu arumenty
	i = 1
	while i < len(sys.argv):
		arg = sys.argv[ i ]
		i += 1

		if arg in ( '-h', '--help' ):
			printHelp()
			exit()

		elif arg in ( '-a', '--area' ):
			state = sys.argv[ i ]
			i += 1
	
		elif arg in ( '-dy', '--download_yes' ):
			download_map = True
	
		elif arg in ( '-dn', '--download_no' ):
			download_map = False
	
		elif arg in ( '-ns', '--no_split' ):
			split = False

		elif arg in ( '-m', '--mapsforge' ):
			mapsforge = True
	
		else:
			print( "Neznamy argument '" + arg + "'!" )
			exit( 1 );


	# Ziskam stat, nebyl-li zadan
	state = area( state )

	print( 'state:', state.id)


	# Zjistim, zda mam stahovat data
	if not state.data_url:
		download_map = False

	# Data jiz byla stazena
	if os.path.isfile( './pbf/' + state.id + '.osm.pbf' ):
		print( 'Nalezen soubor ' + state.id + '.osm.pbf' )
		
		# Uzivatel nespecifikoval, co se ma stat
		if download_map is None and state.data_url != False:
			while True:
				answer = input( 'Data pro mapu byla uz stazena, chcete je pouzit? [A/n] ' )
				if answer in ( 'A', 'a' ):
					download_map = False
					break
				elif answer in ( 'N', 'n' ):
					download_map = True
					break
				else:
					print ( 'Neplatný vstup, zkuste to znovu' )
	else:
		if not state.data_url:
			print( 'NEnalezen soubor ${STATE}.osm.pbf!' )
			exit(1)

		download_map = True


	# Stahnu data
	if download_map:
		print( 'Stahuji aktualni data' )
		download( state.data_url, './pbf/' + state.id + '.osm.pbf' )


	# Stahnu polygon
	if not os.path.isfile( './poly/' + state.id + '.poly' ):
		if state.poly_url == False:
			print( 'NEnalezen soubor ' + state.id + '.poly!' )
			exit(1)

		print( 'Stahuji hranice statu' )
		download( state.poly_url, './poly/' + state.id + '.poly' )


	# Zjistim, zda mam hotove vrstevnice
	if not os.path.isfile( './pbf/' + state.id + '-SRTM.osm.pbf' ):
		print( 'Generuji vrstevnice' )
		
		# --no-zero-contour
		os.system(
			'phyghtmap \
			--polygon=./poly/' + state.id + '.poly \
			-o ./pbf/' + state.id + '-SRTM \
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
		os.rename( glob.glob( './pbf/' + state.id + '-SRTM*.osm.pbf' )[0], './pbf/' + state.id + '-SRTM.osm.pbf' )


	else:
		print( 'Pouzivam drive vygenerovane vrstevnice' )


	# Vytvorim cilovou podslozku
	if not os.path.exists( './img/' + state.id + '_VasaM' ):
		os.makedirs( './img/' + state.id + '_VasaM' )


	# Generuji Mapsforge
	if mapsforge:
		print( 'NENI HOTOVO' )
	# 	cd "./Mapsforge/bin"
	# 	export JAVACMD_OPTIONS="$JAVAMEM"
		
	# 	# Vlozim vrstevnice do mapy
	# 	# if [ $DOWNLOAD = true ] || [ ! -f ../pbf/$STATE-MERGE.osm.pbf ]; then
	# 	# 	./osmosis --rb file="../../pbf/$STATE.osm.pbf" --sort-0.6 --rb "../../pbf/$STATE-SRTM.osm.pbf" --sort-0.6 --merge --wb "../../pbf/$STATE-MERGE.osm.pbf"
	# 	# fi

	# 	# Generuji mapu
	# 	# ./osmosis --rb file="../../pbf/$STATE-MERGE.osm.pbf" --mapfile-writer file="../../map/$STATE.map" type=hd preferred-languages=en,cs threads=4 tag-conf-file="../tag-mapping.xml"
	# 	# ./osmosis --rb file="../../pbf/$STATE-MERGE.osm.pbf" --mapfile-writer file="../../map/$STATE.map" type=ram preferred-languages=en tag-conf-file="../tag-mapping.xml"
	# 	./osmosis --rb file="../../pbf/$STATE.osm.pbf" --mapfile-writer file="../../map/$STATE.map" type=ram preferred-languages=en,cs,ua tag-conf-file="../tag-mapping.xml"

	# 	cd "./../.."

	# Generuji Garmin
	else:
		# Rozdelim soubory
		input_file = './pbf/' + state.id + '.osm.pbf'
		input_srtm_file = './pbf/' + state.id + '-SRTM.osm.pbf'

		if split:
			for file in glob.glob( './pbf/' + state.id + '-SPLITTED/*' ):
				os.remove(file)

			# max-areas = 512
			# max-nodes = 1600000
			os.system(
				'java ' + JAVAMEM + ' -jar ./splitter/splitter.jar \
				' + input_file + ' \
				--max-areas=4096 \
				--max-nodes=1048576 \
				--output-dir=./pbf/' + state.id + '-SPLITTED \
			')

			input_file = ''
			for file in glob.glob( './pbf/' + state.id + '-SRTM*.osm.pbf' ):
				input_file += file + ' '

			if not os.path.isdir( './pbf/' + state.id + '-SPLITTED-SRTM/' ):
				os.system(
					'java ' + JAVAMEM + ' -jar ./splitter/splitter.jar \
					' + input_srtm_file + ' \
					--max-areas=4096 \
					--max-nodes=1048576 \
					--output-dir=./pbf/' + state.id + '-SPLITTED-SRTM \
				')

				input_srtm_file = ''
				for file in glob.glob( './pbf/' + state.id + '-SPLITTED-SRTM*.osm.pbf' ):
					input_srtm_file += file + ' '

		pois_files = ''
		if state.pois is not None:
			for x in state.pois:
				pois_files += ' ./pois/' + x + '.osm.xml'


		# Vytvorim si docasny soubor s licenci
		copyfile( './template/licence.txt', 'licence.tmp' )
		license = open( 'licence.tmp', 'a' ) 
		license.write( '\nGenerováno: ' )
		# echo "Generováno: "`LC_ALL=cs_CZ.UTF-8 date -r ./pbf/${STATE}.osm.pbf +"%k:%M %d. %B %Y"` >> licence.tmp
		license.write( str( datetime.now() ) )		# FIXME formatovat
		license.close()

		# Spustim generator
		inputs = input_file + ' ' + input_srtm_file + ' ' + pois_files
		os.system(
			'java $JAVAMEM -jar ./mkgmap/mkgmap.jar \
			-c ./mkgmap-settings.conf \
			--mapname="' + str( state.number ) + '0001\" \
			--overview-mapnumber="' + str( state.number ) + '0000\" \
			--family-id="' + str( state.number ) + '" \
			--description="' + state.name + '_VasaM" \
			--family-name="' + state.name + '_VasaM" \
			--series-name="' + state.name + '_VasaM" \
			--area-name="' + state.name + '_VasaM" \
			--country-name="' + state.name + '_VasaM" \
			--country-abbr="' + state.id + '" \
			--region-name="' + state.name + '_VasaM" \
			--region-abbr="' + state.id + '" \
			--product-version=$VERSION \
			--output-dir=./img/' + state.id + '_VasaM \
			--dem-poly=./poly/' + state.id + '.poly \
			--license-file=./licence.tmp \
			' + input_file + ' \
			' + input_srtm_file + ' \
			' + str(pois_files) + ' \
			./garmin-style/style.txt \
		')

		os.remove( 'licence.tmp' )


		# Prevedu ID do hexa tvaru
		state.number_hex = format( state.number, 'x' )
		state.number_hex = state.number_hex[2:4] + state.number_hex[0:2]


		# Vytvorim instalacni bat soubor
		install = open( './template/install.bat', 'r' )
		content = install.read()
		install.close()

		content = content.replace( '%NAME%', state.name )
		content = content.replace( '%ID%', str( state.number ) )
		content = content.replace( '%ID_HEX%', state.number_hex )

		install = open( './img/' + state.id + '_VasaM/install.bat', 'w' )
		install.write( content )
		install.close()


		# Vytvorim odinstalacni bat soubor
		uninstall = open( './template/uninstall.bat', 'r' )
		content = uninstall.read()
		uninstall.close()

		content = content.replace( '%NAME%', state.name )
		content = content.replace( '%ID%', str( state.number ) )

		uninstall = open( './img/' + state.id + '_VasaM/uninstall.bat', 'w' )
		uninstall.write( content )
		uninstall.close()


		# Prejmenuji vystupni soubor
		os.rename( './img/' + state.id + '_VasaM/gmapsupp.img', './img/' + state.id + '_VasaM.img' )

		# Vytvorim archiv
		os.chdir( './img/' )
		zip = zipfile.ZipFile( './' + state.id + '_VasaM.zip', 'w' )
		for dirname, subdirs, files in os.walk( './' + state.id + '_VasaM/' ):
			zip.write( dirname )
			for filename in files:
				zip.write( os.path.join( dirname, filename ) )
		zip.close()
		os.chdir( '..' )


		# Vytvorim info soubor
		info = open( './template/info.info', 'r' )
		content = info.read()
		info.close()


		# Spocitam hashe
		def sha1( filename ):
			hash_func = hashlib.sha1()
		
			with open( filename, 'rb') as f:
				while True:
					data = f.read( 67108864 )  # read 64Mb of file
					if not data:
						break
					hash_func.update( data )

			return hash_func.hexdigest()


		hash_zip = sha1( './img/' + state.id + '_VasaM.zip' )
		hash_img = sha1( './img/' + state.id + '_VasaM.img' )
		map_timestamp = round( time_start.timestamp() )
		
		content = content.replace( '%VERSION%', str( VERSION ) )
		content = content.replace( '%TIMESTAMP%', str( map_timestamp ) )
		content = content.replace( '%HASH_IMG%', hash_img )
		content = content.replace( '%HASH_ZIP%', hash_zip )

		info = open( './img/' + state.id + '_VasaM.info', 'w' )
		info.write( content )
		info.close()


		# Konec
		end( time_start )


if __name__ == "__main__":
	main()