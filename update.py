import zipfile, os, shutil, platform
from makerfuncs import download as d, config

def update():
	# TODO download
	versions = config.getVersions()


	splitter = config.get('splitter')
	if versions['splitter'] > splitter:
		print('Download splitter version', versions['splitter'])
		try:
			d.download('https://www.mkgmap.org.uk/download/splitter-r' + str(versions['splitter']) + '.zip', './splitter.zip')
		except:
			print('Download was unsuccessful! Maybe bad version?')
		else:
			print('Unzip')
			with zipfile.ZipFile('./splitter.zip', 'r') as zipRef:
				zipRef.extractall('./')
				config.add('splitter', versions['splitter'])
			if os.path.isdir('./splitter-r' + str(splitter)):
				shutil.rmtree('./splitter-r' + str(splitter))
			os.remove('./splitter.zip')
			print('Done')



	mkgmap = config.get('mkgmap')
	if versions['mkgmap'] > mkgmap:
		print('Download mkgmap version', versions['mkgmap'])
		try:
			d.download('https://www.mkgmap.org.uk/download/mkgmap-r' + str(versions['mkgmap']) + '.zip', './mkgmap.zip')
		except:
			print('Download was unsuccessful! Maybe bad version?')
		else:	
			print('Unzip')
			with zipfile.ZipFile('./mkgmap.zip', 'r') as zipRef:
				zipRef.extractall('./')
				config.add('mkgmap', versions['mkgmap'])
			if os.path.isdir('./mkgmap-r' + str(mkgmap)):
				shutil.rmtree('./mkgmap-r' + str(mkgmap))
			os.remove('./mkgmap.zip')
			print('Done')


	# osmconvert
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



	# Data sea
	if (not os.path.isdir(data['sea'])):
		d.download('http://osm.thkukuk.de/data/sea-latest.zip', './sea.zip')
		with zipfile.ZipFile('./sea.zip', 'r') as zipRef:
			zipRef.extractall(data['sea'])
		os.remove('./sea.zip')
		print('Done')
	else:
		print("Directoty " + data['sea'] + "already exists - skipping...")

	# Data bounds
	if (not os.path.isdir(data['bounds'])):
		d.download('http://osm.thkukuk.de/data/bounds-latest.zip', './bounds.zip')
		with zipfile.ZipFile('./bounds.zip', 'r') as zipRef:
			zipRef.extractall(data['bounds'])
		os.remove('./bounds.zip')
		print('Done')
	else:
		print("Directoty " + data['bounds'] + "already exists - skipping...")



if __name__ == '__main__':
	update()