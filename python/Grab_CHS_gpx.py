# Skript postupne projde vsechny lezecke oblasti na strankach CHS
# Ke kazde skale stahne jeji GPS souradnice, jmeno, rating, obtiznost a odkaz na stranky CHS k dane skale
# Skript je optimalizovan pro Locus Map

import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from time import localtime, strftime

with open('skaly.gpx', 'w') as output:

    output.write('<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n')
    output.write('<gpx version="1.1"\n')
    output.write(' xmlns="http://www.topografix.com/GPX/1/1"\n')
    output.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n')
    output.write(' xsi:schemaLocation="http://www.topografix.com/GPX/1/1 ')
    output.write('http://www.topografix.com/GPX/1/1/gpx.xsd"\n')
    output.write(' xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions')
    output.write('/v3"\n')
    output.write(' xmlns:gpxtrkx="http://www.garmin.com/xmlschemas/')
    output.write('TrackStatsExtension/v1"\n')
    output.write(' xmlns:gpxtpx="http://www.garmin.com/xmlschemas/')
    output.write('TrackPointExtension/v2"\n')
    output.write('xmlns:locus="http://www.locusmap.eu">')
    output.write('<metadata>\n')
    output.write('<desc>Czech rock climbing areas</desc>\n')
    output.write('</metadata>\n')

    # Pocet sklanich oblasti
    rockCount = 18000

    for i in range(1, rockCount + 1):

        try:
            page_url = 'https://www.horosvaz.cz/skaly-skala-' + str(i)
            page = urlopen(page_url)
        except:
            print(i, ':', sep='')
            continue

        # Rozdelim html
        soup = BeautifulSoup(page, 'html.parser')

        # Ziskam jmeno skaly
        name_box = soup.find('h1', attrs={'class': 'menu5 small-h1'})
        name = name_box.text.strip()

        # Ziskam cas vytvoreni
        timestamp = strftime('%Y-%m-%dT%H:%M:%S.000Z', localtime())

        # Ziskam jmeno sektoru
        sector_name_box = soup.find('a', attrs={'class': 'skaly-parent tt'})
        sector_name = sector_name_box.text.strip()

        # Ziskam hodnoceni
        rating_box = soup.find('div', attrs={'class': 'top-ratings-stars'})
        rating = int(rating_box.attrs['title'][11])

        # Ziskam zakaz
        ban_box = soup.find('span', attrs={'class': 'zakaz tt'})
        ban = ban_box is not None

        # Ziskam pocet cest jednotlivych narocnosti a jejich median
        difficulty_box = soup.find('div', attrs={'class': 'sgraph tt big'})
        difficulty_string = difficulty_box.attrs['title']
        difficulty = [0 for j in range(12)]
        key = -1
        value = ""
        ways_count = 0
        for ch in difficulty_string:
            if ch.isdigit():
                if key == -1:
                    key = int(ch) - 1
                else:
                    value += ch
            elif ch == 'x':
                val = int(value)
                difficulty[key] = val
                ways_count += val
                key = -1
                value = ""
        median_pos = ways_count // 2
        cur_pos = 0
        median = 0
        for j in range(12):
            cur_pos += difficulty[j]
            if cur_pos >= median_pos:
                median = j + 1
                break

        # Ziskam souradnice
        coordinates_box = soup.find('a', attrs={'class': 'map mapycz'})
        if coordinates_box is None:
            print(i, ':  ', sector_name, name, sep='')
            continue

        coordinates = coordinates_box.attrs['href']
        m = re.search('y=([0-9]+.[0-9]+)&x=([0-9]+.[0-9]+)', coordinates)
        coordinates = (m.group(1), m.group(2))

        # Vytisknu vysledek a pridam ho do vystupniho souboru
        print(i, ':  ', sector_name, '-', name, '  (N ', coordinates[0], ' E ',
              coordinates[1], ')', sep='')
        output.write('<wpt lat="{}" lon="{}">\n'.
                     format(coordinates[0], coordinates[1]))
        output.write('<time>{}</time>\n'.format(timestamp))
        if sector_name != name:
            output.write('<name>{} - {}</name>\n'.format(sector_name, name))
        else:
            output.write('<name>{}</name>\n'.format(name))
        output.write('<desc><![CDATA[')
        if ban:
            output.write('CLIMBING FORBIDDEN!\n')
        if rating != 0:
            output.write('Rating: {}\n'.format('*' * rating))
        output.write('Difficulty (UIAA):\n')
        for k in range(12):
            output.write(('  {}:' if k < 9 else ' {}:').format(k + 1))
            output.write('#' * difficulty[k])
            output.write('\n')
        output.write('\n{}]]></desc>\n'.format(page_url))
        if ban:
            output.write('<sym>trngl_rd_hscc</sym>\n')
            output.write('<extensions>\n')
            output.write('<locus:icon>file:geometric_shapes_shodyrev_icons')
            output.write('.zip:trngl_rd_hscc.png</locus:icon>\n')
            output.write('</extensions>\n')
        elif median <= 4:
            output.write('<sym>trngl_bl_hscc</sym>\n')
            output.write('<extensions>\n')
            output.write('<locus:icon>file:geometric_shapes_shodyrev_icons')
            output.write('.zip:trngl_bl_hscc.png</locus:icon>\n')
            output.write('</extensions>\n')
        elif median == 5:
            output.write('<sym>trngl_blblbl_hscc</sym>\n')
            output.write('<extensions>\n')
            output.write('<locus:icon>file:geometric_shapes_shodyrev_icons')
            output.write('.zip:trngl_blblbl_hscc.png</locus:icon>\n')
            output.write('</extensions>\n')
        elif median >= 6:
            output.write('<sym>trngl_blbl_hscc</sym>\n')
            output.write('<extensions>\n')
            output.write('<locus:icon>file:geometric_shapes_shodyrev_icons')
            output.write('.zip:trngl_blbl_hscc.png</locus:icon>\n')
            output.write('</extensions>\n')
        output.write('</wpt>\n')
    output.write('</gpx>')
print('Complete!')
