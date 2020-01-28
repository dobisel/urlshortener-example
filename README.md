# urlshortener-example
[![Build Status](https://travis-ci.com/amirRamirfatahi/simplebitly.svg?branch=master)](https://travis-ci.com/amirRamirfatahi/simplebitly)
[![Coverage Status](https://coveralls.io/repos/github/amirRamirfatahi/simplebitly/badge.svg?branch=master)](https://coveralls.io/github/amirRamirfatahi/simplebitly?branch=master)

Simple_bitly is a URL shortener software.

This project has been developed solely for technical purposes.

This is demo projcet for [yhttp](https://github.com/yhttp/yhttp).

## Installation
First you need to clone the project or download it directly.

```bash
git clone https://github.com/yhttp/urlshortener-example
cd urlshortener-example
pip install .
```

Or

```bash
pip install git+https://github.com/yhttp/urlshortener-example
```

## Deployment
You can use [gunicorn](https://gunicorn.org/) to serve our wsgi application.

```bash
pip install gunicorn
```

you can deploy the `generator` using the following command.

**Note**: You can bind it to any address of your liking.

```bash
cd path/to/urlshortener-example
gunicorn shortener:app --bind localhost:8000
```


## Usage
To use `urlshortener-example` use the following command to send a your URL to the app.
```bash
curl localhost:8000 -X POST -d "url=[some long URL]"
```

Now take the accquired short URL to make a request to get redirected.
You can use a web browser for this part as it's a simple *GET* request.
so simply visit `localhost:8000/[short URL]`.

Now you must be automatically redirected to your original URL.


## Tests
Install the necessary packages to contribute or run tests.

```bash
pip install -r requirements-dev.txt
```

We use [bddrest](https://github.com/pylover/bddrest) to test our project.


## Contributing
Pull requests are welcome.
Please make sure to update tests as appropriate if you decide to make a pull request.


## License
[MIT](https://choosealicense.com/licenses/mit/)

