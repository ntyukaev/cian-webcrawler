# Cian Web Crawler

This Python package serves to collect real estate data from [cian.ru](https://cian.ru) using [Scrapy](https://scrapy.org/).

## Requirements

* Python 3.10 or higher is recommended
* Node js

## Installation

Go the project folder and install Python dependencies:

```sh
pip install -r requirements.txt
```

## Usage

The package stores data in a database and also notifies you by email.
Before using the package, you should provide the following environment variables:

- `USER_AGENT`: A user agent string. For more information, refer to [the official documentation](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent). Example value: `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36`.
- `CONNECTION_STRING`: A database connection string. More information [here](https://en.wikipedia.org/wiki/Connection_string). Example: `sqlite:///flats.sqlite`.
- `MAIL_HOST`: Mail server hostname.
- `MAIL_PASS`: Mail server password.
- `MAIL_USER`: Mail sender.
- `MAIL_PORT`: Mail server port.
- `MAIL_RECIPIENT`:  Mail recipient.

For email server configuration, you can use gmail.com. [This article](https://kinsta.com/blog/gmail-smtp-server/) describes the steps to configure a gmail smtp server.

After you set up the environment variables, go to the project folder and run the following command:

```sh
scrapy crawl cian \
-a location=<location string> \
-a minprice=<min price in rubles> \
-a maxprice=<max price in rubles>
```

## Spider Reference

The spider has the following arguments (all arguments are passed as `-a name=val`): 

* `location`: (Required) A real address that identifies a location.
* `minprice`: (Required) A min price for real estate objects
* `maxprice`: (Required) A max pice for real estate objects
* `zoom`: (Optional. Defaults to `0.001`) A variable used to create a location polygon (Check [estate/spiders/cian.py](estate/spiders/cian.py)). The bigger the value of `zoom`, the bigger the location polygon.
* `step`: (Optional. Defaults to `0.001`) A variable used to split the location polygon into multiple polygons. The more polygons generated, the more results you get.
* `room1`: (Optional. Defaults to `1`) If set to `1`, include one-room apartments, otherwise set to `0`.
* `room2`: (Optional. Defaults to `0`) If set to `1`, include two-room apartments, otherwise set to `0`.
* `room3`: (Optional. Defaults to `0`) If set to `1`, include three-room apartments, otherwise set to `0`.
* `room4`: (Optional. Defaults to `0`) If set to `1`, include four-room apartments, otherwise set to `0`.
