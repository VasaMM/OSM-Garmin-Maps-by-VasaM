import zipfile, os, shutil, platform
from makerfuncs import download as d
from makerfuncs.config import Configuration
from bs4 import BeautifulSoup
from os import path


def _mkgmapGetToolsVersion(toolName: str, c: Configuration) -> int:
	tmpFilePath = path.join(c['temp'].getValue(), toolName + '.html')
	version: int

	try:
		d.download('https://www.mkgmap.org.uk/download/' + toolName + '.html', tmpFilePath)
	except:
		print('Downloading ' + toolName + ' html webpage was unsuccessful.')
	else:
		with open(tmpFilePath, 'r') as html:
			parsedHtml = BeautifulSoup(html, 'html.parser')
			versionTag = parsedHtml.body.find('p', attrs={'class':'download-headline'}).find('span', attrs={'data-bind':'text: current().version'})
			if versionTag:
				version = int(versionTag.get_text())
			else:
				print('Parsing ' + toolName + ' version was unsuccessful.')

	if path.isfile(tmpFilePath):
		os.remove(tmpFilePath)

	return version



def _updateMkgmapTools(toolName: str, c: Configuration) -> None:
	actualVersion = c[toolName].getValue()
	version = _mkgmapGetToolsVersion(toolName, c)
	if version > actualVersion:
		tmpFilePath = path.join(c['temp'].getValue(), toolName + '.zip')
		print('Download ' + toolName + ' version', version)
		try:
			d.download('https://www.mkgmap.org.uk/download/' + toolName + '-r' + str(version) + '.zip', tmpFilePath)
		except:
			print('Download was unsuccessful! Maybe bad version?')
		else:
			print('Unzip')
			with zipfile.ZipFile(tmpFilePath, 'r') as zipRef:
				zipRef.extractall('./')
				c[toolName].set(version)
			if os.path.isdir(toolName + '-r' + str(actualVersion)):
				shutil.rmtree(toolName + '-r' + str(actualVersion))
			os.remove(tmpFilePath)
			print('Done')
	else:
		print('Program ' + toolName + ' is up to date')



def _downloadMkgmapHelperFiles(fileName: str, c: Configuration) -> None:
	if (not os.path.isdir(c[fileName].getValue())):
		tmpFilePath = path.join(c['temp'].getValue(), fileName + '.zip')
		d.download('http://osm.thkukuk.de/data/' + fileName + '-latest.zip', tmpFilePath)
		with zipfile.ZipFile(tmpFilePath, 'r') as zipRef:
			zipRef.extractall(c[fileName].getValue())
		os.remove(tmpFilePath)
		print('Done')
	else:
		print("Directory '" + c[fileName].getValue() + "' already exists - skipping...")



def _downloadOsmconvert() -> None:
	if (not os.path.isdir('osmconvert')):
		sysVersion = platform.system()
		sysBits = platform.architecture()[0]

		print('Detected system' , sysVersion, sysBits)
		if sysVersion in ['Windows', 'Linux'] and sysBits in ['32bit', '64bit']:
			print('Download osmconvert for this system')
			if sysVersion == 'Linux':
				d.download('http://m.m.i24.cc/osmconvert' + sysBits[0:2], './osmconvert/osmconvert' + sysBits[0:2])
			elif sysVersion == 'Windows':
				d.download('http://m.m.i24.cc/osmconvert' + ('64' if sysBits == '64bit' else '') + '.exe', './osmconvert/osmconvert' + sysBits[0:2] + '.exe')
			print('Done')

		else:
			print('')
			print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
			print('[ERROR] Unsupported system, see GitHub for instructions.')
			print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
			print('')
	else:
		print('Program osmconvert is up to date')



def update() -> None:
	c = Configuration()
	c.load()

	_updateMkgmapTools('splitter', c)
	_updateMkgmapTools('mkgmap', c)
	_downloadOsmconvert()
	_downloadMkgmapHelperFiles('sea', c)
	_downloadMkgmapHelperFiles('bounds', c)

	c.save()


if __name__ == '__main__':
	update()