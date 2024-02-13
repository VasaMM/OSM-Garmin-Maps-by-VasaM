import sys
from datetime import datetime
from makerfuncs.Lang import _


LOG_FILE_NAME = 'gmapmaker.log'


def say( msg, o, prefix = '[INFO] ', end = "\n"):
	if hasattr(o, 'quiet') and not o.quiet:
		print(prefix, msg, sep='', end = end)

	if hasattr(o, 'logFile'):
		if o.logFile is True:
			try:
				o.logFile = open(LOG_FILE_NAME, "w+")
			except:
				error(_("Nelze otevrit soubor ") + LOG_FILE_NAME, o)

		if o.logFile:
			o.logFile.write(prefix + msg + end)
			o.logFile.flush()


def log( msg, o ):
	if hasattr(o, 'logFile'):
		if o.logFile is True:
			try:
				o.logFile = open(LOG_FILE_NAME, "w+")
			except:
				error(_("Nelze otevrit soubor ") + LOG_FILE_NAME, o)

		if o.logFile:
			o.logFile.write(msg)
			o.logFile.flush()



def error( msg, o = None ):
	print( '[ERROR]', msg, file = sys.stderr )

	if o and o.logFile is True:
		try:
			o.logFile = open(LOG_FILE_NAME, "w+")
		except:
			error(_("Nelze otevrit soubor ") + LOG_FILE_NAME, o)

	if o and o.logFile:
		o.logFile.write('[ERROR] ' + msg + '\n' )
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
	runtime = 0
	timeEnd = datetime.now()
	if hasattr(o, 'timeStart'):
		runtime = timeEnd - o.timeStart

	say(_('Ukonceno v ') + str(timeEnd) + ', ' + _('doba behu') + ' ' + str(runtime), o)
	# print('\007')

	if hasattr(o, 'logFile') and o.logFile and o.logFile.close:
		o.logFile.close()