#!/usr/bin/env python3

import os	# overit nutnost importu
import sys	# overit nutnost importu
from datetime import datetime, timedelta
import urllib.request

def makeBar( length, percent, done = '=', pointer = '>', fill = ' ', start = '[', end = ']' ):
	part_size = 100 / length

	output = start
	for i in range( length ):
		if percent == 100:
			output += done
		elif percent > part_size * ( i + 1):
			output += done
		elif percent > part_size * i:
			output += pointer
		else:
			output += fill

	return output + end

def printProgres( percent, size, length, speed, eta ):
	bar = makeBar( 30, percent )

	sys.stdout.write("\033[K") # Clear to the end of line
	print( "{0:3}%  {1}  {2} MB / {3} MB   {4} MB/s   eta {5}\r".format( percent, bar, size // 1048576, length // 1048576, speed, eta ), end='' )





def download( url, output ):
	# url = 'https://speed.hetzner.de/100MB.bin'
	# url = 'https://speed.hetzner.de/1GB.bin'

	output = open( output, 'wb' )

	response = urllib.request.urlopen( url )
	length = response.getheader( 'content-length' )

	if length:
		length = int( length )
		blocksize = max( 4096, length // 100 )
	else:
		blocksize = 1000000 # just made something up

	print( "Stahuji '" + url + "'  ", length // 1048576, "MB" )  # Prevedu na megabyte

	printProgres( 0, 0, length, 0, 0 )
	size = 0
	while True:
		tmp_time = datetime.now()
		
		data = response.read( blocksize )
		
		time_diff = ( datetime.now() - tmp_time ).total_seconds()

		if not data:
			break

		output.write( data )

		
		if length:
			size += len( data )
			percent = round( size / length * 100 )
			speed = round( ( blocksize // 1048576 ) / time_diff, 2 )
			eta = round( ( ( length - size ) // 1048576 ) / speed )  # v sekundach
			eta = str( timedelta( seconds = eta ) )

			printProgres( percent, size, length, speed, eta )

	print()
