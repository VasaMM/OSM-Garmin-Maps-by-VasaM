import json, os

def save(data):
	with open('gmapmaker.config', 'w') as outfile:
		json.dump(data, outfile)


def load(o):
	with open('gmapmaker.config') as configFile:
		data = json.load(configFile)

		o.img      = data['img']
		o.pbf      = data['pbf']
		o.polygons = data['polygons']
		o.hgt      = data['hgt']
		o.sea      = data['sea']
		o.bounds   = data['bounds']
		o.splitter = data['splitter']
		o.mkgmap   = data['mkgmap']


def add(key, value):
	with open('gmapmaker.config', 'r+') as configFile:
		data = json.load(configFile)

		data[key] = value
		configFile.seek(0)
		configFile.truncate()
		json.dump(data, configFile)


def get(key):
	with open('gmapmaker.config', 'r') as configFile:
		data = json.load(configFile)

		if key in data:
			return data[key]
		else:
			return None


def getVersions():
	# TODO download
	with open('versions.info', 'r') as configFile:
		return json.load(configFile)
