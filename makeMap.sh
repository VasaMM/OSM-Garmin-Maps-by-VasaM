#!/bin/bash

# Prihlasovaci udaje pro https://ers.cr.usgs.gov/
USER=VasaM
PASS=Password123

# Dalsi nastevni
PYTHON=python3.4


# Ukoncovaci funkce
function end {
	TMP=$(date)
	END=$(date +%s)
	RUNTIME=$((END-START))
	echo ""
	eval "echo Konec v ${TMP}, beh $(date -ud "@$RUNTIME" +'%H hodin %M minut %S sekund')"
	echo -en "\007" # Pipnu na konec, pripadne zakomentovat
	exit
}

function viewHelp {
	echo "NAPOVEDA"
	echo ""
	echo "# Skript pro generování OSM map pro Garmin"
	echo ""
	echo "## Požadavky"
	echo "	* Linux"
	echo "	* Java verze 8"
	echo "	* Python verze 3 (testováno na 3.4)"
	echo "	* Program [phyghtmap](http://katze.tfiu.de/projects/phyghtmap/)"
	echo ""
	echo "## Instalace"
	echo "	1) Nejdříve splňte požadavky"
	echo "	2) Uložte si obsah celého repozitáže (vpravo nahoře: *Clone or download*). Mapové soubory, které budou stahovány, zabírají stovky megabajtů, u velkých států jako Německo to mohou být i gigabajty, proto s tím počítejte."
	echo "	3) Ze stránek [http://www.mkgmap.org.uk](http://www.mkgmap.org.uk/download/mkgmap.html) stáhněte soubory *bounds.zip* a *sea.zip*."
	echo "	4) Tyto soubory rozbalte do složek *bounds* a *sea*, bez dalších podsložek!"
	echo "	5) Chcete-li, můžete aktualizovat programy **mkgmap** a **splitter** - NENÍ NUTNÉ."
	echo ""
	echo "## Použití"
	echo "	Skript je nezvykle ukecaný (do budoucna je v plánu i \"tichá\" verze) a na začátku spuštění se uživatle ptá, co chce udělat. Proto jej stačí spustit bez parametrů: \`./makeMap.sh\`."
	echo "	Pro bezobslužné automatické spouštění lze chování ovlivnit pomocí parametrů:"
	echo "		* \`-a <stát>\` nebo \`--area <stát>\` definuje stát (oblast), pro který je mapa generována. Viz [seznam států](Seznam států)"
	echo "		* \`-dy\` nebo \`--download_yes\` vynutí vždy nové stažení mapových dat"
	echo "		* \`-dn\` nebo \`--download_no\` v případě, že byli dříve stažená mapová data, nebudou se znovu stahovat. **POZOR**, není nijak prováděna validace těchto dat, tedy jedná-li se o fragment z přechozího přerušeného stahování, dojde k chybě. Není-li zadáno *download_yes* nebo *download_no*, skript se zeptá."
	echo "		* \`-ns\` nebo \`--no_split\` zakáže dělení mapových souborů na menší díly. Vhodné pouze u velmi malých oblastí a pro počítače s dostatkem RAM. "
	echo "		* \`-h\` nebo \`--help\` zobrazí tuto nápovědu."
	echo ""
	echo "## Seznam států"
	echo "	Státy jsou přímo definovány ve skriptu. Jejich definice začíná okolo řádku \`90\`. Příklad definice pro ČR:"
	echo "		* \`CZ|cz )\` - použitelné zkratky státu pro paramter \`--area\`, zde *CZ* a *cz*"
	echo "		* \`echo \"Tvorim mapu pro Ceskou republiku\"\` - Výpis na konzoly"
	echo "		* \`STATE=\"CZ\"\` - Zkratka státu použitá v názvech souborů"
	echo "		* \`DATA_URL=\"http://download.geofabrik.de/europe/czech-republic-latest.osm.pbf\"\` - Zdroj mapových dat, jsou-li mapová data stahována ručně, použijte \`false\`"
	echo "		* \`POLY_URL=\"http://download.geofabrik.de/europe/czech-republic.poly\"\` - Zdroj hraničních polygonů, je-li polygon definován ručně, použijte \`false\`"
	echo "		* \`COUNTRY_NAME=\"Ceska republika - VasaM\"\` - Název mapy vypsaný v GPS a BaseCamp"
	echo "		* \`VERSION=20\` - Verze mapy děleno stem, tedy 20 = 0.20."
	echo "		* \`COUNTRY_ID=8801\` - Jedinečné ID mapy"
	echo "		* \`break\`"
	echo "		* \`;;\`"
	echo ""
	echo "	Chcete-li přidat další mapu či oblsat, nejednoduší je zkoírovat existjící a upravit ji. Nezapomeňte změnit ID na nějaké jiné. Pro vlastní mapy doporučuji jiné, než \`88xx\`. Toto čislování budu používat pro mnou generované mapy a mohlo by dojít ke konfliktu."
}


