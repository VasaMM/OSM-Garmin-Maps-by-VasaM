<?php
 	$id = 'filename';
	if ( isset( $_GET[ 'id' ] ) ) {
		$id = $_GET[ 'id' ];
	}

	header("Content-type: text/plain");
	header("Content-Disposition: attachment; filename=$id.sha1");

	// Odstranim priponu
	preg_match( '/(.*)\.(.*)/', $id, $fileName );
	$infoFile = './maps/' . $fileName[ 1 ] . '.info';

	if ( file_exists( $infoFile ) ) {
		$info = json_decode( file_get_contents( $infoFile ), true );

		switch ( $fileName[ 2 ] ) {
			case 'img':  echo $info[ 'hashImg' ];  break;
			case 'zip':  echo $info[ 'hashZip' ];  break;
			default:     echo '0';                 break;
		}
	}
?>