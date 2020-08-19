import zipfile, os, shutil, platform
from makerfuncs import download as d, config

def update():
	# TODO download
	versions = config.getVersions()


	splitter = config.get('splitter')
	if versions['splitter'] > splitter:
		print('Download splitter version', versions['splitter'])
		d.download('https://www.mkgmap.org.uk/download/splitter-r' + str(versions['splitter']) + '.zip', './splitter.zip')

		print('Unzip')
		with zipfile.ZipFile('./splitter.zip', 'r') as zipRef:
			zipRef.extractall('./')
			config.add('splitter', versions['splitter'])
		if os.path.isdir('./splitter-r' + str(splitter)):
			shutil.rmtree('./splitter-r' + str(splitter))
		os.remove('./splitter.zip')


	mkgmap = config.get('mkgmap')
	if versions['mkgmap'] > mkgmap:
		print('Download mkgmap version', versions['mkgmap'])
		d.download('https://www.mkgmap.org.uk/download/mkgmap-r' + str(versions['mkgmap']) + '.zip', './mkgmap.zip')

		print('Unzip')
		with zipfile.ZipFile('./mkgmap.zip', 'r') as zipRef:
			zipRef.extractall('./')
			config.add('mkgmap', versions['mkgmap'])
		if os.path.isdir('./mkgmap-r' + str(mkgmap)):
			shutil.rmtree('./mkgmap-r' + str(mkgmap))
		os.remove('./mkgmap.zip')


	# osmconvert
	sysVersion = platform.system()
	sysBits = platform.architecture()[0]

	print('Detected system' , sysVersion, sysBits)
	if sysVersion in ['Windows', 'Linux'] and sysBits in ['32bit', '64bit']:
		print('Download osmconvert for this system')
		if sysVersion == 'Linux':
			d.download('http://m.m.i24.cc/osmconvert' + sysBits[0:2], './osmconvert/osmconvert' + sysBits[0:2])
		elif sysVersion == 'Windows':
			d.download('http://m.m.i24.cc/osmconvert' + ('64' if sysBits == '64bit' else '') + '.exe', './osmconvert/osmconvert' + sysBits[0:2] + '.exe')

	else:
		print('')
		print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
		print('[ERROR] Unsupported system, see GitHub for instructions.')
		print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
		print('')



if __name__ == '__main__':
	update()

	594