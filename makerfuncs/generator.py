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



def garmin(o):
	say( 'Making map for garmin...', o )
	state = o.state


	# Vytvorim cilovou podslozku
	if not os.path.exists(o.img + o.state.id + '_VasaM'):
		os.makedirs(o.img + o.state.id + '_VasaM')


	# Rozdelim soubory
	input_file = o.pbf + state.data_id + '.osm.pbf'
	input_srtm_file = o.pbf + state.data_id + '-SRTM.osm.pbf'

	if o.split:
		say('Split files start',o)
		# Data neexistuji nebo jsem stahl nova
		if not os.path.exists( o.pbf + state.data_id + '-SPLITTED' ) or o.downloaded:
			# SMazu puvodni soubory
			for file in glob.glob( o.pbf + state.data_id + '-SPLITTED/*' ):
				os.remove(file)

			# Spustim splitter
			err = subprocess.run([
				'java', o.JAVAMEM,
				'-jar', './splitter-r' + str(o.splitter) + '/splitter.jar',
				input_file,
				'--max-areas=4096',
				'--max-nodes=1600000',
				'--output-dir=' + o.pbf + state.data_id + '-SPLITTED'
			], shell=True, capture_output=True)
			log(err.stdout.decode(), o)
			
			if err.returncode != 0:
				error(err.stderr.decode(), o)
				raise ValueError('splitter return ' + str(err.returncode) + ' on map data (0 expected)')


		# Aktualizuji seznam vstupnich souboru
		input_file = []
		for file in glob.glob( o.pbf + state.data_id + '-SPLITTED/*.osm.pbf' ):
			input_file.append(file)

		# Rozdelim soubor s vrstevnicemi
		if not os.path.isdir( o.pbf + state.data_id + '-SPLITTED-SRTM/' ):
			err = subprocess.run([
				'java', o.JAVAMEM,
				'-jar', './splitter-r' + str(o.splitter) + '/splitter.jar',
				input_srtm_file,
				'--max-areas=4096',
				'--max-nodes=1600000',
				'--output-dir=' + o.pbf + state.data_id + '-SPLITTED-SRTM'
			], shell=True, capture_output=True)
			log(err.stdout.decode(), o)

			if err.returncode != 0:
				error(err.stderr.decode(), o)
				raise ValueError('splitter return ' + str(err.returncode) + ' on srtm data (0 expected)')

		# Aktualizuji seznam vstupnich souboru
		input_srtm_file = []
		for file in glob.glob( o.pbf + state.data_id + '-SPLITTED-SRTM/*.osm.pbf' ):
			input_srtm_file.append(file)


	# Vytvorim licencni soubor
	say('Prepare license file', o)
	license = open( './template/license.txt', 'r' )
	content = license.read()
	license.close()

	license = open( 'license.txt', 'w' )
	license.write( content + "\n" + str(o.state.timestamp))
	license.close()


	# Spustim generator
	# ' + state.lang + ' \
	
	say('Generating map', o)
	# FIXME najit chybu
	# mkgmap = [
	# 	'java', o.JAVAMEM,
	# 	'-jar', './mkgmap-r' + str(o.mkgmap) + '/mkgmap.jar',
	# 	'-c', './garmin-style/mkgmap-settings.conf',
	# 	'--bounds=' + o.bounds,
	# 	'--precomp-sea=' + o.sea +'sea/',
	# 	'--dem=' + o.hgt +'VIEW3/',
	# 	'--max-jobs=' + str( o.MAX_JOBS ),
	# 	'--mapname="' + str( state.number ) + '0001\"',
	# 	'--overview-mapnumber="' + str( state.number ) + '0000\"',
	# 	'--family-id="' + str( state.number ) + '"',
	# 	'--description="' + state.name + '_VasaM"',
	# 	'--family-name="' + state.name + '_VasaM"',
	# 	'--series-name="' + state.name + '_VasaM"',
	# 	'--area-name="' + state.name + '_VasaM"',
	# 	'--country-name="' + state.name + '_VasaM"',
	# 	'--country-abbr="' + state.id + '"',
	# 	'--region-name="' + state.name + '_VasaM"',
	# 	'--region-abbr="' + state.id + '"',
	# 	'--product-version=' + str( o.VERSION ),
	# 	'--output-dir=' + o.img + state.id + '_VasaM',
	# 	'--dem-poly=' + o.polygons + state.data_id + '.poly',
	# 	'--license-file=license.txt',
	# 	'--code-page=' + o.code,
	# ] + input_file + input_srtm_file + state.pois + ['./garmin-style/style.txt']

	mkgmap = 'java ' + o.JAVAMEM + ' -jar ./mkgmap-r' + str(o.mkgmap) + '/mkgmap.jar \
		-c ./garmin-style/mkgmap-settings.conf \
		--bounds=' + o.bounds + ' \
		--precomp-sea=' + o.sea + 'sea/ \
		--dem=' + o.hgt +'VIEW3/ \
		--max-jobs=' + str( o.MAX_JOBS ) + ' \
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
		--product-version=' + str( o.VERSION ) + ' \
		--output-dir=' + o.img + state.id + '_VasaM \
		--dem-poly=' + o.polygons + state.data_id + '.poly \
		--license-file=license.txt \
		--code-page=' + o.code + ' \
		' + ' '.join(input_file) + ' \
		' + ' '.join(input_srtm_file) + ' \
		' + ' '.join(state.pois) + ' \
		./garmin-style/style.txt'

	err = subprocess.run(mkgmap, shell=True, capture_output=True)
	log(err.stdout.decode(), o)

	os.remove( 'license.txt' )

	if err.returncode != 0:
		error(err.stderr.decode(), o)
		raise ValueError('mkgmap return ' + str(err.returncode) + ' (0 expected)')


	# Prevedu ID do hexa tvaru
	state.number_hex = format( state.number, 'x' )
	state.number_hex = state.number_hex[2:4] + state.number_hex[0:2]


	# Vytvorim instalacni bat soubor
	say('Make install.bat file', o)
	install = open( './template/install.bat', 'r' )
	content = install.read()
	install.close()

	content = content.replace( '%NAME%', state.name )
	content = content.replace( '%ID%', str( state.number ) )
	content = content.replace( '%ID_HEX%', state.number_hex )

	install = open( o.img + state.id + '_VasaM/install.bat', 'w' )
	install.write( content )
	install.close()


	# Vytvorim odinstalacni bat soubor
	say('Make uninstall.bat file', o)
	uninstall = open( './template/uninstall.bat', 'r' )
	content = uninstall.read()
	uninstall.close()

	content = content.replace( '%NAME%', state.name )
	content = content.replace( '%ID%', str( state.number ) )

	uninstall = open( o.img + state.id + '_VasaM/uninstall.bat', 'w' )
	uninstall.write( content )
	uninstall.close()


	# Prejmenuji vystupni soubor
	say('Rename files', o)
	if os.path.isfile( o.img + state.id + '_VasaM.img' ):
		os.remove( o.img + state.id + '_VasaM.img' )

	os.rename( o.img + state.id + '_VasaM/gmapsupp.img', o.img + state.id + '_VasaM.img' )


	# Vytvorim archiv
	say('Make zip file', o)
	os.chdir( o.img )
	zip = zipfile.ZipFile( './' + state.id + '_VasaM.zip', 'w' )
	for dirname, subdirs, files in os.walk( './' + state.id + '_VasaM/' ):
		zip.write( dirname )
		for filename in files:
			zip.write( os.path.join( dirname, filename ) )
	zip.close()
	os.chdir( '..' )


	# Vytvorim info soubor
	say('Make info file', o)
	infoData = {
		'version': str(o.VERSION),
		'timestamp':     str(o.state.timestamp),
		'hashImg':       _sha1( o.img + state.id + '_VasaM.img' ),
		'hashZip':       _sha1( o.img + state.id + '_VasaM.zip' ),
		'codePage':      o.code
	}

	info = open( o.img + state.id + '_VasaM.info', 'w' )
	info.write(json.dumps(infoData))
	info.close()








# def mapsforge( o ):
# 	print( 'NENI HOTOVO' )
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