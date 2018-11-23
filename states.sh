function states {
	DATA_URL=false
	POLY_URL=false
	POIS=false

	while [ true ]; do
		if [ -z ${STATE+x} ]; then
			echo "Zadejte zkratku statu, pro ktery chcete vytvorit mapu."
			echo "  * Ceska republika - [CZ]"
			echo "  * Slovenska republika - [SK]"
			echo "  * Polsko - [PL]"
			echo "  * Německo - [DE]"
			echo "  * Rakousko - [AT]"
			echo "  * Ukrajina - [UA]"
			echo "  * Rumunsku - [RO]"
			echo "  * Chorvatsko - [HR]"
			echo "  * Norsko - [NO]"
			echo "  * Dansko - [DK]"
			echo "  * Slovinsko - [SI]"
			echo "  * Kyrgyzstan - [KG]"
			echo "  * Kazachstan - [KZ]"
			echo "  * Maroko - [MA]"
			echo "  * Nepal - [NP]"
			echo ""
		 	read -p "Vybrana mapa: " -r
		 	STATE=$REPLY
		fi

		# Vytvorim odkaz na dany stat
		case $STATE in
			OL|ol )
				echo "Tvorim mapu pro Olomouc"
				STATE="OL"
				COUNTRY_NAME="Olomouc - VasaM"
				COUNTRY_ID=8800
				break
				;;

			#Stredni Evropa ID: 8801 - 8810
			CZ|cz )
				echo "Tvorim mapu pro Ceskou republiku"
				STATE="CZ"
				DATA_URL="http://download.geofabrik.de/europe/czech-republic-latest.osm.pbf"
				POLY_URL="http://download.geofabrik.de/europe/czech-republic.poly"
				COUNTRY_NAME="Ceska republika - VasaM"
				COUNTRY_ID=8801
				POIS=( chs )
				break
				;;

			SK|sk )
				echo "Tvorim mapu pro Slovensko"
				STATE="SK"
				DATA_URL="http://download.geofabrik.de/europe/slovakia-latest.osm.pbf"
				POLY_URL="http://download.geofabrik.de/europe/slovakia.poly"
				COUNTRY_NAME="Slovenska republika - VasaM"
				COUNTRY_ID=8802
				break
				;;

			PL|pl )
				echo "Tvorim mapu pro Polsko"
				STATE="PL"
				DATA_URL="http://download.geofabrik.de/europe/poland-latest.osm.pbf"
				POLY_URL="http://download.geofabrik.de/europe/poland.poly"
				COUNTRY_NAME="Polsko - VasaM"
				COUNTRY_ID=8803
				break
				;;

			DE|de )
				echo "Tvorim mapu pro Nemecko"
				STATE="DE"
				DATA_URL="http://download.geofabrik.de/europe/germany-latest.osm.pbf"
				POLY_URL="http://download.geofabrik.de/europe/germany.poly"
				COUNTRY_NAME="Nemecko - VasaM"
				COUNTRY_ID=8804
				break
				;;

			AT|at )
				echo "Tvorim mapu pro Rakousko"
				STATE="AT"
				DATA_URL="http://download.geofabrik.de/europe/austria-latest.osm.pbf"
				POLY_URL="http://download.geofabrik.de/europe/austria.poly"
				COUNTRY_NAME="Rakousko - VasaM"
				COUNTRY_ID=8805
				break
				;;

			#Ostatni Evropa ID: 8811 - 8840
			UA|ua )
				STATE="UA"
				echo "Tvorim mapu pro Ukrajinu"
				DATA_URL="http://download.geofabrik.de/europe/ukraine-latest.osm.pbf"
				POLY_URL="http://download.geofabrik.de/europe/ukraine.poly"
				COUNTRY_NAME="Ukrajina - VasaM"
				COUNTRY_ID=8811
				break
				;;

			RO|ro )
				echo "Tvorim mapu pro Rumunsko"
				STATE="RO"
				DATA_URL="http://download.geofabrik.de/europe/romania-latest.osm.pbf"
				POLY_URL="http://download.geofabrik.de/europe/romania.poly"
				COUNTRY_NAME="Rumunsko - VasaM"
				COUNTRY_ID=8812
				break
				;;

			HR|hr )
				echo "Tvorim mapu pro Chorvatsko"
				STATE="HR"
				DATA_URL="http://download.geofabrik.de/europe/croatia-latest.osm.pbf"
				POLY_URL="http://download.geofabrik.de/europe/croatia.poly"
				COUNTRY_NAME="Chorvatsko - VasaM"
				COUNTRY_ID=8813
				break
				;;

			NO|no )
				echo "Tvorim mapu pro Norsko"
				STATE="NO"
				DATA_URL="http://download.geofabrik.de/europe/norway-latest.osm.pbf"
				POLY_URL="http://download.geofabrik.de/europe/norway.poly"
				COUNTRY_NAME="Norsko - VasaM"
				COUNTRY_ID=8814
				break
				;;

			DK|dk )
				echo "Tvorim mapu pro Dansko"
				STATE="DK"
				DATA_URL="http://download.geofabrik.de/europe/denmark-latest.osm.pbf"
				POLY_URL="http://download.geofabrik.de/europe/denmark.poly"
				COUNTRY_NAME="Dansko - VasaM"
				COUNTRY_ID=8815
				break
				;;

			SI|si )
				echo "Tvorim mapu pro Slovinsko"
				STATE="SI"
				DATA_URL="http://download.geofabrik.de/europe/slovenia-latest.osm.pbf"
				POLY_URL="http://download.geofabrik.de/europe/slovenia.poly"
				COUNTRY_NAME="Slovinsko - VasaM"
				COUNTRY_ID=8816
				break
				;;


			#Ostatni ID: 8831 - 8890
			KG|kg )
				echo "Tvorim mapu pro Kyrgyzstan"
				STATE="KG"
				DATA_URL="http://download.geofabrik.de/asia/kyrgyzstan-latest.osm.pbf"
				POLY_URL="http://download.geofabrik.de/asia/kyrgyzstan.poly"
				COUNTRY_NAME="Kyrgyzstan - VasaM"
				COUNTRY_ID=8841
				break
				;;

			KZ|kz )
				echo "Tvorim mapu pro Kazachstan"
				STATE="KZ"
				DATA_URL="http://download.geofabrik.de/asia/kazakhstan-latest.osm.pbf"
				POLY_URL="http://download.geofabrik.de/asia/kazakhstan.poly"
				COUNTRY_NAME="Kazachstan - VasaM"
				COUNTRY_ID=8842
				break
				;;

			NP|np )
				echo "Tvorim mapu pro Nepal"
				STATE="NP"
				DATA_URL="http://download.geofabrik.de/asia/nepal-latest.osm.pbf"
				POLY_URL="http://download.geofabrik.de/asia/nepal.poly"
				COUNTRY_NAME="Nepal - VasaM"
				COUNTRY_ID=8843
				break
				;;

			MA|ma )
				echo "Tvorim mapu pro Maroko"
				STATE="MA"
				DATA_URL="http://download.geofabrik.de/africa/morocco-latest.osm.pbf"
				POLY_URL="http://download.geofabrik.de/africa/morocco.poly"
				COUNTRY_NAME="Maroko - VasaM"
				COUNTRY_ID=8844
				break
				;;

			TEST|test )
				echo "Testuji"
				STATE="TEST"
				POIS=( chs )
				COUNTRY_NAME="Test - VasaM"
				COUNTRY_ID=8899
				break
				;;

			* )
				echo "Neznamy stat '${STATE}'. Zkuste to znovu"
				unset STATE
		esac
	done
}