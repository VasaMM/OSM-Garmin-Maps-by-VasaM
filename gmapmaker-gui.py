#!/usr/bin/env python3

# import os, sys
# for file in os.listdir(sys._MEIPASS):
#    print(file)
# print(sys._MEIPASS)
# while True:
# 	pass

import re, PySimpleGUI as sg

from threading import Thread, Event

from makerfuncs.parser import codePage, downloadType, maximumDataAge
from makerfuncs.states import STATES, continentNames
from makerfuncs.Options import Options
from makerfuncs.prints import error
from makerfuncs.Lang import Lang, _
from userAreas.myAreas import USER_AREAS
from gmapmaker import generate


Lang.bindLanguage('cs')
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

		treeData.Insert(parent='', key='userAreas', text=_('User areas'), values=[])
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
			[sg.Text(_("Choose a state"))],
			[sg.Tree(data=treeData, select_mode=sg.TABLE_SELECT_MODE_BROWSE, num_rows=11, expand_x=True, enable_events=True, key='chooseArea')]
		]

		mapProperties = [
			[
				sg.Text(_("Code page"), size=(29, None), justification="r"),
				sg.OptionMenu(['Windows-1250', 'Windows-1252', 'Latin-2', 'Unicode', 'ASCII'], default_value='Windows-1250', key='codePage', disabled=True)
			],
			[
				sg.Text(_("Download new data"), size=(29, None), justification="r"),
				sg.OptionMenu([_('When is older than day'), _('When is older than 3 days'), _('When is older than week'), _('Always'), _('Never')], default_value=_('When is older than day'), key='download', disabled=True)
			],
			[
				sg.Text(_("Map ID"), size=(29, None), justification="r"),
				sg.InputText(key='mapNumber', size=(5, 0), disabled=True, enable_events=True)
			],
			[
				sg.Text(_("File suffix"), size=(29, None), justification="r"),
				sg.InputText(key='suffix', default_text='_VasaM', size=(20, 0), disabled=True, enable_events=True)
			],
			[
				sg.Text(_("Crop map file by polygon"), size=(29, None), justification="r"),
				sg.OptionMenu([_('No'), _('Yes')], default_value=_('No'), key='crop', disabled=True)
			],
			[
				sg.Text(_("Don\'t split map files to smaller"), size=(29, None), justification="r"),
				sg.OptionMenu([_('No'), _('Yes')], default_value=_('No'), key='split', disabled=True)
			],
		]

		return [[
			sg.Column([
				[sg.Frame("1", areaFrame, expand_x=True)],
				[sg.Frame("2", mapProperties)],
			]),
			sg.Column([
				[sg.Frame("3", [[sg.Button(_('Generate'), key='generate', disabled=True, size=(80, 0))]])],
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
		self.locked = False
		self.setDisabled(False)

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

	jobIsPrepared = Event()
	jobIsDone = Event()


	def generateMapJob():
		try:
			while True:
				jobIsPrepared.wait()
				jobIsPrepared.clear()
				generate(o)
				jobIsDone.set()
		except Exception as e:
			error(str(e))
		finally:
			jobIsDone.set()
	generatorThread = Thread(target=generateMapJob)
	generatorThread.start()

	def windowJob():
		while True:
			jobIsDone.wait()
			jobIsDone.clear()
			w.unlock()
	windowThread = Thread(target=windowJob)
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
			# TODO download progressbar
			w.lock()

			o.gui = True

			o.split          = values['split'] == _('Yes')
			o.areaId         = values['chooseArea'][0]
			o.downloadMap    = downloadType(values['download'])
			o.maximumDataAge = maximumDataAge(values['download'])
			o.extend         = None
			o.quiet          = False
			o.logFile        = False
			o.code           = codePage(values['codePage'])
			o.crop           = values['crop'] == _('Yes')
			o.mapNumber      = int(values['mapNumber'])
			o.variant        = None
			o.en             = False
			o.sufix          = values['suffix']

			jobIsPrepared.set()


	w.close()
	print('ends')
	# exit(0)


if __name__ == "__main__":
	main()
