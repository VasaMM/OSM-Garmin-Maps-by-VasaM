# Skript pro generování OSM map pro Garmin

## Licence
[![Licence Creative Commons](https://i.creativecommons.org/l/by/4.0/88x31.png)](http://creativecommons.org/licenses/by/4.0/)  
Toto dílo podléhá licenci [Creative Commons Uveďte původ 4.0 Mezinárodní License](http://creativecommons.org/licenses/by/4.0/).

## Požadavky
* Java verze 8
* Python verze 3 (testováno na 3.8.5)
* Program [phyghtmap](http://katze.tfiu.de/projects/phyghtmap/), viz [instalace](#Instalace)
<!-- * Program [osmium](https://osmcode.org/osmium-tool/) -->

## Instalace
Pokud si při instalaci nebudete vědět s něčím rady nebo se vyskytnou nějké probémy, podívejte se do [FAQ pro instalaci](#faq-pro-instalaci)

1) Nainstalujte python 3
    1) [Odsud](https://www.python.org/downloads/) stáhněte instalátor (tlačítko pod nápisem *Download the latest version for Windows*) a spusťte ho.
    2) Zatrhněte **Add Python to PATH** a tařítkem *Install Now*, spusťte instalaci.
    3) Na linuxu použijte `sudo apt install python3 python3-pip -y`

2) Nainstalujte javu verze 8
	1) [Zde](https://www.java.com/en/download/manual.jsp) stáhnete instalátor pro windows. Pokud máte 64bitový systém, doporučuji *Windows Offline (64-bit)*. Můžete použít výchozí nastavení instalace.
	2) Pro linux použijte `sudo apt install default-jre -y`

3) Nainstalujte phyghtmap
	1) [Odsud](http://katze.tfiu.de/projects/phyghtmap/download.html) stáhněte program *phyghtmap*. Doporučuji nejnovější verzi *source distribution*. Např. v květnu 2019 to je -*phyghtmap_2.21.orig.tar.gz*. **Pozor**, verze 2.21 obsahuje ve windows chybu, vytvořil jsem opravenou [kopii](http://www.garmin.vasam.cz/downloads/phyghtmap-2.21_fixed.zip).
	2) Archiv rozbalte a ve složce se souborem *setup.py* spusťte konzoli.
	3) Příkazem `pip3 install matplotlib==2.2.5 bs4 lxml` nainstalujte potřebné knihovny.
	4) Příkazem `python setup.py install` nainstalujte *phyghtmap*.
	5) Ověřte si úspěšnost instalace příkazem `phyghtmap --version`. Mělo by se vám zobrazit `phyghtmap 2.21`. Pokud vše funguje, můžete rozbalený archiv smazat.

4) Nainstalujte tento skript *gmapmaker*
	1) Uložte si obsah celého repozitáže (vpravo nahoře: *Code* - *Download ZIP*).
	2) Archiv rozbalte v místě, kde chcete generátor provozovat. Mapové soubory, které budou stahovány, zabírají stovky megabajtů, u velkých států jako Německo to mohou být i gigabajty, proto s tím počítejte.
	3) Příkazem `pip3 install osmium pyclipper geojson` nainstalujte potřebné knihovny.

