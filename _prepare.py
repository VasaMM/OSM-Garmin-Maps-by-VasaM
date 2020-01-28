import zipfile, json, os
from makerfuncs import config, download as d
import _update as u

def prepare():
	data = {}

	#TODO kontroly validity vstupu
	data['img'] = input('The name of the output folder with garmin maps: ')
	data['pbf'] = input('The name of the folder for map data download: ')
	data['polygons'] = input('The name of the folder for polygons: ')
	data['hgt'] = input('The name of the folder for height data: ')
	
	data['sea'] = input('The name of the folder for sea data: ')
	data['bounds'] = input('The name of the folder for bounds data: ')

	for item in data:
		if data[item][-1] != '/':
			data[item] = data[item] + '/'

	# TODO phyghtmap


	d.download('http://osm.thkukuk.de/data/sea-latest.zip', './sea.zip')
	with zipfile.ZipFile('./sea.zip', 'r') as zipRef:
		zipRef.extractall(data['sea'])
	os.remove('./sea.zip')

	d.download('http://osm.thkukuk.de/data/bounds-latest.zip', './bounds.zip')
	with zipfile.ZipFile('./bounds.zip', 'r') as zipRef:
		zipRef.extractall(data['bounds'])
	os.remove('./bounds.zip')


	data['splitter'] = 0
	data['mkgmap'] = 0

	config.save(data)

	u.update()


if __name__ == '__main__':
	prepare()