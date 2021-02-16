#https://developers.themoviedb.org/3/discover/movie-discover
#6ca5bdeac62d09b1186aa4b0fd678720 api key for movie database

import requests
import json
from tmdb import Tmdb

test = Tmdb("6ca5bdeac62d09b1186aa4b0fd678720")

print(test.searchMovieName("Deadpool"))

