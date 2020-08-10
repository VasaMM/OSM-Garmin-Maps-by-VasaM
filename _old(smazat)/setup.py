from setuptools import setup

try:
	setup(
	    name='gmapmaker',
	    version='1.0',
	    description='Script for making OSM Garmin maps',
	    author='VasaM',
	    author_email='osm@vasam.cz',
	    license='CC BY 4.0',
	    url='https://github.com/VasaMM/OSM-Garmin-Maps-by-VasaM',
	    py_modules=['gmapmaker'],
	    packages=['makerfuncs'],
		entry_points={
			'console_scripts': [
				'gmapmaker = gmapmaker:main',
			],
		},
		install_requires=['osmium', 'pyclipper', 'geojson'],   #'click>=6'
	)
finally:
	print('Setup done')