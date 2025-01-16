<?php


include('vendor/autoload.php');

use Predis\Client;
use App\Home\Home;

$home = new Home();
$client = new Client(['host' => getenv('REDIS_HOST')]);
$topCommentators = $home->topCommentatorsWeek();
$client->set('home:topCommentsWeek', json_encode($topCommentators));
echo "Done!";
