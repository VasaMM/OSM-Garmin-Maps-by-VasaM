from bs4 import BeautifulSoup

diacritics=str.maketrans(
	"ÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜÝßàáâãäåçèéêëìíîïñòóôõöùúûüýÿĀāĂăĄąĆćĈĉĊċČčĎďĐđĒēĔĕĖėĘęĚěĜĝĞğĠġĢģĤĥĦħĨĩĪīĬĭĮįİıĶķĸĹĺĻļĽľĿŀŁłŃńŅņŇňŉŊŋŌōŎŏŐőŔŕŖŗŘřŚśŜŝŞşŠšŢţŤťŦŧŨũŪūŬŭŮůŰűŲųŴŵŶŷŸŹźŻżŽžſ",
	"AAAAAACEEEEIIIINOOOOOUUUUYsaaaaaaceeeeiiiinooooouuuuyyAaAaAaCcCcCcCcDdDdEeEeEeEeEeGgGgGgGgHhHhIiIiIiIiIiKkkLlLlLlLlLlNnNnNnNnNOoOoOoRrRrRrSsSsSsSsTtTtTtUuUuUuUuUuUuWwYyYZzZzZzs"
)

# Vytvorim slovnik kod : [anglicky, cesky]
codes = {}
with open('staty.csv', 'r', encoding='utf-8') as csvFile:
	# 0 ... ciselny kod
	# 1 ... 2 kod
	# 2 ... 3 kod
	# 3 ... česky dlouhý název
	# 4 ... česky krátký název
	# 5 ... anglicky dlouhý název
	# 6 ... anglicky krátký název
	for line in csvFile:
		# Rozdelim na bunky
		data = line.split(';')

		# Odtsranim \n na konci
		data[6] = data[6][0:-1]

		# Zapisu
		codes[data[1]] = {'en': data[6].translate(diacritics), 'cs': data[4].translate(diacritics)}

# for code in codes:
# 	print(code, codes[code])


# Zpracuji stazene html soubory
files = [
	'europe', 
	'asia',
	'africa',
	'north-america',
	'central-america',
	'south-america',
	'australia-oceania',
]

numbers = {
	'europe'            : 7000,
	'asia'              : 7300,
	'africa'            : 7500,
	'north-america'     : 7800,
	'central-america'   : 8100,
	'south-america'     : 8200,
	'australia-oceania' : 8300,
}

states = {}
for file in files:
	states[file] = {}

	with open(file + '.html', 'r') as html:
		parser = BeautifulSoup(html.read(), "lxml")

		# Nactu vsechny subregiony
		subregions = parser.find_all("table", {"id": "subregions"})[1].findChildren( "td", {"class": "subregion"} )

		# print('Missing in ' + file + ':')
		# print('-----------------------')
		# Projdu subregiony
		for subregion in subregions:
			state = subregion.find('a')
			
			# Doplnim adresu do tabulky
			added = False
			for code, data in codes.items():
				if data['en'] == state.string:
					data['url'] = state['href'][len(file)+1:-5]
					codes[code]['url'] = state['href'][len(file)+1:-5]
					added = True
					states[file][code] = data
					break

			if added is False:
				print(state.string)




# for area in states:
# 	print(area)
# 	for code in states[area]:
# 		print(code, " => ", states[area][code], sep='')


with open('states.py', 'w') as out:
	out.write("from makerfuncs.Area import State\n\n")
	out.write("STATES = {\n")

	for area in states:
		out.write("\t'%s': {\n" % (area))

		number = numbers[area]
		for code in states[area]:
			number += 5
			out.write("\t\t'%s': State(\n" % code)
			out.write("\t\t\turl    = '%s',\n" % (states[area][code]['url']))
			out.write("\t\t\tnameCs = '%s',\n" % (states[area][code]['cs']))
			out.write("\t\t\tnameEn = '%s',\n" % (states[area][code]['en']))
			out.write("\t\t\tnumber = %i,\n" % (number))
			out.write("\t\t),\n")

		out.write("\t},\n\n")

	out.write("}\n")

