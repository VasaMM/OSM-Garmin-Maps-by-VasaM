#!/usr/bin/env python3

import re, PySimpleGUI as sg
from makerfuncs.states import STATES
from userAreas.myAreas import USER_AREAS
from gmapmaker import Options, main as generateMap



# Vytvorim data pro tree se staty
treeData = sg.TreeData()
rootTreeItems = ['userAreas']

treeData.Insert(parent='', key='userAreas', text='Uživatelské oblasti', values=[])
for area in USER_AREAS:
	treeData.Insert(parent='userAreas', key=area, text=USER_AREAS[area].nameCs, values=[])

for id in STATES:
	treeData.Insert(parent='', key=id, text=id, values=[])
	rootTreeItems.append(id)
	for state in STATES[id]:
		treeData.Insert(parent=id, key=state, text=STATES[id][state].nameCs, values=[])



# Definice GUI
areaFrame = [
	[
		sg.Text("Vyberte oblast"),
	],
	[
		# sg.InputText(key="area", size=(20, 0))
		sg.Tree(data=treeData, select_mode=sg.TABLE_SELECT_MODE_BROWSE, num_rows=15, col0_width=40, enable_events=True, key='chooseArea')
	]
]

mapProperties = [
	[
		sg.Text("Kódová stránka"),
		sg.OptionMenu(['Windows-1250', 'Windows-1252', 'Latin-2', 'Unicode', 'ASCII'], default_value='Windows-1250', key='codePage', disabled=True)
	],
	[
		sg.Text("Stáhnout nová data"),
		sg.OptionMenu(['Jsou-li starší než 1 den', 'Jsou-li starší než 3 dny', 'Jsou-li starší než týden', 'Vždy', 'Nikdy'], default_value='Jsou-li starší než 1 den', key='download', disabled=True)
	],
	[
		sg.Text("ID mapy"),
		sg.InputText(key='mapNumber', disabled=True, enable_events=True)
	],
	[
		sg.Text("Přípona za jménem"),
		sg.InputText(key='suffix', default_text='_VasaM', disabled=True, enable_events=True)
	],
	[
		sg.Text("Oříznout mapový soubor podle polygonu"),
		sg.OptionMenu(['Ne', 'Ano'], default_value='Ne', key='crop', disabled=True)
	],
	[
		sg.Text("Nedělit mapove soiubory na menší"),
		sg.OptionMenu(['Ne', 'Ano'], default_value='Ne', key='split', disabled=True)
	],
]

layout = [
	[
		sg.Frame("1", areaFrame),
	],
	[
		sg.Frame("2", mapProperties),
	],
	[
		sg.Frame("3", [[sg.Button('Generovat', key='generate', disabled=True)]]),
	],
	[
		sg.Frame("4", [[sg.Multiline(write_only=True, size=(None, 20), reroute_stdout=False, key='output')]]),
		# sg.Frame("4", [[sg.Multiline(write_only=True, size=(None, 20), reroute_stdout=True, key='output')]]), // FIXME
	],
]



def main():
	# vytvoření okna s ovládacími prvky
	window = sg.Window("GMapMaker GUI", layout)

	inputsToUpdate = [window['codePage'], window['download'], window['mapNumber'], window['suffix'], window['crop'], window['split'], window['generate']]

	previousMapNumberValue = window['mapNumber'].get()
	previousSuffixValue = window['suffix'].get()

	# obsluha smyčky událostí (event loop)
	while True:
		# přečtení události
		event, values = window.read()

		import sys
		print("Event: ", event, "    Values: ", values, file=sys.stderr)
	    # progressBar.UpdateBar(i+1)

		if event == 'chooseArea':
			areaId = values['chooseArea'][0]
			for input in inputsToUpdate:
				input.update(disabled=areaId in rootTreeItems)

			mapNumber = ''
			if areaId not in rootTreeItems:
				founded = False
				for userArea in USER_AREAS:
					if userArea == areaId:
						founded = True
						mapNumber=USER_AREAS[areaId].number
				if not founded:
					for continent in STATES:
						for state in STATES[continent]:
							if state == areaId:
								mapNumber = STATES[continent][areaId].number

			window['mapNumber'].update(value=mapNumber)

		elif event == 'mapNumber':
			newValue = window['mapNumber'].get()
			if newValue.isascii() and newValue.isdigit() and int(newValue) <= 9999:
				previousMapNumberValue = newValue
			else:
				window['mapNumber'].update(value=previousMapNumberValue)

		elif event == 'suffix':
			newValue = window['suffix'].get()
			if re.match(r'^[a-zA-Z0-9_\-]+$', newValue):
				previousSuffixValue = newValue
			else:
				window['suffix'].update(value=previousSuffixValue)

		elif event == 'generate':
			for input in inputsToUpdate:
				input.update(disabled=True)

			def parseDownloadType(value):
				if value in ['Jsou-li starší než 1 den', 'Jsou-li starší než 3 dny', 'Jsou-li starší než týden']:
					return 'auto'
				elif value == 'Nikdy':
					return 'skip'
				else:
					return 'force'

			def parseMaximumDataAge(value):
				if value == 'Jsou-li starší než týden':
					return 7 * 24 * 3600
				elif value == 'Jsou-li starší než 3 dny':
					return 3 * 24 * 3600
				else:
					return 1 * 24 * 3600

			def parseCodePage(codePage):
				if codePage == 'Windows-1250':
					return '1250'
				elif codePage == 'Windows-1252':
					return '1252'
				elif codePage == 'Latin-2':
					return 'latin2'
				elif codePage == 'Unicode':
					return 'unicode'
				else:
					return 'ascii'


			o = Options()
			o.split          = values['split'] == 'Ano'
			o.area           = values['chooseArea'][0]
			o.downloadMap    = parseDownloadType(values['download'])
			o.maximumDataAge = parseMaximumDataAge(values['download'])
			o.extend         = 0
			o.quiet          = False
			o.logFile        = False
			o.code           = parseCodePage(values['codePage'])
			o.crop           = values['crop'] == 'Ano'
			o.mapNumber      = int(values['mapNumber'])
			o.variant        = 0
			o.en             = False
			o.sufix          = values['suffix']

			generateMap(False, o)

		# Reakce na událost "uzavření okna"
		elif event == sg.WIN_CLOSED:
			break

	# po výskoku ze smyčky událostí aplikaci ukončíme
	window.close()


if __name__ == "__main__":
	main()