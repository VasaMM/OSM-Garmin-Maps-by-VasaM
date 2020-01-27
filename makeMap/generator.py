import os, glob, zipfile, hashlib, json
from datetime import datetime
from makeMap.prints import say, error
import osmium


def contours(o):
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



def garmin( o ):
	say( 'Making map for garmin...', o )
	state = o.state

	# Rozdelim soubory
	input_file = './pbf/' + state.data_id + '.osm.pbf'
	input_srtm_file = './pbf/' + state.data_id + '-SRTM.osm.pbf'

	if o.split:
		if not os.path.exists( './pbf/' + state.data_id + '-SPLITTED' ) or o.download_map:
			for file in glob.glob( './pbf/' + state.data_id + '-SPLITTED/*' ):
				os.remove(file)

			# max-areas = 512
			# max-nodes = 1600000
			os.system(
				'java ' + o.JAVAMEM + ' -jar ./splitter/splitter.jar \
				' + input_file + ' \
				--max-areas=4096 \
				--max-nodes=1600000 \
				--output-dir=./pbf/' + state.data_id + '-SPLITTED \
			')


		input_file = ''
		for file in glob.glob( './pbf/' + state.data_id + '-SPLITTED/*.osm.pbf' ):
			input_file += file + ' '

		if not os.path.isdir( './pbf/' + state.data_id + '-SPLITTED-SRTM/' ):
			os.system(
				'java ' + o.JAVAMEM + ' -jar ./splitter/splitter.jar \
				' + input_srtm_file + ' \
				--max-areas=4096 \
				--max-nodes=1600000 \
				--output-dir=./pbf/' + state.data_id + '-SPLITTED-SRTM \
			')

		input_srtm_file = ''
		for file in glob.glob( './pbf/' + state.data_id + '-SPLITTED-SRTM/*.osm.pbf' ):
			input_srtm_file += file + ' '

	pois_files = ''
	if state.pois is not None:
		for x in state.pois:
			pois_files += ' ./pois/' + x + '.osm.xml'


	# Vytvorim licencni soubor
	license = open( './template/license.txt', 'r' )
	content = license.read()
	license.close()

	license = open( 'license.txt', 'w' )
	license.write( content + "\n" + o.state.timestamp)
	license.close()


	# Spustim generator
	# ' + state.lang + ' \
		
	err = os.system(
		'java ' + o.JAVAMEM + ' -jar ./mkgmap/mkgmap.jar \
		-c mkgmap-settings.conf \
		--check-roundabouts \
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
		--output-dir=./img/' + state.id + '_VasaM \
		--dem-poly=./poly/' + state.data_id + '.poly \
		--license-file=license.txt \
		--code-page=' + o.code + ' \
		' + input_file + ' \
		' + input_srtm_file + ' \
		' + pois_files + ' \
		./garmin-style/style.txt \
	')

	if err != 0:
		sys.stderr.write( 'mkgmap error' )
		sys.exit()

	os.remove( 'license.txt' )


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
	if os.path.isfile( './img/' + state.id + '_VasaM.img' ):
		os.remove( './img/' + state.id + '_VasaM.img' )

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


	# Vytvorim info soubor
	infoData = {
		'version': str(o.VERSION),
		'timestamp':     o.state.timestamp,
		'hashImg':       sha1( './img/' + state.id + '_VasaM.img' ),
		'hashZip':       sha1( './img/' + state.id + '_VasaM.zip' ),
		'codePage':      o.code
	}

	info = open( './img/' + state.id + '_VasaM.info', 'w' )
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