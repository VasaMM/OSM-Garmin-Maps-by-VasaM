class State:
	def __init__(self, nameCs, nameEn, number, url, pois = [], crop = False):
		self.url    = url      # map data url address (*.osm.pbf file)
		self.nameCs = nameCs         # Full name of map
		self.nameEn = nameEn         # Full name of map
		self.number = number       # Map number id
		self.pois   = pois         # List of files with pois
		self.crop   = False

	def __str__(self):
		id = 'None'
		if hasattr(self, 'id'):
			id = self.id

		mapDataName = 'None'
		if hasattr(self, 'mapDataName'):
			mapDataName = self.mapDataName
		
		crop = 'None'
		if hasattr(self, 'crop'):
			crop = self.crop

		parent = 'None'
		if hasattr(self, 'parent'):
			parent = self.parent

		continent = 'None'
		if hasattr(self, 'continent'):
			continent = self.continent

		return "\
	url: %s\n\
	nameCs: %s\n\
	nameEn: %s\n\
	number: %s\n\
	pois: %s\n\
	id: %s\n\
	crop: %s\n\
	mapDataName: %s\n\
	parent: %s\n\
	continent: %s\n\
	" % (self.url, self.nameCs, self.nameEn, self.number, self.pois, id, crop, mapDataName, parent, continent)



class Area(State):
	def __init__(self, nameCs, number, nameEn = None, url = None, pois = [], parent = None, crop = False):
		self.parent = parent

		if nameEn is None:
			nameEn = nameCs

		super().__init__(nameCs, nameEn, number, url, pois, crop)




