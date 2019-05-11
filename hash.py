#!/usr/bin/env python3

import os, sys, glob, zipfile, hashlib
import urllib.request
from shutil import copyfile
from datetime import datetime


def main():
	sha1 = hashlib.sha1()
	with open( "areas.py", 'rb') as f:
		while True:
			data = f.read( 67108864 )  # read 64Mb of file
			if not data:
				break
			sha1.update( data )

	hashed = sha1.hexdigest()
	print("SHA1:", hashed )



if __name__ == "__main__":
	main()