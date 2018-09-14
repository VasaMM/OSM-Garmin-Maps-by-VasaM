function states {
	DATA_URL=false
	POLY_URL=false
	POIS=false

	while [ true ]; do
		if [ -z ${STATE+x} ]; then
			echo "Zadejte zkratku statu, pro ktery chcete vytvorit mapu."
			echo "  * Ceska republika - [CZ]"
			echo "  * Slovenska republika - [SK]"
			echo "  * Ukrajina - [UA]"
			echo "  * Rumunsku - [RO]"
			echo "  * Chorvatsko - [HR]"
			echo "  * Kyrgyzstan - [KG]"
			echo "  * Kazachstan - [KZ]"
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

			#Ostatni Evropa ID: 8811 - 8820
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


			#Ostatni ID: 8821 - 8890
			KG|kg )
				echo "Tvorim mapu pro Kyrgyzstan"
				STATE="KG"
				DATA_URL="http://download.geofabrik.de/asia/kyrgyzstan-latest.osm.pbf"
				POLY_URL="http://download.geofabrik.de/asia/kyrgyzstan.poly"
				COUNTRY_NAME="Kyrgyzstan - VasaM"
				COUNTRY_ID=8821
				break
				;;


			KZ|kz )
				echo "Tvorim mapu pro Kazachstan"
				STATE="KZ"
				DATA_URL="http://download.geofabrik.de/asia/kazakhstan-latest.osm.pbf"
				POLY_URL="http://download.geofabrik.de/asia/kazakhstan.poly"
				COUNTRY_NAME="Kazachstan - VasaM"
				COUNTRY_ID=8822
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