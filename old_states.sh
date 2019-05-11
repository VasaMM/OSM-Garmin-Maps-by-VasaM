function states {
	DATA_URL=false
	POLY_URL=false
	POIS=false

	while [ true ]; do
		if [ -z ${STATE+x} ]; then
			echo "Zadejte zkratku statu, pro ktery chcete vytvorit mapu."
			echo "  * Ceska republika - [CZ]"
			echo "  * Slovenska republika - [SK]"
			echo "  * Dansko - [DK]"
			echo "  * Chorvatsko - [HR]"
			echo "  * Kazachstan - [KZ]"
			echo "  * Kyrgyzstan - [KG]"
			echo "  * Madarsko - [HU]"
			echo "  * Maroko - [MA]"
			echo "  * Nepal - [NP]"
			echo "  * New York - [NY]"
			echo "  * Norsko - [NO]"
			echo "  * Nemecko - [DE]"
			echo "  * Polsko - [PL]"
			echo "  * Rakousko - [AT]"
			echo "  * Recko - [GR]"
			echo "  * Rumunsku - [RO]"
			echo "  * Slovinsko - [SI]"
			echo "  * Tadzikistan - [TJ]"
			echo "  * Ukrajina - [UA]"
			echo "  * Vietnam - [VN]"
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

			GR|gr )
				echo "Tvorim mapu pro Recko"
				STATE="GR"
				DATA_URL="http://download.geofabrik.de/europe/greece-latest.osm.pbf"
				POLY_URL="http://download.geofabrik.de/europe/greece.poly"
				COUNTRY_NAME="Recko - VasaM"
				COUNTRY_ID=8817
				break
				;;

			HU|hu )
				echo "Tvorim mapu pro Madarsko"
				STATE="HU"
				DATA_URL="http://download.geofabrik.de/europe/hungary-latest.osm.pbf"
				POLY_URL="http://download.geofabrik.de/europe/hungary.poly"
				COUNTRY_NAME="Madarsko - VasaM"
				COUNTRY_ID=8818
				break
				;;

			ES|es )
				echo "Tvorim mapu pro Spanelsko"
				STATE="ES"
				DATA_URL="http://download.geofabrik.de/europe/spain-latest.osm.pbf"
				POLY_URL="http://download.geofabrik.de/europe/spain.poly"
				COUNTRY_NAME="Spanelsko - VasaM"
				COUNTRY_ID=8819
				break
				;;

			IT|it )
				echo "Tvorim mapu pro Italii"
				STATE="IT"
				DATA_URL="http://download.geofabrik.de/europe/italy-latest.osm.pbf"
				POLY_URL="http://download.geofabrik.de/europe/italy.poly"
				COUNTRY_NAME="Italie - VasaM"
				COUNTRY_ID=8820
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

			TJ|tj )
				echo "Tvorim mapu pro Tádžikistán"
				STATE="TJ"
				DATA_URL="http://download.geofabrik.de/asia/tajikistan-latest.osm.pbf"
				POLY_URL="http://download.geofabrik.de/asia/tajikistan.poly"
				COUNTRY_NAME="Tadzikistan - VasaM"
				COUNTRY_ID=8845
				break
				;;

			NY|ny )
				echo "Tvorim mapu pro New York"
				STATE="NY"
				DATA_URL="http://download.geofabrik.de/north-america/us/new-york-latest.osm.pbf"
				POLY_URL="http://download.geofabrik.de/north-america/us/new-york.poly"
				COUNTRY_NAME="New York - VasaM"
				COUNTRY_ID=8846
				break
				;;

			VN|vn )
				echo "Tvorim mapu pro Vietnam"
				STATE="VN"
				DATA_URL="https://download.geofabrik.de/asia/vietnam-latest.osm.pbf"
				POLY_URL="https://download.geofabrik.de/asia/vietnam.poly"
				COUNTRY_NAME="Vietnam - VasaM"
				COUNTRY_ID=8847
				break
				;;

			LK|lk )
				echo "Tvorim mapu pro Sri Lanku"
				STATE="LK"
				DATA_URL="https://download.geofabrik.de/asia/sri-lanka-latest.osm.pbf"
				POLY_URL="https://download.geofabrik.de/asia/sri-lanka.poly"
				COUNTRY_NAME="Sri Lanka - VasaM"
				COUNTRY_ID=8848
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

			CZu )
				echo "Tvorim mapu pro Ceskou republiku"
				STATE="CZu"
				DATA_URL="http://download.geofabrik.de/europe/czech-republic-latest.osm.pbf"
				POLY_URL="http://download.geofabrik.de/europe/czech-republic.poly"
				COUNTRY_NAME="Ceska republika (unicode) - VasaM"
				COUNTRY_ID=8888
				POIS=( chs )
				break
				;;

			* )
				echo "Neznamy stat '${STATE}'. Zkuste to znovu"
				unset STATE
		esac
	done
}