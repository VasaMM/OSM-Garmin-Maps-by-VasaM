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



def contours(o):
	try:
		# Zjistim, zda mam hotove vrstevnice
		if not os.path.isfile(o.pbf + o.state.data_id + '-SRTM.osm.pbf'):
			say('Generate contour line', o)

			err = subprocess.run([
				'phyghtmap',
				'--polygon=' + o.polygons + o.state.data_id + '.poly',
				'-o', o.pbf +  o.state.data_id + '-SRTM',
				'--pbf',
				'-j', '2',
				'-s', '10',
				'-c', '200,100',
				'--hgtdir=' + o.hgt,
				'--source=view3',
				'--start-node-id=20000000000',
				'--start-way-id=10000000000',
				'--write-timestamp',
				'--max-nodes-per-tile=0'
			], shell=True, capture_output=True)
			log(err.stdout.decode(), o)

			if err.returncode != 0:
				error(err.stderr.decode(), o)
				raise ValueError('phyghtmap return ' + str(err.returncode) + ' (0 expected)')

			os.rename(glob.glob(o.pbf + o.state.data_id + '-SRTM*.osm.pbf')[0], o.pbf + o.state.data_id + '-SRTM.osm.pbf')

		else:
			say('Use previously generated contour lines', o)
	except:
		if os.path.isfile(glob.glob(o.pbf + o.state.data_id + '-SRTM*.osm.pbf')[0]):
			os.remove(glob.glob(o.pbf + o.state.data_id + '-SRTM*.osm.pbf')[0])

		# TODO remove files
		error("Cann't generate contour lines!", o)
		raise


def _prepareLicence(o):
	# Vytvorim licencni soubor
	say('Prepare license file', o)
	with open( './template/license.txt', 'r' ) as license:
		content = license.read()

	with open( o.temp + 'license.txt', 'w' ) as license:
		license.write( content + "\n" + str(o.state.timestamp))



def _splitFiles(o):
	input_file = o.pbf + o.state.data_id + '.osm.pbf'
	input_srtm_file = o.pbf + o.state.data_id + '-SRTM.osm.pbf'

	if o.split:
		say('Split files start',o)
		# Data neexistuji nebo jsem stahl nova
		if not os.path.exists( o.pbf + o.state.data_id + '-SPLITTED' ) or o.downloaded:
			# Smazu puvodni soubory
			for file in glob.glob( o.pbf + o.state.data_id + '-SPLITTED/*' ):
				os.remove(file)

			# Spustim splitter
			err = subprocess.run([
				'java', o.JAVAMEM,
				'-jar', './splitter-r' + str(o.splitter) + '/splitter.jar',
				input_file,
				'--max-areas=4096',
				'--max-nodes=1600000',
				'--output-dir=' + o.pbf + o.state.data_id + '-SPLITTED'
			], shell=True, capture_output=True)
			log(err.stdout.decode(), o)
			
			if err.returncode != 0:
				error(err.stderr.decode(), o)
				raise ValueError('splitter return ' + str(err.returncode) + ' on map data (0 expected)')


		# Aktualizuji seznam vstupnich souboru
		input_file = []
		for file in glob.glob( o.pbf + o.state.data_id + '-SPLITTED/*.osm.pbf' ):
			input_file.append(file)

		# Rozdelim soubor s vrstevnicemi
		if not os.path.isdir( o.pbf + o.state.data_id + '-SPLITTED-SRTM/' ):
			err = subprocess.run([
				'java', o.JAVAMEM,
				'-jar', './splitter-r' + str(o.splitter) + '/splitter.jar',
				input_srtm_file,
				'--max-areas=4096',
				'--max-nodes=1600000',
				'--output-dir=' + o.pbf + o.state.data_id + '-SPLITTED-SRTM'
			], shell=True, capture_output=True)
			log(err.stdout.decode(), o)

			if err.returncode != 0:
				error(err.stderr.decode(), o)
				raise ValueError('splitter return ' + str(err.returncode) + ' on srtm data (0 expected)')

		# Aktualizuji seznam vstupnich souboru
		input_srtm_file = []
		for file in glob.glob( o.pbf + o.state.data_id + '-SPLITTED-SRTM/*.osm.pbf' ):
			input_srtm_file.append(file)

	return input_file, input_srtm_file


def _makeBat(name, o):
	say('Make install.bat file', o)

	if name not in ['install', 'uninstall']:
		raise ValueError('Invalid bat file name')

	# Prevedu ID do hexa tvaru
	numberHex = format( o.state.number, 'x' )
	numberHex = numberHex[2:4] + numberHex[0:2]


	# Vytvorim instalacni bat soubor
	with open( './template/' + name + '.bat', 'r' ) as batFile:
		content = batFile.read()

	content = content.replace( '%NAME%', o.state.name )
	content = content.replace( '%ID%', str( o.state.number ) )
	content = content.replace( '%ID_HEX%', numberHex )

	with open( o.img + o.state.id + '_VasaM/' + name + '.bat', 'w' ) as batFile:
		batFile.write( content )


