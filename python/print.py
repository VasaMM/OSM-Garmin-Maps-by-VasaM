import sys
# import os, sys, glob, zipfile, hashlib
# import urllib.request
# from shutil import copyfile
# from datetime import datetime


def say( msg, o ):
	if not o.quiet:
		print( '[INFO]', msg )

	if o.log_file:
		o.log_file.write( '[INFO] ' + msg + '\n' )



def error( msg, o = None ):
	print( '[ERROR]', msg, file = sys.stderr )
	
	if o and o.log_file:
		o.log_file.write( '[ERROR] ' + msg + '\n' )




def question( msg ):
	while True:
		answer = input( msg + ' [Y/n] ' )
		if answer in ( 'Y', 'y' ):
			return False
		elif answer in ( 'N', 'n' ):
			return True
		else:
			print ( 'Invalid input, try it again...' )