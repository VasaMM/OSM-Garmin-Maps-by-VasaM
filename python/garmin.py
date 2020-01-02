import os, glob, zipfile, hashlib
from datetime import datetime

from python.print import say


def make_garmin( o ):
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
	license.write( content + "\n" + str( datetime.now() ) )
	license.close()


	# Spustim generator
	# inputs = input_file + ' ' + input_srtm_file + ' ' + pois_files
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
		' + state.lang + ' \
		' + state.code + ' \
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
	map_timestamp = round( o.time_start.timestamp() )
	
	content = content.replace( '%VERSION%', str( o.VERSION ) )
	content = content.replace( '%TIMESTAMP%', str( map_timestamp ) )
	content = content.replace( '%HASH_IMG%', hash_img )
	content = content.replace( '%HASH_ZIP%', hash_zip )

	info = open( './img/' + state.id + '_VasaM.info', 'w' )
	info.write( content )
	info.close()