import sys
from datetime import datetime
from makerfuncs.Lang import _
from makerfuncs.Options import Options


def _openLogFile(o: Options) -> None:
    if not hasattr(o, 'logFileHandler') or (hasattr(o, 'logFileHandler') and not o.logFileHandler):
        try:
            o.logFileHandler = open(o.logFile, 'w+')
        except:
            error(_('Can\'t open file ') + o.logFile, o)


def _closeLogFile(o: Options) -> None:
    if hasattr(o, 'logFileHandler') and o.logFileHandler and o.logFileHandler.close:
        o.logFileHandler.close()


def _writeToLogFile(o: Options, msg: str) -> None:
    if hasattr(o, 'logFile') and o.logFile is not False:
        _openLogFile(o)

        o.logFileHandler.write(msg)
        o.logFileHandler.flush()


def say(msg: str, o: Options, prefix: str = '[INFO] ', end: str = '\n') -> None:
    if hasattr(o, 'quiet') and not o.quiet:
        print(prefix, msg, sep='', end=end)

    _writeToLogFile(o, prefix + msg + end)


def log(msg: str, o: Options) -> None:
    _writeToLogFile(o, msg)


def error(msg: str, o: Options = None) -> None:
    print('[ERROR]', msg, file=sys.stderr)
    _writeToLogFile(o, '[ERROR] ' + msg + '\n')


def end(o: Options) -> None:
    runtime = 0
    timeEnd = datetime.now()
    if hasattr(o, 'timeStart'):
        runtime = timeEnd - o.timeStart

    say(_('End at ') + str(timeEnd) + ', ' +
        _('runtime') + ' ' + str(runtime), o)
    # print('\007')

    _closeLogFile(o)
