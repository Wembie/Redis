<?php

include('vendor/autoload.php');

use App\Home\Home;
use App\Home\HomeCache;
use Predis\Client;

$home = new Home();

$client = new Client(['host' => getenv('REDIS_HOST')]);

if (isset($_GET['cache'])) {
	$home = new HomeCache($client);
}


$start_time = microtime(true);


$cookie_name = "myapp__id_session";
$cookie_value = "123456";
setcookie($cookie_name, $cookie_value, time() + (86400 * 30), "/"); // 86400 = 1 day

?>
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

	<title>MPWEB Redis Demo</title>

	<!-- Bootstrap core CSS -->
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
		  integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
</head>

<body>

<div class="container">

	<div class="row row-offcanvas row-offcanvas-right">

		<div class="col-12 col-md-9">
			<?php
			$greeting = $home->greeting();


			?>
			<div class="jumbotron">
				<h1><?= $greeting['title'] ?></h1>

				<p><?= $greeting['subtitle'] ?></p>
			</div>
			<div class="row">
				<?php
				$articles = $home->articles();
				?>
				<?php foreach ($articles as $article): ?>
				<div class="col-6 col-lg-4">
					<h2><?= $article['title'] ?></h2>
					<p><?= $article['text'] ?></p>
				</div>
				<?php endforeach; ?>


				<!--/span-->
			</div>
			<!--/row-->
		</div>
		<!--/span-->

		<div class="col-6 col-md-3 sidebar-offcanvas" id="sidebar">
			<div class="list-group">
				<?php
				$topCommentators = $home->topCommentatorsWeek();
				?>
				<span class="list-group-item active">Top commentators week</span>
				<?php foreach ($topCommentators as $topCommenter): ?>
					<span class="list-group-item"><?= $topCommenter ?> </span>
				<?php endforeach; ?>
			</div>
		</div>
		<!--/span-->
		<div class="col-6 col-md-3 sidebar-offcanvas" id="sidebar">
			<div class="list-group">
				<?php
				$mostVisitedPages = $home->mostVisitedPages();
				?>
				<span href="#" class="list-group-item active">Most visited pages</span>
				<?php foreach ($mostVisitedPages as $mostVisitedPage): ?>
					<span class="list-group-item"><?= $mostVisitedPage['name'] ?> (<?= $mostVisitedPage['views'] ?> views) </span>
				<?php endforeach; ?>
			</div>
		</div>
		<!--/span-->
	</div>
	<!--/row-->

	<hr>

	<footer>
		<p>&copy; MPWEB 2017</p>
		<p>Tiempo de carga de la home: <span style="background-color:# ffbb33"><?= round(microtime(true) - $start_time, 2); ?> segundos </span> </p>
		<p>
			<a href="/flushall.php">Flush-all</a>
		</p>
		<p>
			<a href="/heatcache.php">Precalentar cache</a>
		</p>



	</footer>

</div>
<!--/.container-->
</body>
</html>
