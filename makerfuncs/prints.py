import sys
from datetime import datetime
from makerfuncs.Lang import _
from makerfuncs.Options import Options

LOG_FILE_NAME = 'gmapmaker.log'


def say(msg: str, o: Options, prefix: str = '[INFO] ', end: str = '\n') -> None:
    if hasattr(o, 'quiet') and not o.quiet:
        print(prefix, msg, sep='', end=end)

    if hasattr(o, 'logFile'):
        if o.logFile is True:
            try:
                o.logFile = open(LOG_FILE_NAME, 'w+')
            except:
                error(_('Can\'t open file ') + LOG_FILE_NAME, o)

        if o.logFile:
            o.logFile.write(prefix + msg + end)
            o.logFile.flush()


def log(msg: str, o: Options) -> None:
    if hasattr(o, 'logFile'):
        if o.logFile is True:
            try:
                o.logFile = open(LOG_FILE_NAME, 'w+')
            except:
                error(_('Can\'t open file ') + LOG_FILE_NAME, o)

        if o.logFile:
            o.logFile.write(msg)
            o.logFile.flush()


def error(msg: str, o: Options = None) -> None:
    print('[ERROR]', msg, file=sys.stderr)

    if o and o.logFile is True:
        try:
            o.logFile = open(LOG_FILE_NAME, 'w+')
        except:
            error(_('Can\'t open file ') + LOG_FILE_NAME, o)

    if o and o.logFile:
        o.logFile.write('[ERROR] ' + msg + '\n')
        o.logFile.flush()


def end(o: Options) -> None:
    runtime = 0
    timeEnd = datetime.now()
    if hasattr(o, 'timeStart'):
        runtime = timeEnd - o.timeStart

    say(_('End at ') + str(timeEnd) + ', ' +
        _('runtime') + ' ' + str(runtime), o)
    # print('\007')

    if hasattr(o, 'logFile') and o.logFile and o.logFile.close:
        o.logFile.close()