def _makeZip(o):
	say('Make zip file', o)

	os.chdir( o.img )
	zip = zipfile.ZipFile( './' + o.state.id + '_VasaM.zip', 'w' )
	for dirname, subdirs, files in os.walk( './' + o.state.id + '_VasaM/' ):
		zip.write( dirname )
		for filename in files:
			zip.write( os.path.join( dirname, filename ) )
	zip.close()
	os.chdir( '..' )



def _makeInfo(o):
	say('Make info file', o)

	infoData = {
		'version': str(o.VERSION),
		'timestamp':     str(o.state.timestamp),
		'hashImg':       _sha1( o.img + o.state.id + '_VasaM.img' ),
		'hashZip':       _sha1( o.img + o.state.id + '_VasaM.zip' ),
		'codePage':      o.code
	}

	with open( o.img + o.state.id + '_VasaM.info', 'w' ) as info:
		info.write(json.dumps(infoData))


def garmin(o):
	say( 'Making map for garmin...', o )


	# Vytvorim cilovou podslozku
	if not os.path.exists(o.img + o.state.id + '_VasaM'):
		os.makedirs(o.img + o.state.id + '_VasaM')


	input_file, input_srtm_file = _splitFiles(o)

	_prepareLicence(o)


	say('Generating map', o)
	# FIXME najit chybu
	"""
	mkgmap = [
		'java', o.JAVAMEM,
		'-jar', './mkgmap-r' + str(o.mkgmap) + '/mkgmap.jar',
		'-c', './garmin-style/mkgmap-settings.conf',
		'--bounds=' + o.bounds,
		'--precomp-sea=' + o.sea +'sea/',
		'--dem=' + o.hgt +'VIEW3/',
		'--max-jobs=' + str( o.MAX_JOBS ),
		'--mapname="' + str( o.state.number ) + '0001\"',
		'--overview-mapnumber="' + str( o.state.number ) + '0000\"',
		'--family-id="' + str( o.state.number ) + '"',
		'--description="' + o.state.name + '_VasaM"',
		'--family-name="' + o.state.name + '_VasaM"',
		'--series-name="' + o.state.name + '_VasaM"',
		'--area-name="' + o.state.name + '_VasaM"',
		'--country-name="' + o.state.name + '_VasaM"',
		'--country-abbr="' + o.state.id + '"',
		'--region-name="' + o.state.name + '_VasaM"',
		'--region-abbr="' + o.state.id + '"',
		'--product-version=' + str( o.VERSION ),
		'--output-dir=' + o.img + o.state.id + '_VasaM',
		'--dem-poly=' + o.polygons + o.state.data_id + '.poly',
		'--license-file=license.txt',
		'--code-page=' + o.code,
	] + input_file + input_srtm_file + o.state.pois + ['./garmin-style/style.txt']
	"""
	mkgmap = 'java ' + o.JAVAMEM + ' -jar ./mkgmap-r' + str(o.mkgmap) + '/mkgmap.jar \
		-c ./garmin-style/mkgmap-settings.conf \
		--bounds=' + o.bounds + ' \
		--precomp-sea=' + o.sea + 'sea/ \
		--dem=' + o.hgt +'VIEW3/ \
		--max-jobs=' + str( o.MAX_JOBS ) + ' \
		--mapname="' + str( o.state.number ) + '0001\" \
		--overview-mapnumber="' + str( o.state.number ) + '0000\" \
		--family-id="' + str( o.state.number ) + '" \
		--description="' + o.state.name + '_VasaM" \
		--family-name="' + o.state.name + '_VasaM" \
		--series-name="' + o.state.name + '_VasaM" \
		--area-name="' + o.state.name + '_VasaM" \
		--country-name="' + o.state.name + '_VasaM" \
		--country-abbr="' + o.state.id + '" \
		--region-name="' + o.state.name + '_VasaM" \
		--region-abbr="' + o.state.id + '" \
		--product-version=' + str( o.VERSION ) + ' \
		--output-dir=' + o.img + o.state.id + '_VasaM \
		--dem-poly=' + o.polygons + o.state.data_id + '.poly \
		--license-file=' + o.temp + 'license.txt \
		--code-page=' + o.code + ' \
		' + ' '.join(input_file) + ' \
		' + ' '.join(input_srtm_file) + ' \
		' + ' '.join(o.state.pois) + ' \
		./garmin-style/style.txt'

	err = subprocess.run(mkgmap, shell=True, capture_output=True)
	log(err.stdout.decode(), o)


	if err.returncode != 0:
		error(err.stderr.decode(), o)
		raise ValueError('mkgmap return ' + str(err.returncode) + ' (0 expected)')


	_makeBat('install', o)
	_makeBat('uninstall', o)



	# Prejmenuji vystupni soubor
	say('Rename files', o)
	if os.path.isfile( o.img + o.state.id + '_VasaM.img' ):
		os.remove( o.img + o.state.id + '_VasaM.img' )

	os.rename( o.img + o.state.id + '_VasaM/gmapsupp.img', o.img + o.state.id + '_VasaM.img' )


	_makeZip(o)
	_makeInfo(o)