# Zaznamenam cas spusteni
TMP=$(date)
START=$(date +%s)
echo "Spusteno v $TMP"


# Nactu arumenty
SPLIT=true
while [[ $# -gt 0 ]]
do
	key="$1"

	case $key in
		-a|--area )
		STATE="$2"
		shift # past argument
		shift # past value
		;;
		
		-dy|--download_yes )
		DOWNLOAD=true
		shift # past argument
		;;
		
		-dn|--download_no )
		DOWNLOAD=false
		shift # past argument
		;;
		
		-ns|--no_split )
		SPLIT=false
		shift # past argument
		;;
		
		-h|--help )
		viewHelp
		end
		;;
		
		* )	# unknown option
		echo "Neznamy argument '$1'!"
		end
		;;
	esac
done


# Ziskam stat, nebyl-li zadan
while [ true ]; do
	if [ -z ${STATE+x} ]; then
		echo "Zadejte zkratku statu, pro ktery chcete vytvorit mapu."
		echo "  * Ceska republika - [CZ]"
		echo "  * Slovenska republika - [SK]"
		echo "  * Kyrgyzstan - [KG]"
		echo "  * Ukrajina - [UA]"
		echo "  * Rumunsku - [RO]"
		echo ""
	 	read -p "Vybrana mapa: " -r
	 	STATE=$REPLY
	fi

	# Vytvorim odkaz na dany stat
	case $STATE in
		CZ|cz )
			echo "Tvorim mapu pro Ceskou republiku"
			STATE="CZ"
			DATA_URL="http://download.geofabrik.de/europe/czech-republic-latest.osm.pbf"
			POLY_URL="http://download.geofabrik.de/europe/czech-republic.poly"
			COUNTRY_NAME="Ceska republika - VasaM"
			VERSION=20
			COUNTRY_ID=8801
			break
			;;

		KG|kg )
			echo "Tvorim mapu pro Kyrgyzstan"
			STATE="KG"
			DATA_URL="http://download.geofabrik.de/asia/kyrgyzstan-latest.osm.pbf"
			POLY_URL="http://download.geofabrik.de/asia/kyrgyzstan.poly"
			COUNTRY_NAME="Kyrgyzstan - VasaM"
			VERSION=20
			COUNTRY_ID=8802
			break
			;;

		UA|ua )
			STATE="UA"
			echo "Tvorim mapu pro Ukrajinu"
			DATA_URL="http://download.geofabrik.de/europe/ukraine-latest.osm.pbf"
			POLY_URL="http://download.geofabrik.de/europe/ukraine.poly"
			COUNTRY_NAME="Ukrajina - VasaM"
			VERSION=20
			COUNTRY_ID=8804
			break
			;;

		SK|sk )
			echo "Tvorim mapu pro Slovensko"
			STATE="SK"
			DATA_URL="http://download.geofabrik.de/europe/slovakia-latest.osm.pbf"
			POLY_URL="http://download.geofabrik.de/europe/slovakia.poly"
			COUNTRY_NAME="Slovenska republika - VasaM"
			VERSION=20
			COUNTRY_ID=8805
			break
			;;

		RO|ro )
			echo "Tvorim mapu pro Rumunsko"
			STATE="RO"
			DATA_URL="http://download.geofabrik.de/europe/romania-latest.osm.pbf"
			POLY_URL="http://download.geofabrik.de/europe/romania.poly"
			COUNTRY_NAME="Rumunsko - VasaM"
			VERSION=20
			COUNTRY_ID=8805
			break
			;;

		* )
			echo "Neznamy stat '${STATE}'. Zkuste to znovu"
			unset STATE
	esac
