import requests
import json
class Tmdb:
    def __init__(self,key):
        self.key = key

    def searchMovieName(self,name):
        url = 'https://api.themoviedb.org/3/search/movie?api_key=' + self.key + '&query='
        if ' ' in name:
            name.replace(' ','+')
        search = url+name
        return requests.get(search).json()

    def searchKeyword(self,keyword):
        url = 'https://api.themoviedb.org/3/search/keyword?api_key=' + self.key + '&query='
        if ' ' in keyword:
            keyword.replace(' ','%20')
        search = url + keyword
        return requests.get(search).json()
    
    def discover(self,keywordID):
        url = 'https://api.themoviedb.org/3/discover/movie?api_key=' + self.key + '&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_keywords='
        if ' ' in keywordID:
            keywordID.replace(' ','%2C')
        search = url + keywordID
        return requests.get(search).json()


    def simpleSearch(self,keyword):

        key = self.searchKeyword(keyword)
        res = key['results']
        id = 0
        for x in res:
            #compare case insensitive
            if x['name'].casefold() == keyword.casefold():
                id = x['id']
                break
        movieList = self.discover(str(id))

        return movieList['results'][0]['title']


test = Tmdb("6ca5bdeac62d09b1186aa4b0fd678720")
print(test.simpleSearch("trash"))
