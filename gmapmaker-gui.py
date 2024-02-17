#!/usr/bin/env python3

import re, PySimpleGUI as sg

from queue import Queue
from threading import Thread

from makerfuncs.parser import codePage, downloadType, maximumDataAge
from makerfuncs.states import STATES, continentNames
from makerfuncs.prints import error
from makerfuncs.Lang import Lang, _
from userAreas.myAreas import USER_AREAS
from gmapmaker import Options, main as generateMap


# Lang.bindLanguage('en')


def getMapFromAreaId(areaId):
	for userArea in USER_AREAS:
		if userArea == areaId:
			return USER_AREAS[areaId].number
	for continent in STATES:
		for state in STATES[continent]:
			if state == areaId:
				return STATES[continent][areaId].number


class Window:
	def prepareLayout(self):
		# Vytvorim data pro tree se staty
		treeData = sg.TreeData()
		self.rootTreeItems = ['userAreas']

		treeData.Insert(parent='', key='userAreas', text=_('Uživatelské oblasti'), values=[])
		for area in USER_AREAS:
			treeData.Insert(parent='userAreas', key=area, text=USER_AREAS[area].nameCs, values=[])

		for continentId in STATES:
			treeData.Insert(parent='', key=continentId, text=_(continentNames[continentId]), values=[])
			self.rootTreeItems.append(continentId)

			for stateId, state in sorted( STATES[continentId].items(), key=lambda item: item[1].nameCs if Lang.getLanguage() == 'cs' else item[1].nameEn):
				name = state.nameCs if Lang.getLanguage() == 'cs' else state.nameEn
				treeData.Insert(parent=continentId, key=stateId, text=name, values=[])



		# Definice GUI
		areaFrame = [
			[sg.Text("Vyberte oblast")],
			[sg.Tree(data=treeData, select_mode=sg.TABLE_SELECT_MODE_BROWSE, num_rows=11, expand_x=True, enable_events=True, key='chooseArea')]
		]

		mapProperties = [
			[
				sg.Text("Kódová stránka", size=(29, None), justification="r"),
				sg.OptionMenu(['Windows-1250', 'Windows-1252', 'Latin-2', 'Unicode', 'ASCII'], default_value='Windows-1250', key='codePage', disabled=True)
			],
			[
				sg.Text("Stáhnout nová data", size=(29, None), justification="r"),
				sg.OptionMenu(['Jsou-li starší než 1 den', 'Jsou-li starší než 3 dny', 'Jsou-li starší než týden', 'Vždy', 'Nikdy'], default_value='Jsou-li starší než 1 den', key='download', disabled=True)
			],
			[
				sg.Text("ID mapy", size=(29, None), justification="r"),
				sg.InputText(key='mapNumber', size=(5, 0), disabled=True, enable_events=True)
			],
			[
				sg.Text("Přípona za jménem", size=(29, None), justification="r"),
				sg.InputText(key='suffix', default_text='_VasaM', size=(20, 0), disabled=True, enable_events=True)
			],
			[
				sg.Text("Oříznout mapový soubor podle polygonu", size=(29, None), justification="r"),
				sg.OptionMenu(['Ne', 'Ano'], default_value='Ne', key='crop', disabled=True)
			],
			[
				sg.Text("Nedělit mapove soubory na menší", size=(29, None), justification="r"),
				sg.OptionMenu(['Ne', 'Ano'], default_value='Ne', key='split', disabled=True)
			],
		]

		return [[
			sg.Column([
				[sg.Frame("1", areaFrame, expand_x=True)],
				[sg.Frame("2", mapProperties)],
			]),
			sg.Column([
				[sg.Frame("3", [[sg.Button('Generovat', key='generate', disabled=True, size=(80, 0))]])],
				[sg.Frame("4", [[sg.Output(expand_x=True, expand_y=True, font='Courier 10', autoscroll_only_at_bottom=True, echo_stdout_stderr=True)]], expand_x=True, expand_y=True)]
			], expand_x=True, expand_y=True)
		]]


	def __init__(self):
		self.window = sg.Window("GMapMaker GUI", self.prepareLayout(), finalize=True)

		self.locked = False
		self.previousMapNumberValue = self.window['mapNumber'].get()
		self.previousSuffixValue = self.window['suffix'].get()

	def setDisabled(self, newState):
		if not self.locked:
			for input in ['codePage', 'download', 'mapNumber', 'suffix', 'crop', 'split', 'generate']:
				self.window[input].update(disabled=newState)

	def lock(self):
		self.setDisabled(True)
		self.locked = True

	def unlock(self):
		self.setDisabled(False)
		self.locked = False

	def isLocked(self):
		return self.locked

	def read(self):
		return self.window.read()

	def close(self):
		return self.window.close()

	def __getitem__(self, key):
		return self.window[key]



def main():
	o = Options()
	w = Window()
	q = Queue()


	def generateMapJob(o, queue):
		try:
			generateMap(o)
		except Exception as e:
			error(str(e))
		finally:
			queue.put(True)
	generatorThread = Thread(target=generateMapJob, args=(o, q))


	def windowJob(queue, window: Window):
		while True:
			queue.get()
			window.unlock()
	windowThread = Thread(target=windowJob, args=(q, w))
	windowThread.start()


	# Event loop
	while True:
		event, values = w.read()
		# print("Event: ", event, "    Values: ", values)

		if event == sg.WIN_CLOSED:
			break

		elif event == 'chooseArea':
			areaId = values['chooseArea'][0]
			w.setDisabled(areaId in w.rootTreeItems)
			w['mapNumber'].update(value='' if areaId in w.rootTreeItems else getMapFromAreaId(areaId))

		elif event == 'mapNumber':
			newValue = w.window['mapNumber'].get()
			if newValue.isascii() and newValue.isdigit() and int(newValue) <= 9999:
				previousMapNumberValue = newValue
			else:
				w['mapNumber'].update(value=previousMapNumberValue)

		elif event == 'suffix':
			newValue = w.window['suffix'].get()
			if re.match(r'^[a-zA-Z0-9_\-]+$', newValue):
				previousSuffixValue = newValue
			else:
				w['suffix'].update(value=previousSuffixValue)

		elif event == 'generate':
			# FIXME multiple start
			# TODO download progressbar
			w.lock()

			o.split          = values['split'] == 'Ano'
			o.area           = values['chooseArea'][0]
			o.downloadMap    = downloadType(values['download'])
			o.maximumDataAge = maximumDataAge(values['download'])
			o.extend         = 0
			o.quiet          = False
			o.logFile        = False
			o.code           = codePage(values['codePage'])
			o.crop           = values['crop'] == 'Ano'
			o.extend         = None
			o.mapNumber      = int(values['mapNumber'])
			o.variant        = None
			o.en             = False
			o.sufix          = values['suffix']

			o.gui = True

			generatorThread.start()

	w.close()


if __name__ == "__main__":
	main()
