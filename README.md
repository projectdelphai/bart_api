bart_api
=============
Reuben Castelino - projectdelphai@gmail.com

Description
-------------
A simple python package that interacts with the [Bay Area Rapid Transit API](http://api.bart.gov/docs/overview/index.aspx).

Usage
-------------

install bart_api with:

    git clone github.com/projectdelphai/bart/api
    sudo python setup.py install

To create a new object:

    from bart_api import BartApi

    bart = BartApi()

If you have your own API key (which you can get at the BART API website), you can use that instead of the default free one with:

    bart = BartApi("YOUR_API_KEY_HERE")

To get the number of live trains:

    live_trains = bart.number_of_trains()

Todo
-----------------
* make method for delays
* make method for stations
* make method for arrival/destination estimations
* make method for routes


Helping Out
-------------

 1. Create an issue (optional)
 1. Clone the codebase
 1. Create a branch
 1. Make your changes
 1. Write tests
 1. Merge branch
 1. Make a pull request