5) Proveďte inicializaci skriptu pomocí `python prepare.py`.
	* Přeskočením odpovědi (klávesa *enter*) se použije výchozí nastavení.
	* Tento skript automaticky stáhne potřebné soubory ([sea](https://www.mkgmap.org.uk/download/mkgmap.html) a [bounds](https://www.mkgmap.org.uk/download/mkgmap.html)) a programy([mkgmap](https://www.mkgmap.org.uk/download/mkgmap.html), [splitter](https://www.mkgmap.org.uk/download/splitter.html) a [Osmconvert](https://wiki.openstreetmap.org/wiki/Osmconvert#Binaries)) - celkem cca 1,5 GB. Případná aktualizace je možná pomocí `python update.py`.
	* Vhodná verze programu *Osmconvert* (Windows/Linux a 32bit/64bit) je detekována automaticky. Pokud ke skriptu *gmapmaker* přistupujete z různých systémů, je nutné spustit `python update.py` v každém z nich. Omezení systému Windows zároveň neumožňuje programu *Osmconvert* zpracovat soubory větší než 2GB. Tento program slouží k vytvoření výřezu (přepínače `--crop` a `--extend`), proto je nutné pro větší oblasti (většina států) použít buď systém Linux nebo si stáhnout speciální verzi [inary for Windows 64 bit](https://wiki.openstreetmap.org/wiki/Osmconvert#Windows) a tou nahradit automaticky stažená soubor *osmconvert64.exe*. **POZOR** toto funguje jen pro 64 bitový systém Windows, pro 32 bitový systém Windows řešení není. Linuxu se tento problém netýká.
	
6) Ověřte si funkčnost skriptu příkazem `python gmapmaker.py --version`.

7) V souboru *gmapmaker.py* na prvních řádcích lze definovat maximální rozsah paměti RAM, povolený počet vláken procesoru a verzi mapy. (**FIXME** v budoucnu bude přesunuto do skriptu *prepare*).

### FAQ pro instalaci
* [*Jak zjistit, zda počítač používá 32bitovou nebo 64bitovou verzi operačního systému Windows*](https://support.microsoft.com/cs-cz/help/827218/how-to-determine-whether-a-computer-is-running-a-32-bit-version-or-64)
* Konzoli na windows spustíte následovně: `Win + R`, napsat `cmd`, *OK*. Druhou možností je napsat `cmd` přímo do adresního řádku průzkuníku.
* Na linuxu může být pro nástroj pip3 (popř. i pro python setup.py) vyžadován přepínač `--user` (`pip3 install --user name1 name2`) nebo `sudo` (`sudo pip3 install name1 name2`).
* Pokud se zobrazí chyba informující o nepřítomnosti pythonu, [restartujte průkumník](https://wintip.cz/425-jak-restartovat-pruzkumnik-windows-proces-explorer-exe).
* Instalace knihovny *matplotlib* může způsobovat problémy. V tom případě si stáhněte upravený instalátor ze [těchto stránek](https://www.lfd.uci.edu/~gohlke/pythonlibs/#matplotlib). Verzi vyberte podle vašeho systému (32bit vs 64bit) a verze pythou (pro python 3.8.5 je to cp38). Nezapomeňte, že potřebujete starší verzi matplotlib a to 2.2.5. Ve složce se staženým soubor spusťe následující příkaz `pip3 install <jméno souboru>`.
* Na Windows 10 může být problém s antivirem, viz [zde](https://github.com/VasaMM/OSM-Garmin-Maps-by-VasaM/issues/2#issuecomment-532711693).


## Použití
Je-li skript spuštěn bez parametrů `python ./gmapmaker.py` vyžádá si od uživatele jméno generované oblasti. Pro bezobslužnou instalaci ho lze (a i další vlastnosti) předem definovat pomocí následujících parametrů:
* `-a <area>`, `--area <area>` definuje stát (oblast), pro který je mapa generována. Viz [seznam států](https://github.com/VasaMM/OSM-Garmin-Maps-by-VasaM/blob/dev/makerfuncs/states.py).
* `-c <codePage>`, `--code-page <codePage>` kódování mapy (*unicode*, *ascii*, *1250*, *1252*, *latin2*).
* `-d <opt>`, `--download <opt>` princip stahování mapových dat:
	* *force* - Mapová data se při každém spuštění znovu stáhnou.
	* *skip* - Mapová data se nebudou stahovat.
	* *auto* - Mapová data se stáhnou pouze pokud jsou starší než --maximum-date-age (**výchozí**).
* `--maximum-data-age <age>` určuje maximální stáří mapovyýh dat při automatickém stahování. Hodnota ve tvaru [0-9]+[hdm], kde *h* značí hodinu, *d* značí den (24 hodin) a m značí měsíc (30 dní) (**výchozí hodnota 1d**).
* `--map-number <number>` vynutí konkretní map ID.
* `--variant <variant>` vynutí konkretní variantu mapy (hodnota 1 - 5). Varianta mapy ovlivňuje její ID. Jinka je generována automaticky.
* `-e <km>`, `--extend <km>` zvětší polygon o zadaný počet kilometrů (**POZOR, zatím nefunguje**).
* `--sufix <sufix>` přípona za jménem mapy.
* `--no-split` zakáže dělení mapy na podsoubory - vhodné jen pro velmi malé oblasti.
* `-r`, `--crop` ořízne mapový soubor podle polygonu.
* `-q`, `--quiet` žádné výpisy na stdout.
* `-l`, `--logging` vytvoří logovací soubor *gmapmaker.log*.
* `-h`, `--help` zobrazí nápovědu.


## Seznam států
Státy jsou definovány ve skriptu *python/areas.py*. Vlastní oblasti lze definovat v souboru *userAreas/myAreas.py* (ten je vytvořen až skriptem *prepare*, tudíž by měl být imunní vůči přepsání při aktualizaci i opětovnému spuštění zmíněného skriptu). Doporučuji vycházet z předpřipravené oblasti *OL* definující okres Olomouc. Pro každou novou oblast je nutné zadefinovat nový objekt třídy *Area* (definována v *makerfuncs/Area.py*). K mapě lze definovat následující vlastnosti:
* `nameCs` jméno mapy česky
* `nameEn` jméno mapy anglicky (je-li prázdné, použije se `nameCs`)
* `number` garmin ID mapy. Čtyřmístné číslo, mělo by být unikátní.
* `pois` pole se jmény souborů obsahující dodatečné POI, které budou vloženy do mapy. Tyto soubory se musí nacházet ve složce *pois*.
* `parent` rodičovská mapa, vhodné pro vytváření podoblastí z různých států (budou automaticky stažena/použita mapová data rodiče)
* `crop` výchozí `False`, `True` vynutí oříznutí dat podle polygonu (**POZOR, zatím nefunguje**).

Dále je nutné připravit polygon a to buď ve formátu *.poly* nebo *.geojson* a umístit ho pod stejným názvem do složky s polygony. Mapová data je pak nutné buď také stáhnout a nachystat do patřičné složky nebo definovat rodiče (viz výše). 


### Hotové mapy
Hotové mapy najdete na stránce [http://www.garmin.vasam.cz](http://www.garmin.vasam.cz)


**Pozor, tento skript používáte na vlastní riziko a já, jakožto autor nenesu žádnou odpovědnost za škody jim způsobené!**

Chyby, připomínky, návrhy hlašte v diskuzi na adrese [http://www.geocaching.cz/topic/31987-osm-topo-mapa-pro-garmin/](http://www.geocaching.cz/topic/31987-osm-topo-mapa-pro-garmin/).
