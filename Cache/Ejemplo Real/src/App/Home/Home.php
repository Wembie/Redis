<?php namespace App\Home;


class Home
{

	public function greeting()
	{
		usleep(200000); // 200ms
		return [
			'title' => 'Redis Demo',
			'subtitle' => 'Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui.',

		];
	}

	public function topCommentatorsWeek()
	{
		usleep(1200000); // 1.2 second

		return [
			'Jimmy',
			'Fred',
			'Greg',
			'Alice',
			'Melania',
		];
	}

	public function mostVisitedPages()
	{
		usleep(1300000); // 1.3 second

		return [
			['name' => 'Foo', 'views' => rand(300, 400)],
			['name' => 'Bar', 'views' => rand(200, 300)],
			['name' => 'Dump', 'views' => rand(100, 200)],
		];
	}

	public function articles()
	{
		usleep(350000); // 350ms

		return [
			[
				'title' => 'Lorem ipsum',
				'text'  => 'Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui.',
			],
			[
				'title' => 'Gravida at',
				'text'  => 'Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui.',
			],
			[
				'title' => 'Tellus ac cursus',
				'text'  => 'Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui.',
			],
		];
	}

}