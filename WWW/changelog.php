<strong>CHANGELOG:</strong>
<ul>

<?php

	$changelog = scandir( './changelog', 1 );

	foreach ( $changelog as $change ) {
		if ( preg_match( '/v([\d]{3,5})/', $change, $match ) ) {
			$version = number_format( intval( $match[ 1 ] ) / 100, 2, ".", " " );
			$file = fopen( "./changelog/" . $change, "r" );
			
			echo "<li>\n";
			echo "<strong id=\"v$version\">v " . $version . " <em>" . date( "j. n. Y", filemtime( "./changelog/" . $change ) ) . "</em></strong>\n";
			echo "<ul>\n";

		    while ( ( $line = fgets( $file) ) !== false ) {
		    	$line = preg_replace('/\r?\n$/', '', $line);

				if ( $line == '<ul>' ) {
					echo "<ul>\n";
					continue;
				}
				elseif ( $line == '</ul>' ) {
					echo "</ul>\n";
					continue;
				}

				echo "<li>" . $line . "</li>\n";
		    }
		    fclose( $file );
	
			echo "</ul>\n";
			echo "</li>\n";
		}
	}
?>

</ul>