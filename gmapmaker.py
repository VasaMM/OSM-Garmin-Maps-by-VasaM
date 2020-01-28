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

		self.VERSION = 48		   # Verze generovane mapy



def main():
	try:
		# Objekt pro ulozeni globalnich promennych a nastaveni
		o = Options()


		config.load(o)


		# Zaznamenam cas spusteni
		o.time_start = datetime.now()


		# Nactu arumenty
		args.parse(o)


		say('Start at ' + str(o.time_start), o)


		# Ziskam stat, nebyl-li zadan
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


		# parse_poly(o)

		# Generuji Garmin mapu
		generator.garmin(o)


		# Ukoncim generovani
		end(o)



	except Exception as e:
		error('Some error...')
		print(e)

		exit(1)


	finally:
		if hasattr(o, 'logFile'):
			if o.logFile and o.logFile.close:
				o.logFile.close()


if __name__ == "__main__":
	main()