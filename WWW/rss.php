<?php
	$URL = "https://brazovic.cz/subdom/osmg";

	// Funkce pro vytvoreni jedne mapy v RSS
	function mapItem( $id, $name, $suffix ) {
		global $URL;
		if ( file_exists( './maps/' . $id . '_VasaM.' . $suffix ) ) {
			$title = 'Mapa: ' . $name;

			switch ( $suffix ) {
				case 'zip':  $title .= ' (BaseCamp)';  break;
				case 'img':  $title .= ' (GPS)';       break;
			}


			$link = $URL . '/maps/' . $id . '_VasaM.' . $suffix;
			$pubDate = date('r', filemtime( './maps/' . $id . '_VasaM.' . $suffix ) );

			$description = "Nejspíše vadný soubor!!!";
			if ( file_exists( './maps/' . $id . '_VasaM.info' ) ) {
				$info = json_decode( file_get_contents( './maps/' . $id . '_VasaM.info' ), true );

				$version = number_format( intval( $info[ 'version' ] ) / 100, 2, ".", " " );
				$title .= ' v ' . $version;

				$description = "Mapa pro $name (verze $version) vytvořená v " . date( "H:i j. n. Y", $info[ 'timestamp' ] ) . ".";
			}

			printItem( $title, $link, $description, $pubDate );
		}
	}
	
	// Funkce pro vytvoreni jedne zmeny v RSS
	function changeItem( $version, $pubDate, $description ) {
		global $URL;
		$title = 'Nová verze ' . $version;
		$link = $URL . '#v' . $version;

		printItem( $title, $link, $description, $pubDate );
	}




	header('Expires: ' . gmdate('D, d M Y H:i:s') . '  GMT');
	header('Last-Modified: ' . gmdate('D, d M Y H:i:s') . '  GMT');
	header('Content-Type: text/xml; charset=utf-8');

	echo '<?xml version="1.0" encoding="utf-8"?>';

	function printItem( $title, $link, $description, $pubDate ) {
		echo "\t\t<item>";
		echo "\t\t\t<title>$title</title>";
		echo "\t\t\t<link>$link</link>";
		echo "\t\t\t<description>";
		echo "\t\t\t\t$description";
		echo "\t\t\t</description>";
		echo "\t\t\t<pubDate>$pubDate</pubDate>";
		echo "\t\t</item>";
	}
?>

<rss version="2.0">
	<channel>
		<title>OSM Garmin Maps by VasaM</title>
		<link><?php echo $URL ?></link>
		<description>Turistická mapa pro navigace Garmin</description>
		<language>cs</language>

<?php
	include( 'areas.php' );

	// Vypisu vsechny mapy
	foreach ($area as $subareaName => $subareas) {
		foreach ($subareas as $id => $name) {
			mapItem( $id, $name, 'zip' );
			mapItem( $id, $name, 'img' );
		}
	}

	// Vypisu changelog
	$changelog = scandir( './changelog', 1 );

	foreach ( $changelog as $change ) {
		if ( preg_match( '/v([\d]{3,5})/', $change, $match ) ) {
			$version = number_format( intval( $match[ 1 ] ) / 100, 2, ".", " " );
			$pubDate = date('r', filemtime( "./changelog/" . $change ) );
			$description = '';

			$file = fopen( "./changelog/" . $change, "r" );

		    while ( ( $line = fgets( $file) ) !== false ) {
		    	$description = $description . $line;
		    }
		    fclose( $file );
	
			changeItem( $version, $pubDate, $description );			
		}
	}
?>

	</channel>
</rss>

