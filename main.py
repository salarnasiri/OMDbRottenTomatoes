import argparse
import sys, os
import requests
import json

#consts
VERSION = '0.0.1'
URL = "http://www.omdbapi.com/"

#envs
apikey =  os.environ.get('API_KEY')
if not apikey:
    sys.exit("Please set API_KEY environment variable first")

def requester(get_args: dict):
    get_args.update(dict(apikey = apikey))
    r = requests.get(URL, params = get_args)
    return r.json()

def rottenRateFetcher(imdbID: str):
    movie = requester(dict(i = imdbID))
    for rate in movie["Ratings"]:
        if "Rotten Tomatoes" in rate["Source"]:
            return int(rate["Value"][:-1])

def populate(json_response: list):
    output = []
    for movie in json_response:
        imdbID = movie["imdbID"]
        output.append(dict(
            title = movie["Title"],
            imdbID = imdbID,
            rottenTomatoesPercentage = rottenRateFetcher(imdbID)
            ))
    return output

def prettyPrint(output: list):
    for op in output:
        for movie in op.items():
            print(movie[0]+":", movie[1])
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

args = arg_parser.parse_args()

movies = requester(dict(s = args.name))
prettyPrint(populate(movies["Search"]))
