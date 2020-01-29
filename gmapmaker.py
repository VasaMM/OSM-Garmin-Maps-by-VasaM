 #!/usr/bin/env python3

import os
from datetime import datetime

from makerfuncs import *
from makerfuncs.prints import say, error, end



# Nastevni a globalni promenne
class Options:
	def __init__(self):
		self.JAVAMEM  = '-Xmx4g'   # Maximalni velikost RAM, kterou lze pouzit, viz https://stackoverflow.com/questions/14763079/what-are-the-xms-and-xmx-parameters-when-starting-jvm
		self.MAX_JOBS = 4          # Maximalni pocet vlaken

		self.VERSION = 50		   # Verze generovane mapy



def main():
	

	try:
		# TODO vytvorit TMP slozku

		# Objekt pro ulozeni globalnich promennych a nastaveni
		o = Options()
	
		# Nactu konfiguracni soubor
		config.load(o)

		# Nactu a zpracuji arumenty
		args.parse(o)
	
		# Zaznamenam cas spusteni
		o.timeStart = datetime.now()
		say('Start at ' + str(o.timeStart), o)

		# Ziskam informace o statu
		area.get(o)

		# Nactu informace z hlavicky
		parser.fileHeader(o)

		# Stahnu mapova data
		download.mapData(o)

		# Stahnu polygon
		download.polygon(o)

		# Zpracuji polygon
		polygon.load(o)

		# Vytvorim vrstevnice
		generator.contours(o)

		# Generuji Garmin mapu
		generator.garmin(o)

		# TODO remove temp


	except Exception as e:
		error(str(e))

		exit(1)


	finally:
		# Ukoncim generovani
		end(o)


if __name__ == "__main__":
	main()