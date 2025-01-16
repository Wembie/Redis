<?php


namespace App\Home;

class HomeCache extends Home
{
	/** @var Client */
	private $client;

	/**
	 * HomeCache constructor.
	 * @param \Predis\Client $client
	 */
	public function __construct(\Predis\Client $client)
	{
		$this->client = $client;
	}

	public function greeting()
	{
		$key = 'home:greeting';

		if ($this->client->exists($key)) {
			return json_decode($this->client->get($key), true);
		}

		$data = parent::greeting();
		$this->client->set($key, json_encode($data));
		return $data;
	}

	public function topCommentatorsWeek()
	{
		$key = 'home:topCommentsWeek';
		if (!$this->client->exists($key))
		{
			return [];
		}

		return json_decode($this->client->get($key), true);
	}

	public function mostVisitedPages()
	{
		$key = 'home:mostVisitedPages';

		if ($this->client->exists($key)) {
			return json_decode($this->client->get($key), true);
		}

		$data = parent::mostVisitedPages();
		$this->client->set($key, json_encode($data));
		$this->client->expireat($key, strtotime("+1 minute"));
		return $data;
	}

	public function articles()
	{
		$key = 'home:articles';

		if ($this->client->exists($key)) {
			return json_decode($this->client->get($key), true);
		}

		$data = parent::articles();
		$this->client->set($key, json_encode($data));
		return $data;
	}

}