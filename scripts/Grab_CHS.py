# Skript postupne projde vsechny lezecke oblasti na strankach CHS
# Ke kazde skale stahne jeji GPS souradnice, jmeno a dalsi atributy
# https://github.com/rory/openstreetmap-writer

import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from osmwriter import OSMWriter


xml = OSMWriter( "chs.osm.xml" )

# Pocet sklanich oblasti
rockCount = 17220

for i in range( 1, rockCount + 1 ):

	try:
		page = urlopen( 'https://www.horosvaz.cz/skaly-skala-' + str( i ) )
	except:
		print( i, ':', sep='' )
		continue

	# Rozdelim html
	soup = BeautifulSoup( page, 'html.parser' )

	# Ziskam jmeno
	name_box = soup.find( 'h1', attrs={ 'class': 'menu5 small-h1' } )
	name = name_box.text.strip()

	# Ziskma souradnice
	coordinates_box = soup.find( 'a', attrs={ 'class': 'map mapycz' } )
	if ( coordinates_box == None ):
		print( i, ':  ', name, sep='' )
		continue
	
	coordinates = coordinates_box.attrs[ 'href' ]
	m = re.search( 'y=([0-9]+.[0-9]+)&x=([0-9]+.[0-9]+)', coordinates )
	coordinates = ( m.group( 1 ), m.group( 2 ) )


	# Vytisknu vysledek a pridam ho do vystupniho souboru
	print( i, ':  ', name, '  (N ', coordinates[0], ' E ', coordinates[1], ')', sep='' )
	xml.node(  10000000000 +  i, coordinates[0], coordinates[1], { 'name': name, 'rock': 'chs' } )


xml.close()