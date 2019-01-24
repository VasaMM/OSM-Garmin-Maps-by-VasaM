<!DOCTYPE html>
<html>
<head>
	<title>OSM Garmin Maps by VasaM</title>
	<meta charset="UTF-8">
	<meta name="robots" content="none, noindex, nofollow">
	<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
	<link rel="icon" href="./favicon.png">
	<link rel="stylesheet/less" type="text/css" href="style.less">
	<script src="//cdnjs.cloudflare.com/ajax/libs/less.js/3.0.2/less.min.js"></script>

	<!-- Global site tag (gtag.js) - Google Analytics -->
	<script async src="https://www.googletagmanager.com/gtag/js?id=UA-126444520-1"></script>
	<script>
		window.dataLayer = window.dataLayer || [];
		function gtag(){dataLayer.push(arguments);}
		gtag('js', new Date());

		gtag('config', 'UA-126444520-1');
	</script>

	<?php
		if ( isset( $_GET[ 'thanks' ] ) ) {
			echo '<script type="text/javascript">';
			echo 'alert("Děkuji za váš příspěvek!");';
			echo '</script>';
		}
	?>
</head>

<body>
	<header>
		Turistická mapa pro navigace Garmin
	</header>

	<main>
		<section class="about">
			<p>
				Tyto mapy vznikly jako náhrada za komerční produkt Českých Garmin TOPO map a zároveň z potřeby turistických map i pro exotičtější země. Projekt vychází z map od <a href="https://garmin.v0174.net/" title="V0174">V0174</a>.
				Byly přidány další podrobnosti, upraven jejich vzhled a  vytvořen univerzální generátor pro libovolnou zemi. Více o generátoru najdete na <a href="https://github.com/VasaMM/OSM-Garmin-Maps-by-VasaM" title="GitHub">GitHubu</a>.
			</p>
			<p>
				Výsledkem je vcelku podrobná mapa vhodná jak pro turistiku, tak pro kolo. Ta je generována buď v podobě instalátoru do programu BaseCamp nebo jako <em>*.img</em> soubor pro přímé použití v GPS. <strong>Mapy jsou aktualizovány nepravidelně.</strong> Pokud si myslíte, že je na čase další aktualizace nebo Vám tu chybí nějaká země, zkuste mi napsat do <a href="http://www.geocaching.cz/topic/31987-osm-topo-mapa-pro-garmin/" title="Diskuze">diskuze</a>.
				Chcete-li být pravidelně informováni o novinkách, můžete využítít <a href="./rss.php" target="_blank" title="RSS feed">RSS čtečku</a>.
			</p>
		</section>

		<section class="properities">
			<strong>Vlastnosti:</strong>
			<ul>
				<li>turistické značky včetně rozcestníků</li>
				<li>cyklostezky</li>
				<li>vrstevnice včetně výškových dat (funguje výpočet výškového profilu trasy)</li>
				<li>turisticky zajímavé informace (lavička, přístřešek, koš, brána v plotě, ...)</li>
				<li>instalátor do BaseCamp</li>
			</ul>
		</section>

		<section>
			<a href="1.png" target="_blank" title="Klikněte pro detail"><img src="1_thumb.png" width="33%" style="float: left; margin-right: 0.5%;"></a>
			<a href="2.png" target="_blank" title="Klikněte pro detail"><img src="2_thumb.png" width="33%" style="float: left"></a>
			<a href="3.png" target="_blank" title="Klikněte pro detail"><img src="3_thumb.png" width="33%" style="float: left; margin-left: 0.5%;"></a>
		</section>

		<section class="changelog">
			<?php include( 'changelog.php' ) ?>
		</section>

		<hr>

		<section class="download">
			
			<?php
				include( 'make_table.php' );

				echo '<h3>Česká republika a okolí:</h3>';
				make_table( 'cr' );

				echo '<h3>Evropa:</h3>';
				make_table( 'europe' );

				echo '<h3>Asie:</h3>';
				make_table( 'asia' );

				echo '<h3>Ostatní:</h3>';
				make_table( 'other' );
			?>

			<br>
			<strong>Chybý Vám tu mapa pro jiný stát nebo je zastaralá? Tak mi napište do <a href="http://www.geocaching.cz/topic/31987-osm-topo-mapa-pro-garmin/" title="Diskuze">diskuze</a>.</strong>
			
			
		</section>

		<section class="manual">
			Každá mapa je vytvořena ve dvou variantách:
			<ul>
				<li>soubor <em>*.zip</em> obsahuje soubory pro použití v BaseCamp</li>
				<li>soubor <em>*.img</em> slouží pro přímé nahrání do GPS</li>
			</ul>

			<h3>Instalace do BaseCamp</h3>
			<ol>
				<li>Nemáte-li, nainstauljte si BaseCamp, Mapsource nebyl testován</li>
				<li>Stáhněte archiv s mapou (přípona *.zip)</li>
				<li>Rozbalte ho do složky s Vašimi mapami (nejčastěji <em>C:/Garmin</em>)</li>
				<li>Otevřete složku, najděte soubor <em>install.bat</em>, klikněte na něj pravým tlačítkem myši a zvlite <em>Spustit jako správce</em></li>
				<li>Postupujte podle pokynů instalátoru</li>
				<li>Užívejte si mapu</li>
				<li>Aktualizace map (nebude-li zmíněno jinak) se provádí pouhým přepisem původních souborů za ty v archivu (nejjednodušší je původní soubory smazat a nové nahrát)</li>
				<li>Případná odinstalace se provádí souborem <em>uninstall.bat</em>, opět ho musíte spustit jako správce</li>
				<li><strong>POZOR! Zatím nefunguje instalace map z programu BaseCamp do GPS (Mapsource se tato chyba zřejmě netýká). Pro instalaci mapy do GPS použijte návod níže.</strong></li>
			</ol>

			<h3>Instalace do GPS</h3>
			<ol>
				<li>Stáhněte soubor <em>*.img</em></li>
				<li>Máte-li velmi starou GPS (např. Garmin Etrex Legend HCx):
					<ul>
						<li>Ta nepodporuje více mapových souborů - musíte proto nejdříve původní mapy zazálohovat</li>
						<li>Stažený soubor přejmenujte na <em>gmapsupp.img</em> a nahrejte do složky <em>Garmin</em> na paměťové kartě vaší GPS</li>
						<li>Takto nelze provozovat více map, proto raději doporučuji instalaci do BaseCamp a následné nahrání map pomocí programu</li>
					</ul>
				</li>
				<li>Máte-li novější GPS, stačí vám soubor jednoduše uložit do složky <em>Garmin</em> na paměťové kartě zařízení.</li>
			</ol>

			<strong>Pozor, raději mapu neukládejte do paměti GPS - mohlo by dojít k zablokování přístroje. Používáte je na vlastní riziko a já, jakožto autor nenesu žádnou odpovědnost za škody jimi způsobené!</strong>

			Chyby, připomínky, návrhy hlaště v <a href="http://www.geocaching.cz/topic/31987-osm-topo-mapa-pro-garmin/" title="Diskuze">diskuzi</a>.
		</section>

		<section class="donation">
			<form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_top">
				<input type="hidden" name="cmd" value="_s-xclick" />
				<input type="hidden" name="hosted_button_id" value="CTME4PA4E6JD2" />
				<input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif" border="0" name="submit" title="PayPal - The safer, easier way to pay online!" alt="Donate with PayPal button" />
			</form>
			<em>Nechcete-li zbytečně platit poplatky PayPalu, napište mi a můžeme najít i jinou cestu...</em>
		</section>
	</main>

</body>

</html>

