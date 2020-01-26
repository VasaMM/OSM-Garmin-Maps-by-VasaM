# Skript pro generování OSM map pro Garmin

## Licence
Licence CC BY 3.0 CZ, uveďte původ.

## Požadavky
* Java verze 8
* Python verze 3 (testováno na 3.6.8)
* Program [phyghtmap](http://katze.tfiu.de/projects/phyghtmap/), viz [instalace](#Instalace)
<!-- * Program [osmium](https://osmcode.org/osmium-tool/) -->

## Instalace
[*Jak zjistit, zda počítač používá 32bitovou nebo 64bitovou verzi operačního systému Windows*](https://support.microsoft.com/cs-cz/help/827218/how-to-determine-whether-a-computer-is-running-a-32-bit-version-or-64)

1) Nainstalujte python verze 3.6.8 (starší nebo novější verze může způsobovat problémy)
    1) [Odsud](https://www.python.org/downloads/release/python-368/) stáhněte instalátor pro windows. Doporučuji [Windows x86-64 web-based installer](https://www.python.org/ftp/python/3.6.8/python-3.6.8-amd64-webinstall.exe) pro 64bitový systém nebo [Windows x86 web-based installer](https://www.python.org/ftp/python/3.6.8/python-3.6.8-webinstall.exe) pro 32bitový systém. Přečtěte si další kroky a instalátor spusťte.
    2) Vyberte **Customize installation**. Zatrhněte **pip**, ostatní můžete odznačit. **Next**. Zatrhněte **Add python to enviroment variables** a **Precompile standart library**, ostatní nemusíte. **Install**.
    3) Na linuxu použijte `sudo apt install python3.7 python3-pip -y`

2) Nainstalujte javu verze 8 (pokud ji již máte, můžete přeskočit). [Zde](https://www.java.com/en/download/manual.jsp) stáhnete instalátor pro windows. Pokud máte 64bitový systém, doporučuji *Windows Offline (64-bit)*. Můžete použít výchozí nastavení instalace.

3) Spusťtě konzoli (na windows `Win + R`, napsat `cmd`, *OK*). Nainstalujte python moduly `pip install --user matplotlib==2.2.4 cycler==0.10.0 kiwisolver==1.1.0 numpy==1.16.3 pyparsing==2.4.0 python-dateutil==2.8.0 pytz==2019.1 six==1.12.0 beautifulsoup4==4.7.1 bs4==0.0.1 soupsieve==1.9.1 lxml`

4) [Odsud](http://katze.tfiu.de/projects/phyghtmap/download.html) stáhněte program *phyghtmap*. Doporučuji nejnovější verzi *source distribution*. Např. v květnu 2019 to je [phyghtmap_2.21.orig.tar.gz](phyghtmap_2.21.orig.tar.gz). **Pozor**, verze 2.21 obsahuje ve windows chybu, vytvořil jsem opravenou [kopii](http://www.osm.vasam.cz/phyghtmap-2.21_fixed.zip). Archiv rozbalte a ve složce se souborem *setup.py* spusťte konzoli (na windows např. pomocí zapsání příkazu `cmd` do adresního řádku průzkumníku). Příkazem `python setup.py install` nainstalujte *phyghtmap*. Pokud se zobrazí chyba informující o nepřítomnosti pythonu, [restartujte průkumník](https://wintip.cz/425-jak-restartovat-pruzkumnik-windows-proces-explorer-exe).

5) Ověřte si úspěšnost instalace příkazem `phyghtmap --version`. Mělo by se vám zobrazit `phyghtmap 2.21`. Pokud vše funguje, můžete rozbalený archiv smazat.
6) Uložte si obsah celého repozitáže (vpravo nahoře: *Clone or download*).
7) Rozbalte ho do míst, kde chcete generátor provozovat. Mapové soubory, které budou stahovány, zabírají stovky megabajtů, u velkých států jako Německo to mohou být i gigabajty, proto s tím počítejte. Na Windows 10 může být problém s antivirem, viz [zde](https://github.com/VasaMM/OSM-Garmin-Maps-by-VasaM/issues/2#issuecomment-532711693)
8) Ze stránek [http://www.mkgmap.org.uk](http://www.mkgmap.org.uk/download/mkgmap.html) stáhněte soubory *bounds.zip* a *sea.zip*.
9) Tyto soubory rozbalte do složek *bounds* a *sea*, bez dalších podsložek!
10) V souboru *makeMap.py* na prvních řádcích lze definovat maximální rozsah paměti RAM, povolený počet vláken procesoru a verzi mapy.


## Použití
Skript je nezvykle ukecaný (do budoucna je v plánu i "tichá" verze) a na začátku spuštění se uživatele ptá, co chce udělat. Proto jej stačí spustit bez parametrů: `./makeMap.py`.  
Pro bezobslužné automatické spouštění lze chování ovlivnit pomocí parametrů:
* `-a <stát>` nebo `--area <stát>` definuje stát (oblast), pro který je mapa generována. Viz [seznam států](#seznam-států)
* `-dy` nebo `--download_yes` vynutí vždy nové stažení mapových dat
* `-dn` nebo `--download_no` v případě, že byli dříve stažená mapová data, nebudou se znovu stahovat. **POZOR**, není nijak prováděna validace těchto dat, tedy jedná-li se o fragment z přechozího přerušeného stahování, dojde k chybě. Není-li zadáno *download_yes* nebo *download_no*, skript se zeptá.
* `-ns` nebo `--no_split` zakáže dělení mapových souborů na menší díly. Vhodné pouze u velmi malých oblastí a pro počítače s dostatkem RAM. 
* `-h` nebo `--help` zobrazí nápovědu.

## Seznam států
Státy jsou definovány ve skriptu *python/areas.py*. **Dodělat návod na přidání vlastního státu!**


### Hotové mapy
Hotové mapy najdete na stránce [http://www.osm.vasam.cz](http://www.osm.vasam.cz)


Chcete-li přidat další mapu či oblast, nejednoduší je zkopírovat existující a upravit ji. Nezapomeňte změnit ID na nějaké jiné. Pro vlastní mapy doporučuji jiné, než 88xx. Toto čislování budu používat pro mnou generované mapy a mohlo by dojít ke konfliktu.

**Pozor, tento skript používáte na vlastní riziko a já, jakožto autor nenesu žádnou odpovědnost za škody jim způsobené!**

Chyby, připomínky, návrhy hlašte v diskuzi na adrese [http://www.geocaching.cz/topic/31987-osm-topo-mapa-pro-garmin/](http://www.geocaching.cz/topic/31987-osm-topo-mapa-pro-garmin/).
