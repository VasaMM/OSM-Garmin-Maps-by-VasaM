class State:
	def __init__(self, name, number, parent = None, dataUrl = None, polyUrl = None, pois = [], crop = False):
		self.dataUrl = dataUrl      # map data url address (*.osm.pbf file)
		self.polyUrl = polyUrl      # polygon url address (*.poly or *.geojson file)
		self.name    = name         # Full name of map
		self.number  = number       # Map number id
		self.parent  = parent
		self.pois    = pois         # List of files with pois
		self.crop    = crop
		
		# if len(lang) > 0:
		# 	self.lang = ' --name-tag-list='
		# 	for l in lang:
		# 		self.lang += 'name:' + l + ','
	
		# 	self.lang = self.lang[ 0 : -1 ] + ' '
		# else:
		# 	self.lang = ' '


	def __str__(self):
		_id = 'None'
		if hasattr(self, 'id'):
			_id = self.id
		_mapDataName = 'None'
		if hasattr(self, 'mapDataName'):
			_mapDataName = self.mapDataName
		return "dataUrl: %s\npolyUrl: %s\nname: %s\nnumber: %s\npois: %s\nparent: %s\nid: %s\ncrop: %s\nmapDataName: %s\n" % (self.dataUrl, self.polyUrl, self.name, self.number, self.pois, self.parent, _id, self.crop, self.mapDataName)