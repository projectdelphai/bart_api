bart_api
=============
Reuben Castelino - projectdelphai@gmail.com

Description
-------------
A simple python package that interacts with the [Bay Area Rapid Transit API](http://api.bart.gov/docs/overview/index.aspx).

Usage
-------------

install bart_api with:

    git clone github.com/projectdelphai/bart_api
    sudo python setup.py install

To create a new object:

    from bart_api import BartApi

    bart = BartApi()

If you have your own API key (which you can get at the BART API website), you can use that instead of the default free one with:

    bart = BartApi("YOUR_API_KEY_HERE")

To get the number of live trains:

    live_trains = bart.number_of_trains()

To get the status of all elevators:

    elevators_status = bart.elevator_status()

All responses for now are returned as lxml etrees.

To get all recorded stations:

    station_list = bart.get_stations()

This is important because you need the abbreviation necessary to find further information about a station or a route. Once you have your list of stations, you can find the abbreviation for your station by iterating through the list, comparing the name with the one you want

    if entry.find("name").text == "West Oakland"

then grabbing the abbreviation:

    entry.find("abbr").text

You can get the info about a station with

    info = bart.station_info(station_abbr)

To get the access information of a station (directions, lockers, parking, entering and exiting):

    access_info = bart.station_access(station_abbr, legend)

Legend must be in the form of "0" or "1". If nothing, it defaults to 1.

To get the estimated time of departure for a station:

   departures = bart.etd(station_abbr, platform_number, direction)

The station abbreviation defaults to all if nothing else if placed. Nothing else can be used if you make station abbreviation all. If you have a specific station, you can specify either th eplatform number or the direction. The direction must be either "s" or "n" (southbound or northbound). If both are used, platform will be used over direction.

To get all routes:

   routes = bart.routes(sched, date)

sched is the currently used schedule (which as of oct 27, 2013 is 32). If there is no schedule, it defaults to date which if not specified defaults to today. The date format is mm/dd/yyyy. You can also use today or now.

To get specific info about a route use:

    route_info = bart.route_info(route, sched, date)

sched is used over date if both are supplied.

To run the tests to make sure everything is running well, run this command in the root directory:

    python -m unittest discover

Todo
-----------------
* remove duplicate code into a better method

Helping Out
-------------

 1. Create an issue (optional)
 1. Fork the codebase
 1. Create a branch
 1. Make your changes
 1. Write tests
 1. Merge branch
 1. Make a pull request

Changelog
--------------
0.0.3
* made methods for all but three of the schedule methods
* started transitioning to return dicts
* implemented easier search for item method

0.0.2
* made methods for everything but the schedule section

0.0.1
* working through advisory information part of api
* designed structure for tests and packaging
