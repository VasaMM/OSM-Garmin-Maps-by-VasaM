#!/bin/bash

# Prihlasovaci udaje pro https://ers.cr.usgs.gov/
USER=VasaM
PASS=Password123


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
		
		-g|--garmin )
		GARMIN=true
		shift # past argument
		;;
		
		-m|--mapsforge )
		MAPSFORGE=true
		shift # past argument
		;;
		
		-h|--help )
		echo "Toto je napoveda"
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
		echo "  * Olomouc - [OL]"
		echo ""
	 	read -p "Vybrana mapa: " -r
	 	STATE=$REPLY
	fi

	# Vytvorim odkaz na dany stat
	case $STATE in
		"CZ" )
			echo "Tvorim mapu pro Ceskou republiku"
			DATA_URL="http://download.geofabrik.de/europe/czech-republic-latest.osm.pbf"
			POLY_URL="http://download.geofabrik.de/europe/czech-republic.poly"
			COUNTRY_NAME="Ceska republika TOPO"
			COUNTRY_ABBR="CZ"
			VERSION=10
			COUNTRY_ID=8801
			break
			;;

		"KG" )
			echo "Tvorim mapu pro Kyrgyzstan"
			DATA_URL="http://download.geofabrik.de/asia/kyrgyzstan-latest.osm.pbf"
			POLY_URL="http://download.geofabrik.de/asia/kyrgyzstan.poly"
			COUNTRY_NAME="Kyrgyzstan TOPO"
			COUNTRY_ABBR="KG"
			VERSION=10
			COUNTRY_ID=8802
			break
			;;

		"OL" )
			echo "Tvorim mapu pro Olomouc"
			DATA_URL=false
			POLY_URL=false
			COUNTRY_NAME="Olomouc TOPO"
			COUNTRY_ABBR="OL"
			VERSION=10
			COUNTRY_ID=8803
			break
			;;

		"UA" )
			echo "Tvorim mapu pro Ukrajinu"
			DATA_URL="http://download.geofabrik.de/europe/ukraine-latest.osm.pbf"
			POLY_URL="http://download.geofabrik.de/europe/ukraine.poly"
			COUNTRY_NAME="Ukrajina TOPO"
			COUNTRY_ABBR="UA"
			VERSION=10
			COUNTRY_ID=8804
			break
			;;

		"SK" )
			echo "Tvorim mapu pro Slovensko"
			DATA_URL="http://download.geofabrik.de/europe/slovakia-latest.osm.pbf"
			POLY_URL="http://download.geofabrik.de/europe/slovakia.poly"
			COUNTRY_NAME="Slovenska republika TOPO"
			COUNTRY_ABBR="SK"
			VERSION=10
			COUNTRY_ID=8805
			break
			;;

		"RO" )
			echo "Tvorim mapu pro Rumunsko"
			DATA_URL="http://download.geofabrik.de/europe/romania-latest.osm.pbf"
			POLY_URL="http://download.geofabrik.de/europe/romania.poly"
			COUNTRY_NAME="Rumunsko TOPO"
			COUNTRY_ABBR="RO"
			VERSION=10
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


# Zjistim cilovou platformu
while [ -z ${MAPSFORGE+x} ] && [ -z ${GARMIN+x} ]; do
 	read -p "Chcete vytvořit mapu pro [G]armin, [M]apsforge nebo [O]boje? [G/M/O] " -r
	
	# Garmin
	if [[ $REPLY =~ ^[Gg]$ ]]; then
		GARMIN=true
	fi
	# Mapsforge
	if [[ $REPLY =~ ^[Mm]$ ]]; then
		MAPSFORGE=true
	fi
	# Oboje
	if [[ $REPLY =~ ^[Oo]$ ]]; then
		GARMIN=true
		MAPSFORGE=true
	fi
done


# Definuji nedefinovane promenne
if [ -z ${MAPSFORGE+x} ]; then
	MAPSFORGE=false
fi

if [ -z ${GARMIN+x} ]; then
	GARMIN=false
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


# Generuji Mapsforge
if [ $MAPSFORGE = true ]; then
	cd "./Mapsforge/bin"
	export JAVACMD_OPTIONS="-Xmx4000m"
	
	# Vlozim vrstevnice do mapy
	if [ $DOWNLOAD = true ] || [ ! -f ../pbf/$STATE-MERGE.osm.pbf ]; then
		./osmosis --rb file="../../pbf/$STATE.osm.pbf" --sort-0.6 --rb "../../pbf/$STATE-SRTM.osm.pbf" --sort-0.6 --merge --wb "../../pbf/$STATE-MERGE.osm.pbf"
	fi

	# Generuji mapu
	# ./osmosis --rb file="../../pbf/$STATE-MERGE.osm.pbf" --mapfile-writer file="../../map/$STATE.map" type=hd preferred-languages=en,cs threads=4 tag-conf-file="../tag-mapping.xml"
	./osmosis --rb file="../../pbf/$STATE.osm.pbf" --mapfile-writer file="../../map/$STATE.map" type=ram preferred-languages=en tag-conf-file="../tag-mapping.xml"

	cd "./../.."
fi


# Generuji Garmin
if [ $GARMIN = true ]; then
	if [ ! -d ./img/${STATE}_VasaM ]; then
		mkdir ./img/${STATE}_VasaM
	fi

	# Stahnu HGT soubory
	# FIXME
	python3.4 ./hgt/hgt-downloader.py ./hgt/SRTM3v3.0 ./hgt

	INPUT_FILE=./pbf/${STATE}.osm.pbf
	INPUT_SRTM_FILE=./pbf/${STATE}-SRTM.osm.pbf

	if [ $SPLIT != false ]; then
		if [ ! -d ./pbf/${STATE}-SPLITTED/ ]; then
			java -Xmx4000m -jar ./Garmin/splitter/splitter.jar $INPUT_FILE --output-dir=./pbf/${STATE}-SPLITTED/
		fi
		INPUT_FILE=./pbf/${STATE}-SPLITTED/*.osm.pbf

		if [ ! -d ./pbf/${STATE}-SPLITTED-SRTM/ ]; then
			java -Xmx4000m -jar ./Garmin/splitter/splitter.jar $INPUT_SRTM_FILE --output-dir=./pbf/${STATE}-SPLITTED-SRTM/
		fi
		INPUT_SRTM_FILE=./pbf/${STATE}-SPLITTED-SRTM/*.osm.pbf
	fi

	java -Xmx8000m -jar ./Garmin/mkgmap/mkgmap.jar \
	     -c ./Garmin/settings.conf \
	     --mapname="${COUNTRY_ID}0001" \
	     --overview-mapnumber="${COUNTRY_ID}0000" \
	     --family-id="${COUNTRY_ID}" \
	     --description="Turisticka mapa $COUNTRY_NAME od VasaM" \
	     --family-name="$COUNTRY_NAME" \
	     --series-name="$COUNTRY_NAME" \
	     --country-name="$COUNTRY_NAME" \
	     --country-abbr="$COUNTRY_ABBR" \
	     --product-version=$VERSION \
	     --output-dir=./img/${STATE}_VasaM \
	     --dem-poly=./poly/$STATE.poly \
	     $INPUT_FILE \
	     $INPUT_SRTM_FILE \
	     ./Garmin/style/style.txt

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
fi

end