import os, sys, errno
from datetime import datetime, timezone
from math import floor
import urllib.request
from makerfuncs.Options import Options
from makerfuncs.prints import say
from makerfuncs import parser
from makerfuncs.Lang import _


def _makeBar(length: int, percent: int, done: str = '=', pointer: str = '>', fill: str = ' ', start: str = '[', end: str = ']') -> str:
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



def _printProgress(percent: int, size: int, length: int, speed: int, eta: str, unit: str, unitSize: int) -> None:
	bar = _makeBar(30, percent)

	sys.stdout.write("\r") # Clear to the end of line
	print("{0:3}%  {1}  {2} {6} / {3} {6}   {4:.2f} {6}/s   eta {5}      \r".format(percent, bar, size // unitSize, length // unitSize, speed, eta, unit), end='')



def download(url: str, output: str, quiet: bool = False) -> None:
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
			print(_("Download") + " '" + url + "'  ", length // unitSize, unit)  # Convert to MB
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
		print(_('Error code: '), e.code)
		raise

	except urllib.error.URLError as e:
		print(_('Reason: '), e.reason)
		raise



def mapData(o: Options):
	say(_('Start map data download'), o)
	o.downloaded = False

	# Check, if download is necessary
	if o.area.url is None:
		say(_('I don\'t have data url - skip downloading'), o)
		if not o.area.file:
			raise ValueError(_('Map file does NOT exist!'))
		return

	if o.downloadMap == 'skip':
		say(_('User set "--download skip" - skip downloading'), o)
		return

	if o.downloadMap == 'auto':
		if o.area.timestamp is None:
			o.downloaded = True
		else:
			diff = datetime.now(timezone.utc) - o.area.timestamp

			if diff.total_seconds() > o.maximumDataAge:
				o.downloaded = True
			else:
				say(_('Map data is to young - skip downloading'), o)


	if o.downloadMap == 'force' or o.downloaded is True:
		try:
			say(_('Downloading map data'), o)
			download(o.area.url, o.area.mapDataName)
			parser.fileHeader(o)

		except:
			raise ValueError(_('Can\'t download map data!'))



# Download polygon
def polygon(o: Options):
	if hasattr(o.area, 'continent') and not os.path.isfile(os.path.join(o.polygons, o.area.id + '.poly')):
		say(_('Download polygon'), o)
		download(o.area.url[0:-15] + '.poly', os.path.join(o.polygons, o.area.id + '.poly'))
