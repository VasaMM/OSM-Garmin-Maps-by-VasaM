from bs4 import BeautifulSoup

files = ('africa', )


for file in files:
	html = open(file + ".html", "r")

	parser = BeautifulSoup(html.read(), "lxml")

	subregions = parser.find_all("table", {"id": "subregions"})[1].findChildren( "td", {"class": "subregion"} )


	for subregion in subregions:
		state = subregion.find('a')

		print( state.string, ':', state['href'][len(file)+1:-5] )