done


# Zjistim, zda mam stahovat data
if [ -f ./pbf/$STATE.osm.pbf ]; then	# Data jiz byla stazena
	echo "Nalezen soubor ${STATE}.osm.pbf"

	if [ -z ${DOWNLOAD+x} ]; then	# Uzivatel nespecifikoval, co se ma stat
	 	while [ true ]; do
		 	read -p "Data pro mapu byla uz stazena, chcete je pouzit? [A/n] " -r
			if [[ $REPLY =~ ^[Aa]$ ]]; then
				DOWNLOAD=false
				break
			elif [[ $REPLY =~ ^[Nn]$ ]]; then
				DOWNLOAD=true
				break
			else
			 	echo "Neplatný vstup, zkuste to znovu"
			fi
		done
	fi
else
	if [ $DATA_URL = false ]; then
		echo "NEnalezen soubor ${STATE}.osm.pbf!"
		end
	fi

	DOWNLOAD=true
fi


# Stahnu data
if [ $DOWNLOAD = true ]; then
 	echo "Stahuji aktualni data"
	wget -v -O ./pbf/${STATE}.osm.pbf $DATA_URL
else
 	echo "Pouzivam drive stazena data"
fi


# Stahnu polygon
if [ ! -f ./poly/$STATE.poly ]; then
	if [ POLY_URL = false ]; then
		echo "NEnalezen soubor ${STATE}.poly!"
		end
	fi

 	echo "Stahuji hranice"
	wget -v -O ./poly/$STATE.poly $POLY_URL
fi


# Zjistim, zda mam hotove vrstevnice
if [ ! -f ./pbf/$STATE-SRTM.osm.pbf ]; then
 	echo "Generuji vrstevnice"
	phyghtmap \
		--polygon=./poly/${STATE}.poly \
		-o ./pbf/${STATE}-SRTM \
		--pbf \
		-j 2 \
		-s 10 \
		-c 200,100 \
		--start-node-id=20000000000 \
		--start-way-id=10000000000 \
		--write-timestamp \
		--max-nodes-per-tile=0 \
		--earthexplorer-user=$USER \
		--earthexplorer-password=$PASS

	mv ./pbf/$STATE-SRTM* ./pbf/$STATE-SRTM.osm.pbf
else
 	echo "Pouzivam drive vygenerovane vrstevnice"
fi


# Vytvorim cilovou podslozku
if [ ! -d ./img/${STATE}_VasaM ]; then
	mkdir ./img/${STATE}_VasaM
fi


# Stahnu HGT soubory
PYTHON ./hgt/hgt-downloader.py ./hgt/SRTM3v3.0 ./hgt


# Rozdelim soubory
INPUT_FILE=./pbf/${STATE}.osm.pbf
INPUT_SRTM_FILE=./pbf/${STATE}-SRTM.osm.pbf

