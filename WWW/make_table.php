<?php

class Link {
	public $title   = "";
	public $class   = "";
	public $href    = "";
	public $content = "";
}

function printDownloadLink( $fileLink, $hash_value ) {
	$link = new Link();
	$size = new Link();
	$hash = new Link();

	// Soubor se teprve nahrává
	if ( file_exists( $fileLink . '.uploading' ) ) {
		$link->title = "Soubor se nahrává";
		$link->class = "no_file";

		$size->class = "uploading";
		$size->content = "Nahrává se";
	}
	else if ( file_exists( $fileLink ) ) {
		$link->title = "Stáhnout";
		$link->href  = "href=\"$fileLink\"";
		$link->content = "<div class=\"pc-no small\">" . round( filesize( $fileLink ) / 1000000, 0 ) . "&nbsp;MB</div>";

		$size->content = round( filesize( $fileLink ) / 1000000, 0 ) . " MB";

		if ( $hash_value != '' ) {
			preg_match( '/.*\/(.*)/', $fileLink, $id );
			
			$hash->title = "title=\"$hash_value\"";
			$hash->class = "hash italic mobile-no";
			$hash->content = "<a href=\"hash.php?id=$id[1]\">SHA1</a>";
		}
	}
	else {
		$link->title = "Soubor neexistuje";
		$link->class = "no_file";
	}
	
	echo "<td><a $link->href title=\"$link->title\" class=\"$link->class\"><span class=\"mobile-no\">Stáhnout</span><span class=\"pc-no\">Stáh.</span></a>$link->content</td>";
	echo "<td class=\"mobile-no $size->class\">$size->content</td>";
	echo "<td class=\"mobile-no $hash->class\" $hash->title>$hash->content</td>";
}


function make_table( $subarea ) {
	?>
	<table>
		<tr>
			<th>Oblast</th>
			<th><span class="basecamp">Base</span><span class="basecamp">Camp</span></th>
			<th class="mobile-no">Velikost</th>
			<th class="mobile-no">Hash</th>
			<th>GPS</th>
			<th class="mobile-no">Velikost</th>
			<th class="mobile-no">Hash</th>
			<th class="mobile-no">Verze</th>
			<th>Mapová data</th>
			<th class="mobile-no">Nahráno</th>
		</tr>

	<?php

	include( 'areas.php' );
	foreach ( $area[ $subarea ] as $id => $name ) {
		$infoFile = './maps/' . $id . '_VasaM.info';

		$info = '';
		$version = '';
		$age = '';
		$class = '';
		$hashZip = '';
		$hashImg = '';

		if ( file_exists( $infoFile ) ) {
			$info = json_decode( file_get_contents( $infoFile ), true );
			
			$version = number_format( intval( $info[ 'version' ] ) / 100, 2, ".", " " );
			
			$age = time() - $info[ 'timestamp' ];
			
			if ( $age < 259200 ) {	// 3 dny
				$class = 'class="new"';
			}
			elseif ( $age > 2592000 ) { // 30 dni
				$class = 'class="old"';
			}

			$hashZip = $info[ 'hashZip' ];
			$hashImg = $info[ 'hashImg' ];
		}
		
		echo "<tr>";
		echo "<td>$name <div class=\"pc-no center italic\">v $version</div></td>";

		printDownloadLink( './maps/' . $id . '_VasaM.zip', $hashZip );
		printDownloadLink( './maps/' . $id . '_VasaM.img', $hashImg );
		
		
		if ( $info != '' ) {
			echo "<td class=\"mobile-no\">$version</td>";
			echo "<td $class >" . date( "H:i  j. n. Y", $info[ 'timestamp' ] ) . "</td>";
			echo "<td class=\"mobile-no\">" . date( "H:i  j. n. Y", filectime( './maps/' . $id . '_VasaM.info' ) ) . "</td>";
		}
		else {
			echo "<td class=\"mobile-no\"></td>";
			echo "<td></td>";
			echo "<td class=\"mobile-no\"></td>";
		}

		echo "</tr>";
	}
	
	echo "</table>";
}
?>