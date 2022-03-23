import json, os

class Item:
	setted = False

	def set(self, value):
		if type(value) != self.valueType:
			raise RuntimeError('Ivalid type of value! ' + value + ': ' + self.valueType + ' expected but ' + type(value) + ' getted.')
		self.value = value
		self.setted = True

	def unset(self):
		self.setted = False

	def getType(self):
		return self.valueType

	def getValue(self):
		if self.setted:
			return self.value
		else:
			raise RuntimeError('Item is unset!')

	def getValueOrDefault(self):
		if self.setted:
			return self.getValue()
		else:
			return self.getDefault()

	def getDefault(self):
		return self.default

	def __init__(self, valueType, defaultValue):
		self.value = None
		self.valueType = valueType
		if type(defaultValue) != valueType:
			raise RuntimeError('Ivalid type of value! ' + str(defaultValue) + ': ' + str(valueType) + ' expected but ' + str(type(defaultValue)) + ' getted.')
		self.default = defaultValue

	def __str__(self):
		return str(self.value) + ': ' + str(self.valueType) + ' [' + str(self.default) + ']'



class Configuration:
	items = {
		'img':      Item(str, os.path.abspath('maps')),
		'pbf':      Item(str, os.path.abspath('pbf')),
		'polygons': Item(str, os.path.abspath('polygons')),
		'hgt':      Item(str, os.path.abspath('hgt')),
		'temp':     Item(str, os.path.abspath('temp')),
		'sea':      Item(str, os.path.abspath('sea')),
		'bounds':   Item(str, os.path.abspath('bounds')),
		'splitter': Item(int, 0),
		'mkgmap':   Item(int, 0),
	}

	def __str__(self):
		output = ''
		for key, item in self:
			output += key + '\t => ' + str(item) + '\n'
		return output

	def __len__(self):
		return len(self.items)

	def __getitem__(self, key):
		return self.items[key]

	def __contains__(self, key):
		return key in self.items

	def __iter__(self):
		self.iterIndex = 0
		return self

	def __next__(self):
		if self.iterIndex == len(self):
			raise StopIteration

		for i, key in enumerate(self.items.keys()):
			if i == self.iterIndex:
				break

		self.iterIndex += 1
		return key, self.items[key]


	def save(self) -> None:
		with open('gmapmaker.config', 'w') as outfile:
			data = {}

			for key, item in self:
				data[key] = item.getValueOrDefault()
			json.dump(data, outfile)


	def load(self) -> bool:
		try:
			with open('gmapmaker.config', 'r') as configFile:
				data = json.load(configFile)

				for key in data:
					if key in self:
						self[key].set(data[key])

				return True

		except IOError:
			return False