"""
Fetches rotten tomatoes from http://www.omdbapi.com/ website
"""

import argparse
import sys
import os
import requests

#consts
VERSION = '0.0.1'
URL = "http://www.omdbapi.com/"

#envs
apikey =  os.environ.get('API_KEY')
if not apikey:
    sys.exit("Please set API_KEY environment variable first")

def requester(get_args: dict) -> dict:
    """
    Appends apikey to the params and requests to the url
    """
    get_args.update(dict(apikey = apikey))
    response = requests.get(URL, params = get_args)
    return response.json()

def rotten_rate_fetcher(imdb_id: str) -> int:
    """
    Fetches the rotten tomatoes removes % and also will return None if no rotten tomatoes found
    """
    movie = requester(dict(i = imdb_id))
    for rate in movie["Ratings"]:
        if "Rotten Tomatoes" in rate["Source"]:
            return int(rate["Value"][:-1])
    return None

def populate(json_response: list) -> list:
    """
    Creates a list for output
    """
    output = []
    for movie in json_response:
        imdb_id = movie["imdbID"]
        output.append(dict(
            title = movie["Title"],
            imdbID = imdb_id,
            rottenTomatoesPercentage = rotten_rate_fetcher(imdb_id)
            ))
    return output

def pretty_print(output: list):
    """
    Human readable print for output
    """
    for movie in output:
        for item in movie.items():
            print(item[0]+":", item[1])
        print()

#argParser
arg_parser = argparse.ArgumentParser(
    usage = '%(prog)s name',
    description = 'Get Rotten Tomato of movie',
    epilog='Enjoy the program! :)')
arg_parser.version = VERSION

arg_parser.add_argument(
    'name',
    metavar = 'name',
    type = str,
    help = 'the name of the movie for search')

arg_parser.add_argument(
    '-j',
    '--json',
    action="store_true",
    help = 'json output')

args = arg_parser.parse_args()

if __name__ == '__main__':
    movies = requester(dict(s = args.name))
    if args.json:
        print(populate(movies["Search"]))
    else:
        pretty_print(populate(movies["Search"]))
