import os, sys
from datetime import datetime, timezone, timedelta
from math import floor
import urllib.request
from makerfuncs.prints import say, error



def makeBar(length, percent, done = '=', pointer = '>', fill = ' ', start = '[', end = ']'):
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



def printProgres(percent, size, length, speed, eta):
	bar = makeBar(30, percent)

	sys.stdout.write("\r") # Clear to the end of line
	print("{0:3}%  {1}  {2} MB / {3} MB   {4} MB/s   eta {5}      \r".format(percent, bar, size // 1048576, length // 1048576, speed, eta), end='')



def download(url, output, quiet = False):
	# url = 'https://speed.hetzner.de/100MB.bin'
	# url = 'https://speed.hetzner.de/1GB.bin'

	output = open(output, 'wb')

	response = urllib.request.urlopen(url)
	length = response.getheader('content-length')

	if length:
		length = int(length)
		blocksize = max(4096, length // 1000)
		# blocksize = 4096 # just made something up
		# FIXME
	else:
		blocksize = 1000000 # just made something up

	if not quiet:
		print("Stahuji '" + url + "'  ", length // 1048576, "MB")  # Prevedu na megabyte
		printProgres(0, 0, length, 0, 0)

	size = 0
	while True:
		tmp_time = datetime.now()
		
		data = response.read(blocksize)
		
		time_diff = (datetime.now() - tmp_time).total_seconds()

		if not data:
			break

		output.write(data)

		
		if length:
			size += len(data)
			percent = round(size / length * 100)
			speed = 0
			if time_diff != 0:
				speed = round((blocksize // 1048576) / time_diff, 2)
			eta = 0
			if speed != 0:
				eta = round(((length - size) // 1048576) / speed)  # v sekundach
				if eta > 99:
					eta = str(floor(eta / 60)) + ' min ' + str(eta % 60) + ' s'
				else:
					eta = str(eta) + ' s'

			if not quiet:
				printProgres(percent, size, length, speed, eta)

	if not quiet:
		print()


def mapData(o):
	say('Start map data download', o)
	# Zjistim, zda mam stahovat data
	if o.state.data_url is False or o.state.data_url is None:
		say('I don\'t have data url - skip downloading', o)
		if o.state.fileHeader is None:
			error('Map file does NOT exist!', o)
		return;

	if o.downloadMap is 'skip':
		say('User set "--download skip" - skip downloading', o)
		return;


	downloadData = False
	if o.downloadMap is 'auto':
		if o.state.timestamp is None:
			downloadData = True
		else:
			diff = datetime.now(timezone.utc) - o.state.timestamp

			if diff.total_seconds() > o.maximumDataAge:
				downloadData = True
			else:
				say('Map data is to young - skip downloading', o)
	


	if o.downloadMap is 'force' or downloadData is True:
		try:
			say('Downloading map data', o)
			download(o.state.data_url, './pbf/' + o.state.data_id + '.osm.pbf')
			parser.fileHeader(o)

		except:
			error("Cann't download map data!", o)



# Stahnu polygon
def polygon(o):
	try:
		if not os.path.isfile('./poly/' + o.state.data_id + '.poly'):
			if o.state.poly_url is False or o.state.poly_url is None:
				error("Polygon '" + o.state.data_id + "' does NOT exist!", o)

			say('Downloading polygon', o)
			download(o.state.poly_url, './poly/' + o.state.data_id + '.poly')
	except:
		error("Cann't download polygon!", o)