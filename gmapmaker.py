from datetime import datetime
import traceback

from makerfuncs import args, parser, download, polygon, generator
from makerfuncs.config import Configuration
from makerfuncs.Options import Options
from makerfuncs.prints import say, error, end
from makerfuncs.Lang import Lang, _


def main():
	# Object with configuration and options
	o = Options()
	o.JAVAMEM  = '-Xmx4g' # Maximum amount of available RAM, see https://stackoverflow.com/questions/14763079/what-are-the-xms-and-xmx-parameters-when-starting-jvm
	o.MAX_JOBS = 4        # Maximum od cores
	o.VERSION  = 110      # Version


	try:
		# TODO Create TMP folder

		# Load config file and copy values to options
		config = Configuration()
		config.load()
		for key, item in config:
			setattr(o, key, item.getValue())

		# Load arguments
		args.parse(o)

		# Set english language
		if o.en:
			Lang.bindLanguage('en')

		# Record the start time
		o.timeStart = datetime.now()
		say(_('Start at ') + str(o.timeStart), o)

		# Gen info about area
		parser.area(o)

		# Load info from file header
		parser.fileHeader(o)

		# Download area map data
		download.mapData(o)

		# Download polygon
		download.polygon(o)

		# Parse polygon
		polygon.load(o)

		# Create contours
		generator.contours(o)

		# Crop map data
		generator.crop(o)

		# Generate garmin maps
		generator.garmin(o)

		# TODO Remove temp


	except KeyboardInterrupt:
		error("\n" + _('Terminated by user'))


	except Exception as e:
		print(traceback.format_exc())
		error(str(e))
		exit(1)


	finally:
		# End generation
		end(o)


if __name__ == "__main__":
	main()