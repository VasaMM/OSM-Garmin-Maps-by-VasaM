import sys
from datetime import datetime


def say( msg, o ):
	if not o.quiet:
		print( '[INFO]', msg )

	if o.logFile is True:
		try:
			o.logFile = open("makeMap.log", "w+")
		except:
			error("Cann't open file 'makeMap.log'", o)
	
	if o.logFile:
		o.logFile.write( '[INFO] ' + msg + '\n' )
		o.logFile.flush()



def error( msg, o = None ):
	print( '[ERROR]', msg, file = sys.stderr )

	if o and o.logFile is True:
		try:
			o.logFile = open("makeMap.log", "w+")
		except:
			error("Cann't open file 'makeMap.log'", o)
	
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