 #!/usr/bin/env python3

import os
from datetime import datetime


from python.areas import State, get_area
from python.print import say, error
from python.functions import parse_args, make_log_file, download_map_data, make_contours, end
from python.mapsforge import make_mapsforge
from python.garmin import make_garmin
from python.polygons import parse_poly



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


		# Zaznamenam cas spusteni
		o.time_start = datetime.now()


		# Nactu arumenty
		parse_args(o)


		# Vytvorim logovaci soubor
		make_log_file(o)


		say('Start at ' + str(o.time_start), o)


		# Ziskam stat, nebyl-li zadan
		get_area(o)

		# Stahnu mapova data a polygon
		download_map_data(o)


		# Vytvorim vrstevnice
		make_contours(o)


		# Vytvorim cilovou podslozku
		if not os.path.exists('./img/' + o.state.id + '_VasaM'):
			os.makedirs('./img/' + o.state.id + '_VasaM')


		# parse_poly(o)

		# Generuji Mapsforge
		o.mapsforge = False
		if o.mapsforge:
			make_mapsforge(o)
		# Generuji Garmin
		else:
			make_garmin(o)


		# Ukoncim generovani
		end(o)



	except Exception as e:
		error('Some error...')
		print(e)

		exit(1)


	finally:
		if hasattr(o, 'log_file'):
			if o.log_file and o.log_file.close:
				o.log_file.close()


if __name__ == "__main__":
	main()