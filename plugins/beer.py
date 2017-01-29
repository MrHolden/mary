import requests

from cloudbot import hook
from cloudbot.util import web, botvars

class APIError(Exception):
    pass

# API Constants
beerdb_api = "http://api.brewerydb.com/v2/search/?q={}&type=beer&withBreweries=Y&p=1&key={}"
api_key = "71b949fae6ac19d96896497fae3c50aa"

@hook.command("beer", autohelp=False)
def beer_search(text, reply, nick, notice):
    """beer <search> -- Searches BreweryDB for first matching item."""

    lookup = text.strip().lower()
    url = beerdb_api.format(lookup, api_key)
    global beerjson
    beerjson = requests.get(url).json()
    
    # put all beer data into dictionary for easy formatting
    beer_data = {
        "name": beerjson['data'][0]['name'],
        "style": beerjson['data'][0]['style']['name'],
        "brewery": beerjson['data'][0]['breweries'][0]['name'],
    }
    

    # output a pretty blurb with beer info
    out = "\x02Beer:\x02 {}".format(beer_data["name"])
    if beer_data["brewery"]:
        out += ", \x02Brewery:\x02 {}".format(beer_data["brewery"])
    if beer_data["style"]:
        out += ", \x02Style:\x02 {}".format(beer_data["style"])
    try:
        out += ", \x02ABV:\x02 {}%".format(beerjson['data'][0]['abv'])
    except KeyError:
        pass
    try:
        out += ", \x02Availability:\x02 {}".format(beerjson['data'][0]['available']['name'])
    except KeyError:
        pass
    reply(out)
