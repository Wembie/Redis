<?php

include('vendor/autoload.php');

use Predis\Client;

$client = new Client(['host' => getenv('REDIS_HOST')]);
$client->flushall();
echo "Done!";