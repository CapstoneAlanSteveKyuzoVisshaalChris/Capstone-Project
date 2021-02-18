import requests
import json

from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator('Urysw6Zb3FD5CDASMUiyZEnmcctbDIuPpFUdyTCH3KrL')
assistant = AssistantV2(
    version='2020-09-26',
    authenticator=authenticator
)
assistant.set_service_url('https://api.us-south.assistant.watson.cloud.ibm.com')
ass_id = '2120d4b4-5d21-4880-981c-245436c7e12f'

response = assistant.create_session(
    assistant_id=ass_id
).get_result()

sess_id=  response["session_id"]

response = assistant.message(
    assistant_id=ass_id,
    session_id=sess_id,
    input={
        'message_type': 'text',
        'text': 'crime movie with cool car chase and nice soundtrack'
    }
).get_result()

json_str = json.dumps(response, indent=2)
#SIZE
size = len(response["output"]["entities"])
print(size)
print(response["output"]["entities"])
#GENRE
genre = response["output"]["entities"][0]["value"]
#KEYWORD
keywords = []
i = 1
while (i < size):
    print(i)
    keywords.append(response["output"]["entities"][i]["value"])
    i+=1
print(keywords)



response = assistant.delete_session(
    assistant_id=ass_id,
    session_id=sess_id
).get_result()



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
        keyWordID = "";
        for y in keyword:
            key = self.searchKeyword(y)
            res = key['results']
            id = 0
            for x in res:
                #compare case insensitive
                if x['name'].casefold() == y.casefold():
                    id = x['id']
                    print(id)
                    keyWordID += str(id) + ","

            movieList = self.discover(keyWordID)

        return movieList['results'][0]['title']


test = Tmdb("6ca5bdeac62d09b1186aa4b0fd678720")
keyword = keywords
print(test.simpleSearch(keyword))
