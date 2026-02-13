import os


def prepareUserAreas():
	# Pripravim slozku pro uzivatelske oblasti
	try:
		os.mkdir('userAreas')
	except FileExistsError:
		print("Directory userAreas already exists")

	with open('userAreas/myAreas.py', 'w') as file:
		file.write('from makerfuncs.Area import Area\n')
		file.write('\n')
		file.write('USER_AREAS = {\n')
		file.write('	\'OL\': Area(\n')
		file.write('		parent = \'CZ\',\n')
		file.write('		nameCs = \'Olomouc\',\n')
		file.write('		number = 8800,\n')
		file.write('		pois   = [\'./pois/chs.osm.xml\',],\n')
		file.write('		crop   = True\n')
		file.write('	),\n')
		file.write('}\n')


def prepare():
	prepareUserAreas()

	from makerfuncs import config
	import update as u

	default = {
		'img':      'maps',
		'pbf':      'pbf',
		'polygons': 'polygons',
		'hgt':      'hgt',
		'temp':     'temp',
		'sea':      'sea',
		'bounds':   'bounds',
	}

	data = {}


	#TODO kontroly validity vstupu
	data['img'] = input('The name of the output folder with garmin maps (default maps): ')
	data['pbf'] = input('The name of the folder for map data download (default pbf): ')
	data['polygons'] = input('The name of the folder for polygons (default polygons): ')
	data['hgt'] = input('The name of the folder for height data (default hgt): ')
	data['temp'] = input('The name of the folder for temporary data (default temp): ')
	data['sea'] = input('The name of the folder for sea data (default sea): ')
	data['bounds'] = input('The name of the folder for bounds data (default bounds): ')

	for item in data:
		if data[item] == '':
			data[item] = default[item]
		if data[item][-1] != '/':
			data[item] = data[item] + '/'

		try:
			os.mkdir(data[item])
		except:
			print("Directory " + data[item] + " already exists")
			pass


	data['splitter'] = 0
	data['mkgmap'] = 0

	config.save(data)

	u.update()




if __name__ == '__main__':
	prepare()