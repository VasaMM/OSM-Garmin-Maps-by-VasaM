 #!/usr/bin/env python3

#  Skript pro dávkové generování map
# Jako parametry jsou předány kódy jednotlivých států, ty jsou postupně vygenerovány a nahrány na web

import sys, os
from upload import upload


def getPython():
	if os.system('python3.8 --version') == 0:
		return 'python3.8'
	elif os.system('python --version') == 0:
		return 'python'
	else:
		print('Nenalezen python')
		exit()


def main():
	python = getPython()

	if len(sys.argv) > 1:
		for state in sys.argv[1:]:
			print('Generuji mapu', state)

			# FIXME elegantneji
			print(python + ' gmapmaker.py --logging --area ' + state)
			ret = os.system(python + ' gmapmaker.py --logging --area ' + state)

			# TODO Spustit jako druhe vlakno
			if ret == 0:
				upload([state])
			else:
				exit()


if __name__ == "__main__":
	main()