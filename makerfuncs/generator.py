import os, sys, glob, zipfile, hashlib, json
import subprocess

from datetime import datetime
from makerfuncs.prints import say, error, log
import osmium


def _sha1(filename):
	hash_func = hashlib.sha1()

	with open(filename, 'rb') as f:
		while True:
			data = f.read(67108864)  # read 64Mb of file
			if not data:
				break
			hash_func.update(data)

	return hash_func.hexdigest()


def _run(program, o):
	program = ' '.join(program.split())
	say(program, o, '[RUN] ')
	process = subprocess.Popen(program, universal_newlines = True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	while True:
		output = process.stdout.readline()

		if output == '' and process.poll() is not None:
			break;
		if output:
			say(output, o, '', '')
			log(output, o)

	if process.poll() != 0:
		error('stderr: ' + process.stderr.read(), o)
		raise ValueError(program + ' return ' + str(process.poll()) + ' (0 expected)')


def contours(o):
	say('Generuji vrstevnice', o)
	# try:
	# Zjistim, zda mam hotove vrstevnice
	if not os.path.isfile(o.pbf + o.area.id + '-SRTM.osm.pbf'):
		say('Generate contour line', o)
		_run('phyghtmap \
			--polygon=' + o.temp + 'polygon.poly \
			-o ' + o.pbf + o.area.id + '-SRTM \
			--pbf \
			-j 2 \
			-s 10 \
			-c 200,100 \
			--hgtdir=' + o.hgt +' \
			--source=view3 \
			--start-node-id=20000000000 \
			--start-way-id=10000000000 \
			--write-timestamp \
			--max-nodes-per-tile=0'
		, o)

		os.rename(glob.glob(o.pbf + o.area.id + '-SRTM*.osm.pbf')[0], o.pbf + o.area.id + '-SRTM.osm.pbf')

	else:
		say('Use previously generated contour lines', o)
	# except:
	# 	if os.path.isfile(glob.glob(o.pbf + o.area.id + '-SRTM*.osm.pbf')[0]):
	# 		os.remove(glob.glob(o.pbf + o.area.id + '-SRTM*.osm.pbf')[0])

	# 	error("Cann't generate contour lines!", o)
	# 	raise


def crop(o):
	# FIXME
	if o.crop or o.area.crop:
		say('Vytvarim vyrez oblasti', o)

		os.chdir( 'osmconvert' )
		_run('osmconvert64-0.8.8p.exe \
			../' + o.area.mapDataName + 
			' -B=../' + o.temp + 'polygon.poly \
			--complete-ways --complete-multipolygons --complete-boundaries \
			--out-pbf \
			-o=../' + o.temp + o.area.id + '.osm.pbf'
		, o)
		os.chdir( '..' )

		o.area.mapDataName = o.temp + o.area.id + '.osm.pbf'

	# mapsplit europe.osm.pbf /tmp/output -p=country.poly
	# osmconvert europe.osm.pbf -B=country.poly -o=switzerland.o5m

	# https://bretth.dev.openstreetmap.org/osmosis-build/osmosis-latest.zip
	# osmosis --read-xml file="planet-latest.osm" --bounding-polygon file="country.poly" --write-xml file="australia.osm"
	# osmosis --read-pbf file="planet-latest.osm" --bounding-polygon file="country.poly" --write-pbf file="australia.osm"



def _prepareLicence(o):
	# Vytvorim licencni soubor
	say('Prepare license file', o)
	with open( './template/license.txt', 'r' ) as license:
		content = license.read()

	with open( o.temp + 'license.txt', 'w' ) as license:
		license.write( content + "\n" + str(o.area.timestamp))



def _splitFiles(o):
	input_file = o.area.mapDataName
	input_srtm_file = o.pbf + o.area.id + '-SRTM.osm.pbf'

	if o.split:
		say('Split files start',o)
		# Data neexistuji nebo jsem stahl nova
		if not os.path.exists( o.pbf + o.area.id + '-SPLITTED' ) or o.downloaded:
			# Smazu puvodni soubory
			for file in glob.glob( o.pbf + o.area.id + '-SPLITTED/*' ):
				os.remove(file)

			# Spustim splitter
			_run('java ' + o.JAVAMEM + ' -jar \
				./splitter-r' + str(o.splitter) + '/splitter.jar ' + 
				input_file +
				' --max-areas=4096 \
				--max-nodes=1600000 \
				--output-dir=' + o.pbf + o.area.id + '-SPLITTED'
			, o)

		# Aktualizuji seznam vstupnich souboru
		input_file = o.pbf + o.area.id + '-SPLITTED/*.osm.pbf'
		# input_file = []
		# for file in glob.glob( o.pbf + o.area.id + '-SPLITTED/*.osm.pbf' ):
		# 	input_file.append(file)

		# Rozdelim soubor s vrstevnicemi
		if not os.path.isdir( o.pbf + o.area.id + '-SPLITTED-SRTM' ):
			_run('java ' + o.JAVAMEM + ' -jar \
				./splitter-r' + str(o.splitter) + '/splitter.jar ' + 
				input_srtm_file +
				' --max-areas=4096 \
				--max-nodes=1600000 \
				--output-dir=' + o.pbf + o.area.id + '-SPLITTED-SRTM'
			, o)

		say('Split files DONE',o)


		# Aktualizuji seznam vstupnich souboru
		input_srtm_file = o.pbf + o.area.id + '-SPLITTED-SRTM/*.osm.pbf'
		# input_srtm_file = []
		# for file in glob.glob( o.pbf + o.area.id + '-SPLITTED-SRTM/*.osm.pbf' ):
		# 	input_srtm_file.append(file)

	return input_file, input_srtm_file


def _makeBat(name, o):
	say('Make ' + name + '.bat file', o)

	if name not in ['install', 'uninstall']:
		raise ValueError('Invalid bat file name')

	# Prevedu ID do hexa tvaru
	numberHex = format( o.area.number, 'x' )
	numberHex = numberHex[2:4] + numberHex[0:2]


	# Vytvorim instalacni bat soubor
	with open( './template/' + name + '.bat', 'r' ) as batFile:
		content = batFile.read()

	content = content.replace( '%NAME%', o.area.nameCs )
	content = content.replace( '%ID%', str(o.area.number).zfill(4) )
	content = content.replace( '%ID_HEX%', numberHex )

	with open( o.img + o.area.id + o.sufix + '/' + name + '.bat', 'w' ) as batFile:
		batFile.write( content )


def _makeZip(o):
	say('Make zip file', o)

	os.chdir( o.img )
	zip = zipfile.ZipFile( './' + o.area.id + o.sufix + '.zip', 'w' )
	for dirname, subdirs, files in os.walk( './' + o.area.id + o.sufix ):
		zip.write( dirname )
		for filename in files:
			zip.write( os.path.join( dirname, filename ) )
	zip.close()
	os.chdir( '..' )



def _makeInfo(o):
	say('Make info file', o)

	infoData = {
		'version':   str(o.VERSION),
		'datetime':  str(o.area.timestamp),
		'timestamp': str(o.area.timestamp.timestamp()),
		'hashImg':   _sha1( o.img + o.area.id + o.sufix + '.img' ),
		'hashZip':   _sha1( o.img + o.area.id + o.sufix + '.zip' ),
		'codePage':  o.code
	}

	with open( o.img + o.area.id + o.sufix + '.info', 'w' ) as info:
		info.write(json.dumps(infoData))


def garmin(o):
	say( 'Making map for garmin...', o )


	# Vytvorim cilovou podslozku
	if not os.path.exists(o.img + o.area.id + o.sufix):
		os.makedirs(o.img + o.area.id + o.sufix)


	input_file, input_srtm_file = _splitFiles(o)

	_prepareLicence(o)


	say('Generating map', o)
	# FIXME najit chybu
		# -c ' + o.temp + 'mkgmap-settings.conf \
	_run('java ' + o.JAVAMEM + ' -jar ./mkgmap-r' + str(o.mkgmap) + '/mkgmap.jar \
		-c ./garmin-style/mkgmap-settings.conf \
		--bounds=' + o.bounds + ' \
		--precomp-sea=' + o.sea + 'sea/ \
		--dem=' + o.hgt +'VIEW3/ \
		--max-jobs=' + str( o.MAX_JOBS ) + ' \
		--mapname="' + str(o.area.number).zfill(4) + '0001\" \
		--overview-mapnumber="' + str(o.area.number).zfill(4) + '0000\" \
		--family-id="' + str(o.area.number).zfill(4) + '" \
		--description="' + o.area.nameCs + o.sufix + '" \
		--family-name="' + o.area.nameCs + o.sufix + '" \
		--series-name="' + o.area.nameCs + o.sufix + '" \
		--area-name="' + o.area.nameCs + o.sufix + '" \
		--country-name="' + o.area.nameCs + o.sufix + '" \
		--country-abbr="' + o.area.id + '" \
		--region-name="' + o.area.nameCs + o.sufix + '" \
		--region-abbr="' + o.area.id + '" \
		--product-version=' + str( o.VERSION ) + ' \
		--output-dir=' + o.img + o.area.id + o.sufix + ' \
		--dem-poly=' + o.polygons + o.area.id + '.poly \
		--license-file=' + o.temp + 'license.txt \
		--code-page=' + o.code + ' \
		' + input_file + ' \
		' + input_srtm_file + ' \
		' + ' '.join(o.area.pois) + ' \
		./garmin-style/style.txt'
	, o)

	# mkgmap = 'java ' + o.JAVAMEM + ' -jar ./mkgmap-r' + str(o.mkgmap) + '/mkgmap.jar \
	# 	-c ./garmin-style/mkgmap-settings.conf \
	# 	--bounds=' + o.bounds + ' \
	# 	--precomp-sea=' + o.sea + 'sea/ \
	# 	--dem=' + o.hgt +'VIEW3/ \
	# 	--max-jobs=' + str( o.MAX_JOBS ) + ' \
	# 	--mapname="' + str(o.area.number).zfill(4) + '0001\" \
	# 	--overview-mapnumber="' + str(o.area.number).zfill(4) + '0000\" \
	# 	--family-id="' + str(o.area.number).zfill(4) + '" \
	# 	--description="' + o.area.nameCs + o.sufix + '" \
	# 	--family-name="' + o.area.nameCs + o.sufix + '" \
	# 	--series-name="' + o.area.nameCs + o.sufix + '" \
	# 	--area-name="' + o.area.nameCs + o.sufix + '" \
	# 	--country-name="' + o.area.nameCs + o.sufix + '" \
	# 	--country-abbr="' + o.area.id + '" \
	# 	--region-name="' + o.area.nameCs + o.sufix + '" \
	# 	--region-abbr="' + o.area.id + '" \
	# 	--product-version=' + str( o.VERSION ) + ' \
	# 	--output-dir=' + o.img + o.area.id + o.sufix + ' \
	# 	--dem-poly=' + o.polygons + o.area.id + '.poly \
	# 	--license-file=' + o.temp + 'license.txt \
	# 	--code-page=' + o.code + ' \
	# 	' + ' '.join(input_file) + ' \
	# 	' + ' '.join(input_srtm_file) + ' \
	# 	' + ' '.join(o.area.pois) + ' \
	# 	./garmin-style/style.txt'

	# _run(o, mkgmap)

	# FIXME
	# err = subprocess.run(mkgmap, shell=True, capture_output=False)
	# log(err.stdout.decode(), o)

	# if err.returncode != 0:
	# 	error(err.stderr.decode(), o)
	# 	raise ValueError(program + ' return ' + str(err.returncode) + ' (0 expected)')


	_makeBat('install', o)
	_makeBat('uninstall', o)


	# Prejmenuji vystupni soubor
	say('Rename files', o)
	if os.path.isfile( o.img + o.area.id + o.sufix + '.img' ):
		os.remove( o.img + o.area.id + o.sufix + '.img' )

	os.rename( o.img + o.area.id + o.sufix + '/gmapsupp.img', o.img + o.area.id + o.sufix + '.img' )


	_makeZip(o)
	_makeInfo(o)
