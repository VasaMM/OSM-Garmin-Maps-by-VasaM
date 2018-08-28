# Skript pro generování OSM map pro Garmin

## Požadavky
* Linux
* Java verze 8
* Python verze 3 (testováno na 3.4)
* Program [phyghtmap](http://katze.tfiu.de/projects/phyghtmap/)

## Instalace
1) Nejdříve splňte požadavky
2) Uložte si obsah celého repozitáže (vpravo nahoře: *Clone or download*). Mapové soubory, které budou stahovány, zabírají stovky megabajtů, u velkých států jako Německo to mohou být i gigabajty, proto s tím počítejte.
3) Ze stránek [http://www.mkgmap.org.uk](http://www.mkgmap.org.uk/download/mkgmap.html) stáhněte soubory *bounds.zip* a *sea.zip*.
4) Tyto soubory rozbalte do složek *bounds* a *sea*, bez dalších podsložek!
5) V souboru *mkaMap.sh* na prvních řádcích lze definovat verzi pythonu, maximální rozsah paměti RAM a číslo verze mapy.
6) Chcete-li, můžete aktualizovat programy **mkgmap** a **splitter** - NENÍ NUTNÉ.

## Použití
Skript je nezvykle ukecaný (do budoucna je v plánu i "tichá" verze) a na začátku spuštění se uživatele ptá, co chce udělat. Proto jej stačí spustit bez parametrů: `./makeMap.sh`.  
Pro bezobslužné automatické spouštění lze chování ovlivnit pomocí parametrů:
* `-a <stát>` nebo `--area <stát>` definuje stát (oblast), pro který je mapa generována. Viz [seznam států](#seznam-států)
* `-dy` nebo `--download_yes` vynutí vždy nové stažení mapových dat
* `-dn` nebo `--download_no` v případě, že byli dříve stažená mapová data, nebudou se znovu stahovat. **POZOR**, není nijak prováděna validace těchto dat, tedy jedná-li se o fragment z přechozího přerušeného stahování, dojde k chybě. Není-li zadáno *download_yes* nebo *download_no*, skript se zeptá.
* `-ns` nebo `--no_split` zakáže dělení mapových souborů na menší díly. Vhodné pouze u velmi malých oblastí a pro počítače s dostatkem RAM. 
* `-h` nebo `--help` zobrazí nápovědu.

## Seznam států
Státy jsou definovány ve skriptu *states.sh*. Příklad definice pro ČR:
* `CZ|cz )` - použitelné zkratky státu pro paramter `--area`, zde *CZ* a *cz*
* `echo "Tvorim mapu pro Ceskou republiku"` - Výpis na konzoly
* `STATE="CZ"` - Zkratka státu použitá v názvech souborů
* `DATA_URL="http://download.geofabrik.de/europe/czech-republic-latest.osm.pbf"` - Zdroj mapových dat, jsou-li mapová data stahována ručně, použijte `false`
* `POLY_URL="http://download.geofabrik.de/europe/czech-republic.poly"` - Zdroj hraničních polygonů, je-li polygon definován ručně, použijte `false`
* `COUNTRY_NAME="Ceska republika - VasaM"` - Název mapy vypsaný v GPS a BaseCamp
* `COUNTRY_ID=8801` - Jedinečné ID mapy
* `break`
* `;;`

Ve skriptu jsou defivány následující státy/oblasti:
* `OL` - Olomouc - vhodné pro testování
* `CZ` - Česká republika
* `SK` - Slovenská republika
* `UA` - Ukrajina
* `RO` - Rumunsko
* `NO` - Norsko
* `KG` - Kyrgyzstán
* `KZ` - Kazachstán

### Hotové mapy
Hotové mapy najdete na stránce [http://www.osmg.brazovic.cz/](http://www.osmg.brazovic.cz/)


Chcete-li přidat další mapu či oblast, nejednoduší je zkopírovat existjící a upravit ji. Nezapomeňte změnit ID na nějaké jiné. Pro vlastní mapy doporučuji jiné, než 88xx. Toto čislování budu používat pro mnou generované mapy a mohlo by dojít ke konfliktu.

**Pozor, tento skript používáte na vlastní riziko a já, jakožto autor nenesu žádnou odpovědnost za škody jim způsobené!**

Chyby, připomínky, návrhy hlašte v diskuzi na adrese [http://www.geocaching.cz/topic/31987-osm-topo-mapa-pro-garmin/](http://www.geocaching.cz/topic/31987-osm-topo-mapa-pro-garmin/).
