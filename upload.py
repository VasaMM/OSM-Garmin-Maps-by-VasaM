 #!/usr/bin/env python3

# Nahraje hotová data na FTP server
# Ocekava soubor ftp.secret, kde na prvnim radku je adresa ftp serveru, na druhem uzivatelske jmeno a na tretim heslo

import sys, os
from ftplib import FTP
from makerfuncs.config import Configuration
from makerfuncs.Options import Options


def upload(states):
	if len(states) > 0:
		o = Options()

		config = Configuration()
		config.load()
		for key, item in config:
			setattr(o, key, item.getValue())

		print('Nacitam prihlasovaci udaje')
		with open( './ftp.secret', 'r' ) as secret:
			address, username, password = secret.read().splitlines()

		print('Pripojuji se na server', address)
		with FTP(address) as ftp:
			print('Prihlasuji se jako', username)
			ftp.login(user=username, passwd=password)

			for state in states:
				for suffix in ['.zip', '.img', '.info']:
					file = state + '_VasaM' + suffix

					print('Nahrávám', file)
					ftp.storbinary('STOR ' + file + '.uploading', open(os.path.join(o.img, file), 'rb'))

					print('Nahrávání dokončeno')
					ftp.rename(file + '.uploading', file)


def main():
	upload(sys.argv[1:])


if __name__ == "__main__":
	main()