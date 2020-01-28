from setuptools import setup

setup(
    name='gmapmaker',
    version='0.1',
    description='Script for making OSM Garmin maps',
    author='VasaM',
    author_email='osm@vasam.cz',
    license='CC BY 3.0',
    url='https://github.com/VasaMM/OSM-Garmin-Maps-by-VasaM',
    packages=['makerfuncs'],
	entry_points={
		'console_scripts': [
			'gmapmaker = gmapmaker:main',
		],
	},
)