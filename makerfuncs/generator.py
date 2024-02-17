import os, sys, glob, zipfile, hashlib, json, platform
import subprocess
from makerfuncs.Options import Options

from makerfuncs.prints import say, error, log
from makerfuncs.Lang import _


def _sha1(filename: str):
	hash_func = hashlib.sha1()

	with open(filename, 'rb') as f:
		while True:
			data = f.read(67108864) # Read 64Mb of file
			if not data:
				break
			hash_func.update(data)

	return hash_func.hexdigest()


def run(program: list[str], o: Options) -> str:
	say(' '.join(program), o, '[RUN] ')
	process = subprocess.Popen(program, universal_newlines=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

	output = ''
	for line in process.stdout:
		output += line
		say(line, o, '', '')
		log(line, o)

	returnCode = process.wait()
	if returnCode != 0:
		raise ValueError(program[0] + ' ' + _('returns') + ' ' + str(returnCode) + ' (0 expected)')

	return output


def contours(o: Options) -> None:
	say(_('Generating contours'), o)
	# Check if SRTM file exists
	if not os.path.isfile(os.path.join(o.pbf, o.area.id + '-SRTM.osm.pbf')):
		run([
			'phyghtmap', # FIXME
			'--polygon=' + os.path.join(o.temp, 'polygon.poly'),
			'-o', os.path.join(o.pbf, o.area.id + '-SRTM'),
			'--pbf',
			'-j', '2',
			'-s', '10',
			'-c', '200,100',
			'--hgtdir=' + o.hgt,
			'--source=view3',
			'--start-node-id=20000000000',
			'--start-way-id=10000000000',
			'--write-timestamp',
			'--max-nodes-per-tile=0']
			, o
		)

		os.rename(glob.glob(os.path.join(o.pbf, o.area.id + '-SRTM*.osm.pbf'))[0], os.path.join(o.pbf, o.area.id + '-SRTM.osm.pbf'))

	else:
		say(_('Use previously generated contours'), o)


def getActualOsmconvert() -> None:
	return ('' if platform.system() == 'Windows' else './') + 'osmconvert' + platform.architecture()[0][0:2] + ('.exe' if platform.system() == 'Windows' else '')


def crop(o: Options) -> None:
	if o.crop or o.area.crop:
		if platform.system() == 'Windows' and platform.architecture()[0] == '32bit' and os.path.getsize(o.area.mapDataName) > 2000000000:
			raise ValueError(_('File for crop is too big') + ' (' + "{:.2f}".format(os.path.getsize(o.area.mapDataName) / 1000000000) + ' GB), ' + _('maximum is 2 GB. See GitHub for details.'))

		say(_('Creating crop of an area'), o)

		os.chdir('osmconvert')
		run([getActualOsmconvert(), # FIXME
			'../' + o.area.mapDataName,
			'-B=' + os.path.join(o.temp, 'polygon.poly'),
			'--complete-ways', '--complete-multipolygons', '--complete-boundaries',
			'--out-pbf',
			'-o=' + os.path.join(o.temp, o.area.id + '.osm.pbf')]
			, o
		)
		os.chdir('..')

		o.area.mapDataName = o.temp + o.area.id + '.osm.pbf'



def _prepareLicence(o: Options) -> None:
	# Create licence file
	say(_('Prepare license file'), o)
	with open('./template/license.txt', 'r') as license:
		content = license.read()

	with open(os.path.join(o.temp, 'license.txt'), 'w') as license:
		license.write( content + "\n" + str(o.area.timestamp))



def _splitFiles(o: Options) -> tuple[str, str]:
	input_file = o.area.mapDataName
	input_srtm_file = os.path.join(o.pbf, o.area.id + '-SRTM.osm.pbf')

	if o.split:
		say(_('Split files start'), o)
		try:
			splitter = os.path.join(sys._MEIPASS, 'splitter.jar')
		except Exception:
			splitter = './splitter-r' + str(o.splitter) + '/splitter.jar'

		# Data isn't exist or new one is downloaded
		if not os.path.exists(os.path.join(o.pbf, o.area.id + '-SPLITTED')) or o.downloaded:
			# Delete origin files
			for file in glob.glob(os.path.join(o.pbf, o.area.id + '-SPLITTED/*')):
				os.remove(file)

			run(['java', o.JAVAMEM, '-jar',
				splitter,
				input_file,
				'--max-areas=4096',
				'--max-nodes=1600000',
				'--output-dir=' + os.path.join(o.pbf, o.area.id + '-SPLITTED')]
				, o)

		# Update list of files
		input_file = os.path.join(o.pbf, o.area.id + '-SPLITTED/*.osm.pbf')

		# Split contour file
		if not os.path.isdir(os.path.join(o.pbf, o.area.id + '-SPLITTED-SRTM')):
			run(['java', o.JAVAMEM, '-jar',
				splitter,
				input_srtm_file,
				'--max-areas=4096',
				'--max-nodes=1600000',
				'--output-dir=' + os.path.join(o.pbf, o.area.id + '-SPLITTED-SRTM')]
				, o)

		say(_('Split files - DONE'), o)

		# Update list of srtm files
		input_srtm_file = os.path.join(o.pbf, o.area.id + '-SPLITTED-SRTM/*.osm.pbf')

	return input_file, input_srtm_file



def _makeBat(name: str, o: Options) -> None:
	say(_('Make ') + name + '.bat ' + _('file'), o)

	if name not in ['install', 'uninstall']:
		raise ValueError(_('Invalid bat file name'))

	# Convert ID to hex format
	numberHex = format(o.area.number, 'x')
	numberHex = numberHex[2:4] + numberHex[0:2]


	# Create installation bat script
	with open('./template/' + name + '.bat', 'r') as batFile:
		content = batFile.read()

	content = content.replace('%NAME%', o.area.nameCs)
	content = content.replace('%ID%', str(o.area.number).zfill(4))
	content = content.replace('%ID_HEX%', numberHex)

	with open(os.path.join(o.img, o.area.id + o.sufix, name + '.bat'), 'w') as batFile:
		batFile.write(content)


def _makeZip(o: Options) -> None:
	say(_('Make zip file'), o)

	os.chdir(o.img)
	zip = zipfile.ZipFile('./' + o.area.id + o.sufix + '.zip', 'w')
	for dirname, subdirs, files in os.walk('./' + o.area.id + o.sufix):
		zip.write( dirname )
		for filename in files:
			zip.write(os.path.join(dirname, filename))
	zip.close()
	os.chdir('..')



def _makeInfo(o: Options) -> None:
	say(_('Make info file'), o)

	infoData = {
		'ID':        o.area.id,
		'version':   str(o.VERSION),
		'datetime':  str(o.area.timestamp),
		'timestamp': str(int(o.area.timestamp.timestamp())),
		'hashImg':   _sha1(os.path.join(o.img, o.area.id + o.sufix + '.img')),
		'hashZip':   _sha1(os.path.join(o.img, o.area.id + o.sufix + '.zip')),
		'codePage':  o.code
	}

	with open(os.path.join(o.img, o.area.id + o.sufix + '.info'), 'w') as info:
		info.write(json.dumps(infoData))


def garmin(o: Options) -> None:
	say(_('Make map for Garmin...'), o )

	# Create subfolder
	if not os.path.exists(os.path.join(o.img, o.area.id + o.sufix)):
		os.makedirs(os.path.join(o.img, o.area.id + o.sufix))

	input_file, input_srtm_file = _splitFiles(o)

	_prepareLicence(o)

	mkgmap = if './mkgmap.jar' o.gui else ('./mkgmap-r' + str(o.mkgmap) + '/mkgmap.jar')
	mkgmapOptions = ['java', o.JAVAMEM, '-jar', mkgmap,
		'-c', './garmin-style/mkgmap-settings.conf',
		'--bounds=' + o.bounds,
		'--precomp-sea=' + os.path.join(o.sea, 'sea'),
		'--dem=' + os.path.join(o.hgt, 'VIEW3'),
		'--max-jobs=' + str( o.MAX_JOBS ),
		'--mapname=' + str(o.area.number).zfill(4) + '0001',
		'--overview-mapnumber=' + str(o.area.number).zfill(4) + '0000',
		'--family-id=' + str(o.area.number).zfill(4),
		'--description=' + o.area.nameCs + o.sufix,
		'--family-name=' + o.area.nameCs + o.sufix,
		'--series-name=' + o.area.nameCs + o.sufix,
		'--area-name=' + o.area.nameCs + o.sufix,
		'--country-name=' + o.area.nameCs + o.sufix,
		'--country-abbr=' + o.area.id,
		'--region-name=' + o.area.nameCs + o.sufix,
		'--region-abbr=' + o.area.id,
		'--product-version=' + str( o.VERSION ),
		'--output-dir=' + os.path.join(o.img, o.area.id + o.sufix),
		'--dem-poly=' + os.path.join(o.polygons, o.area.id + '.poly'),
		'--license-file=' + os.path.join(o.temp, 'license.txt')
	]

	if o.code == 'unicode':
		mkgmapOptions += ['--code-page=65001']
		o.code = '65001'
	elif o.code == 'ascii':
		pass
	else:
		mkgmapOptions += ['--code-page=' + o.code]

	mkgmapOptions += [
		input_file,
		input_srtm_file,
		'./garmin-style/style.txt'
	]
	mkgmapOptions += o.area.pois

	say(_('Generating map'), o)
	run(mkgmapOptions, o)

	_makeBat('install', o)
	_makeBat('uninstall', o)

	# Rename output file
	say(_('Rename files'), o)
	if os.path.isfile(os.path.join(o.img, o.area.id + o.sufix + '.img')):
		os.remove(os.path.join(o.img, o.area.id + o.sufix + '.img'))

	os.rename(os.path.join(o.img, o.area.id + o.sufix, 'gmapsupp.img'), os.path.join(o.img, o.area.id + o.sufix + '.img'))

	_makeZip(o)
	_makeInfo(o)
