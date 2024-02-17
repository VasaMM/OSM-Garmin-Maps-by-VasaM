import os, sys, errno
from datetime import datetime, timezone, timedelta
from math import floor
import urllib.request
from makerfuncs.prints import say, error
from makerfuncs import parser
from makerfuncs.Lang import _
import queue


def _makeBar(length, percent, done = '=', pointer = '>', fill = ' ', start = '[', end = ']'):
	part_size = 100 / length

	output = start
	for i in range(length):
		if percent == 100:
			output += done
		elif percent > part_size * (i + 1):
			output += done
		elif percent > part_size * i:
			output += pointer
		else:
			output += fill

	return output + end



def _printProgress(percent, size, length, speed, eta, unit, unitSize):
	bar = _makeBar(30, percent)

	sys.stdout.write("\r") # Clear to the end of line
	print("{0:3}%  {1}  {2} {6} / {3} {6}   {4:.2f} {6}/s   eta {5}      \r".format(percent, bar, size // unitSize, length // unitSize, speed, eta, unit), end='')



def download(url, output, quiet = False):
	# url = 'https://speed.hetzner.de/100MB.bin'
	# url = 'https://speed.hetzner.de/1GB.bin'

	if not os.path.exists(os.path.dirname(output)):
		try:
			os.makedirs(os.path.dirname(output))
		except OSError as exc:
			if exc.errno != errno.EEXIST:
				raise
	output = open(output, 'wb')

	try:
		response = urllib.request.urlopen(url)
		length = response.getheader('content-length')
		unit = 'MB'
		unitSize = 1048576

		if length:
			length = int(length)
			blocksize = max(4096, length // 1000)
			# blocksize = 4096 # just made something up
			# FIXME
			if length < unitSize:
				unit = 'kB'
				unitSize = 1024

		else:
			length = 0
			blocksize = 1000000 # just made something up


		if not quiet:
			print(_("Stahuji") + " '" + url + "'  ", length // unitSize, unit)  # Prevedu na megabyte
			_printProgress(0, 0, length, 0, 0, unit, unitSize)

		speedHistory = [0] * 10
		speedHistoryPointer = 0
		size = 0
		while True:
			tmp_time = datetime.now()

			data = response.read(blocksize)

			time_diff = (datetime.now() - tmp_time).total_seconds()

			if not data:
				if not quiet:
					_printProgress(100, length, length, 0, 0, unit, unitSize)
				break

			output.write(data)


			if length:
				size += len(data)
				percent = round(size / length * 100)
				speed = 0
				if time_diff != 0:
					# speed = round((blocksize / unitSize) / time_diff, 2)
					speedHistory[speedHistoryPointer] = (blocksize / unitSize) / time_diff
					speedHistoryPointer = (speedHistoryPointer + 1) % len(speedHistory)
					speed = round(sum(speedHistory) / len(speedHistory), 2)
				eta = 0
				if speed != 0:
					eta = round(((length - size) // unitSize) / speed)  # v sekundach
					if eta > 99:
						eta = str(floor(eta / 60)) + ' min ' + str(eta % 60) + ' s'
					else:
						eta = str(eta) + ' s'

				if not quiet:
					_printProgress(percent, size, length, speed, eta, unit, unitSize)

		if not quiet:
			print()

	except urllib.error.HTTPError as e:
		print('Error code: ', e.code)
		raise

	except urllib.error.URLError as e:
		print('Reason: ', e.reason)
		raise




def mapData(o):
	say(_('Spoustim stahovani mapovych dat'), o)
	o.downloaded = False

	# Zjistim, zda mam stahovat data
	if o.area.url is None:
		say(_('Neznam URL adresu - preskakuji'), o)
		if o.area.fileHeader is None:
			raise ValueError(_('Mapový soubor NEEXISTUJE!'))
		return

	if o.downloadMap == 'skip':
		say(_('Uzivatel nastavil "--download skip" - nestahuji'), o)
		return


	if o.downloadMap == 'auto':
		if o.area.timestamp is None:
			o.downloaded = True
		else:
			diff = datetime.now(timezone.utc) - o.area.timestamp

			if diff.total_seconds() > o.maximumDataAge:
				o.downloaded = True
			else:
				say(_('Mapova data jsou prilis mlada - nestahuji'), o)



	if o.downloadMap == 'force' or o.downloaded is True:
		try:
			say(_('Stahuji mapova data'), o)
			download(o.area.url, o.area.mapDataName, quiet=o.gui)
			parser.fileHeader(o)

		except:
			raise ValueError(_('Nelze stahnout mapova data!'))



# Stahnu polygon
def polygon(o):
	if hasattr(o.area, 'continent') and not os.path.isfile(o.polygons + o.area.id + '.poly'):
		say(_('Stahuji polygon'), o)
		download(o.area.url[0:-15] + '.poly', o.polygons + o.area.id + '.poly', quiet=o.gui)
