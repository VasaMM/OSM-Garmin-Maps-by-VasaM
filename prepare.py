import os, update as u
from makerfuncs.config import Configuration


def _prepareUserAreas() -> None:
	# Prepare folder for user defined areas
	try:
		os.mkdir('userAreas')
	except FileExistsError:
		print("Directory userAreas already exists")

	with open('userAreas/myAreas.py', 'w') as file:
		file.write('from makerfuncs.Area import Area\n')
		file.write('from makerfuncs.states import STATES\n')
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
	# TODO OL.poly


def prepare() -> None:
	_prepareUserAreas()

	c = Configuration()
	c.load()

	QUESTIONS = {
		'img': 'The name of the output folder with garmin maps',
		'pbf': 'The name of the folder for map data download',
		'polygons': 'The name of the folder for polygons',
		'hgt': 'The name of the folder for height data',
		'temp': 'The name of the folder for temporary data',
		'sea': 'The name of the folder for sea data',
		'bounds': 'The name of the folder for bounds data',
	}

	for key in QUESTIONS:
		question = QUESTIONS[key]
		if c[key].setted:
			question += ' (actual ' + c[key].getValue() + '): '
		else:
			question += ' (default ' + c[key].getDefault() + '): '

		value = input(question)
		if value == '':
			c[key].set(c[key].getDefault())
		else:
			c[key].set(value)


	PATHS = ['img', 'pbf', 'polygons', 'hgt', 'temp', 'sea', 'bounds']

	for key in PATHS:
		path = os.path.abspath(c[key].getValue())

		try:
			os.mkdir(path)
		except FileExistsError:
			print('Directory ' + path + ' already exists')
		except:
			raise RuntimeError('Directory ' + path + ' is invalid')
		else:
			c[key].set(path)

	c.save()
	u.update()


if __name__ == '__main__':
	prepare()