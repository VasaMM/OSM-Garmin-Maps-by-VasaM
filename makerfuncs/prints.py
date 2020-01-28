import sys
from datetime import datetime

LOG_FILE_NAME = 'gmapmaker.log'


def say( msg, o ):
	if not o.quiet:
		print( '[INFO]', msg )

	if o.logFile is True:
		try:
			o.logFile = open(LOG_FILE_NAME, "w+")
		except:
			error("Cann't open file " + LOG_FILE_NAME, o)
	
	if o.logFile:
		o.logFile.write( '[INFO] ' + msg + '\n' )
		o.logFile.flush()


def log( msg, o ):
	if o.logFile is True:
		try:
			o.logFile = open(LOG_FILE_NAME, "w+")
		except:
			error("Cann't open file " + LOG_FILE_NAME, o)
	
	if o.logFile:
		o.logFile.write(msg)
		o.logFile.flush()



def error( msg, o = None ):
	print( '[ERROR]', msg, file = sys.stderr )

	if o and o.logFile is True:
		try:
			o.logFile = open(LOG_FILE_NAME, "w+")
		except:
			error("Cann't open file " + LOG_FILE_NAME, o)
	
	if o and o.logFile:
		o.logFile.write( '[ERROR] ' + msg + '\n' )
		o.logFile.flush()




# def question( msg ):
# 	while True:
# 		answer = input( msg + ' [Y/n] ' )
# 		if answer in ( 'Y', 'y' ):
# 			return False
# 		elif answer in ( 'N', 'n' ):
# 			return True
# 		else:
# 			print ( 'Invalid input, try it again...' )


# Ukoncovaci funkce
def end(o):
	timeEnd = datetime.now()
	runtime = timeEnd - o.time_start
	say('Konec v ' + str(timeEnd) + ', beh ' + str(runtime), o)
	print('\007')