if [ $SPLIT != false ]; then
	if [ ! -d ./pbf/${STATE}-SPLITTED/ ]; then
		java -Xmx4000m -jar ./splitter/splitter.jar $INPUT_FILE --output-dir=./pbf/${STATE}-SPLITTED/
	fi
	INPUT_FILE=./pbf/${STATE}-SPLITTED/*.osm.pbf

	if [ ! -d ./pbf/${STATE}-SPLITTED-SRTM/ ]; then
		java -Xmx4000m -jar ./splitter/splitter.jar $INPUT_SRTM_FILE --output-dir=./pbf/${STATE}-SPLITTED-SRTM/
	fi
	INPUT_SRTM_FILE=./pbf/${STATE}-SPLITTED-SRTM/*.osm.pbf
fi


# Spustim generator
java -Xmx8000m -jar ./mkgmap/mkgmap.jar \
     -c ./mkgmap-settings.conf \
     --mapname="${COUNTRY_ID}0001" \
     --overview-mapnumber="${COUNTRY_ID}0000" \
     --family-id="${COUNTRY_ID}" \
     --description="Turisticka mapa ${COUNTRY_NAME}" \
     --family-name="${COUNTRY_NAME}" \
     --series-name="${COUNTRY_NAME}" \
     --country-name="${COUNTRY_NAME}" \
     --country-abbr="${STATE}" \
     --product-version=$VERSION \
     --output-dir=./img/${STATE}_VasaM \
     --dem-poly=./poly/$STATE.poly \
     $INPUT_FILE \
     $INPUT_SRTM_FILE \
     ./style/style.txt


# Vytvorim instalacni bat soubor
# Prevedu ID do hexa tvaru
a=$(printf "%x\n" $COUNTRY_ID | egrep -o '[a-fA-F0-9]{2}$')
b=$(printf "%x\n" $COUNTRY_ID | egrep -o '^[a-fA-F0-9]{2}')

echo "echo off"                                                                                     > ./img/${STATE}_VasaM/install.bat
echo "echo - Instalce mapy do Mapsource/Basecamp"                                                  >> ./img/${STATE}_VasaM/install.bat
echo "echo - "                                                                                     >> ./img/${STATE}_VasaM/install.bat
echo "echo - Mapa:  \"${COUNTRY_NAME}\""                                                           >> ./img/${STATE}_VasaM/install.bat
echo "echo -  FID:  ${COUNTRY_ID}"                                                                 >> ./img/${STATE}_VasaM/install.bat
echo "echo -  PID:  1"                                                                             >> ./img/${STATE}_VasaM/install.bat
echo "echo - "                                                                                     >> ./img/${STATE}_VasaM/install.bat
echo "echo - Instalaci zrusite stiskem Ctrl-C."                                                    >> ./img/${STATE}_VasaM/install.bat
echo "echo - "                                                                                     >> ./img/${STATE}_VasaM/install.bat
echo "pause"                                                                                       >> ./img/${STATE}_VasaM/install.bat
echo " "                                                                                           >> ./img/${STATE}_VasaM/install.bat
echo "echo Zapisuji do registru:."                                                                 >> ./img/${STATE}_VasaM/install.bat
echo " "                                                                                           >> ./img/${STATE}_VasaM/install.bat
echo "set KEY=HKLM\SOFTWARE\Wow6432Node\Garmin\MapSource"                                          >> ./img/${STATE}_VasaM/install.bat
echo "if %PROCESSOR_ARCHITECTURE% == AMD64 goto key_ok"                                            >> ./img/${STATE}_VasaM/install.bat
echo "set KEY=HKLM\SOFTWARE\Garmin\MapSource"                                                      >> ./img/${STATE}_VasaM/install.bat
echo ":key_ok"                                                                                     >> ./img/${STATE}_VasaM/install.bat
echo " "                                                                                           >> ./img/${STATE}_VasaM/install.bat
echo "reg ADD %KEY%\Families\FAMILY_${COUNTRY_ID} /v ID /t REG_BINARY /d ${a}${b} /f"              >> ./img/${STATE}_VasaM/install.bat
echo "reg ADD %KEY%\Families\FAMILY_${COUNTRY_ID} /v IDX /t REG_SZ /d \"%~dp0mapset.mdx\" /f"      >> ./img/${STATE}_VasaM/install.bat
echo "reg ADD %KEY%\Families\FAMILY_${COUNTRY_ID} /v MDR /t REG_SZ /d \"%~dp0mapset_mdr.img\" /f"  >> ./img/${STATE}_VasaM/install.bat
echo "reg ADD %KEY%\Families\FAMILY_${COUNTRY_ID} /v TYP /t REG_SZ /d \"%~dp0style.typ\" /f"       >> ./img/${STATE}_VasaM/install.bat
echo "reg ADD %KEY%\Families\FAMILY_${COUNTRY_ID}\1 /v Loc /t REG_SZ /d \"%~dp0\\\" /f"            >> ./img/${STATE}_VasaM/install.bat
echo "reg ADD %KEY%\Families\FAMILY_${COUNTRY_ID}\1 /v Bmap /t REG_SZ /d \"%~dp0mapset.img\" /f"   >> ./img/${STATE}_VasaM/install.bat
echo "reg ADD %KEY%\Families\FAMILY_${COUNTRY_ID}\1 /v Tdb /t REG_SZ /d \"%~dp0mapset.tdb\" /f"    >> ./img/${STATE}_VasaM/install.bat
echo " "                                                                                           >> ./img/${STATE}_VasaM/install.bat
echo "pause"                                                                                       >> ./img/${STATE}_VasaM/install.bat
echo "exit 0"                                                                                      >> ./img/${STATE}_VasaM/install.bat


echo "echo off"                                             > ./img/${STATE}_VasaM/uninstall.bat
echo "echo - Odinstalace mapy z Mapsource/Basecamp"        >> ./img/${STATE}_VasaM/uninstall.bat
echo "echo - "                                             >> ./img/${STATE}_VasaM/uninstall.bat
echo "echo - Mapa:  \"${COUNTRY_NAME}\""                   >> ./img/${STATE}_VasaM/uninstall.bat
echo "echo -  FID:  ${COUNTRY_ID}"                         >> ./img/${STATE}_VasaM/uninstall.bat
echo "echo -  PID:  1"                                     >> ./img/${STATE}_VasaM/uninstall.bat
echo "echo - "                                             >> ./img/${STATE}_VasaM/uninstall.bat
echo "echo - Instalaci zrusite stiskem Ctrl-C."            >> ./img/${STATE}_VasaM/uninstall.bat
echo "echo - "                                             >> ./img/${STATE}_VasaM/uninstall.bat
echo "pause"                                               >> ./img/${STATE}_VasaM/uninstall.bat
echo " "                                                   >> ./img/${STATE}_VasaM/uninstall.bat
echo "set KEY=HKLM\SOFTWARE\Wow6432Node\Garmin\MapSource"  >> ./img/${STATE}_VasaM/uninstall.bat
echo "if %PROCESSOR_ARCHITECTURE% == AMD64 goto key_ok"    >> ./img/${STATE}_VasaM/uninstall.bat
echo "set KEY=HKLM\SOFTWARE\Garmin\MapSource"              >> ./img/${STATE}_VasaM/uninstall.bat
echo ":key_ok"                                             >> ./img/${STATE}_VasaM/uninstall.bat
echo " "                                                   >> ./img/${STATE}_VasaM/uninstall.bat
echo "reg DELETE %KEY%\Families\FAMILY_${COUNTRY_ID} /f"   >> ./img/${STATE}_VasaM/uninstall.bat
echo "pause"                                               >> ./img/${STATE}_VasaM/uninstall.bat
echo "exit 0"                                              >> ./img/${STATE}_VasaM/uninstall.bat

# Prejmenuji vystupni soubor
mv ./img/${STATE}_VasaM/gmapsupp.img ./img/${STATE}_VasaM.img

# Vytvorim archiv
cd img
rm ${STATE}_VasaM.zip
zip -r ${STATE}_VasaM.zip ${STATE}_VasaM/
cd ..

end