# SRTM:
# http://builder.osmand.net/terrain-aster-srtm-eudem/
# http://rmd.neoknet.com/srtm3/

import os
import sys
import re
import urllib.request
import zipfile

if ( len( sys.argv ) != 3 ):
	print( 'Spatny pocet argumentu. Pouzijte ve tvrau poly-downloader.py <tif-dir> <hgt-dir>' )
	exit()

# Opravim vystupni adresar
inputDir = sys.argv[1]
if( inputDir[-1] != '/' ):
	inputDir = inputDir + '/'

outputDir = sys.argv[2]
if( outputDir[-1] != '/' ):
	outputDir = outputDir + '/'


# Ctu postupne nazvy suboru
for file in os.listdir( inputDir ):
	# Ziskam nazev souboru
	fileName = re.search('([NS]\d{2}[EW]\d{3})\.tif', file)

	if ( fileName == None ):
		continue

	fileName = fileName.group( 1 )


	# Pokud soubor neexistuje, pokusim se ho stahnout
	if ( not os.path.isfile( outputDir + fileName + '.hgt' ) ):
		print ( '\r' + fileName + ': Stahuji hgt', end = '' )
		sys.stdout.flush()

		try:
			# urllib.request.urlretrieve( 'http://rmd.neoknet.com/srtm3/' + fileName + '.hgt.zip', outputDir + fileName + '.zip' )
			urllib.request.urlretrieve( 'http://firmware.ardupilot.org/SRTM/Eurasia/' + fileName + '.hgt.zip', outputDir + fileName + '.zip' )
		
		except Exception:
		    continue

		print ( '\r' + fileName + ': Rozbaluji  ', end = '' )
		sys.stdout.flush()

		zipRef = zipfile.ZipFile( outputDir + fileName + '.zip', 'r')
		zipRef.extractall( outputDir )
		zipRef.close()
		os.remove( outputDir + fileName + '.zip' )

	# if ( not os.path.isfile( outputDir + 'SRTM3v3.0/' + fileName + '.tif' ) ):
		# print ( '\r' + fileName + ': Stahuji tif', end = '' )
		# sys.stdout.flush()

		# urllib.request.urlretrieve( 'http://builder.osmand.net/terrain-aster-srtm-eudem/' + fileName + '.tif', outputDir + 'SRTM3v3.0/' + fileName + '.tif' )
		
	print ( '\r' + fileName + ': Stazeno    ', end = '' )
	# print ( '\r' + fileName + ': Stazeno    ' )
	sys.stdout.flush()

print ( '\rVsechny hgt soubory stazeny' )
