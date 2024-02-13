 #!/usr/bin/env python3

# Nahraje hotová data na FTP server
# Ocekava soubor ftp.secret, kde na prvnim radku je adresa ftp serveru, na druhem uzivatelske jmeno a na tretim heslo

import sys, os
from ftplib import FTP
from makerfuncs import config
from makerfuncs.download import _makeBar, _printProgres



class Options:
	pass

def upload(states):
	if len(states) > 0:
		o = Options()
		config.load(o)

		print('Nacitam prihlasovaci udaje')
		with open( './ftp.secret', 'r' ) as secret:
			address, username, password = secret.read().splitlines()

		print('Pripojuji se na server', address)
		with FTP(address) as ftp:
			print('Prihlasuji se jako', username)
			ftp.login(user=username, passwd=password)

			for state in states:
				for suffix in ['.zip', '.img', '.info']:
					bytesInMB = 1048576

					file = state + '_VasaM' + suffix
					fileSize = os.stat(o.img + file).st_size
					blockSize = 8192

					class ProgressBar:
						uploaded = 0

						def update(self, _):
							self.uploaded += blockSize
							# TODO Calculate speed and ETA
							_printProgres(round(self.uploaded / fileSize * 100), self.uploaded, fileSize, 0, 0, 'MB', 1048576)

						def finish(self):
							_printProgres(100, fileSize, fileSize, 0, 0, 'MB', 1048576)
							print()

					progressBar = ProgressBar()

					print(f'Nahrávám {file} ({fileSize // bytesInMB} MB)')
					ftp.storbinary('STOR ' + file + '.uploading', open(o.img + file, 'rb'), blockSize, progressBar.update)

					progressBar.finish()

					print('Nahrávání dokončeno')
					ftp.rename(file + '.uploading', file)


def main():
	upload(sys.argv[1:])


if __name__ == "__main__":
	main()