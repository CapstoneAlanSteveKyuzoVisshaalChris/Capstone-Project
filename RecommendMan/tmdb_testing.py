import requests
import json

from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def assistant(inputValue):
    ###TMDB CLASS#########
    class Tmdb:
        def __init__(self,key):
            self.key = key

        def searchMovieName(self,name):
            url = 'https://api.themoviedb.org/3/search/movie?api_key=' + self.key + '&query='
            if ' ' in name:
                name.replace(' ','+')
            search = url+name
            return requests.get(search).json()

        def searchGenre(self,genre):
            url = 'https://api.themoviedb.org/3/genre/movie/list?api_key=' + self.key + '&query='
            #print("genre: '", genre, "'")
            if ' ' in genre:
                genre.replace(' ','%20')
            genre = genre.capitalize()
            search = url + genre
            req = requests.get(search).json()
            i = 0
            id = 0
            while i < len(req["genres"]):
                if req["genres"][i].get("name") == genre:
                    id = req["genres"][i].get("id")
                i+=1
            return id

        def searchKeyword(self,keyword):
            url = 'https://api.themoviedb.org/3/search/keyword?api_key=' + self.key + '&query='
            if ' ' in keyword:
                keyword.replace(' ','%20')
            search = url + keyword
            return requests.get(search).json()

        def parseTimes(self, movieList, time):
            list = []
            if (movieList.get("total_results")!=0):
                list = movieList['results']
                temp = []
                while list:
                    mv = list.pop()
                    release = mv["release_date"][0:4]
                    if (((time == "new") and (int(release) > 2010)) or ((time == "old") and (int(release) < 1985)) or (time == "")):
                            temp.append(mv)
                while temp:
                    list.append(temp.pop())
            return list
    
        def discover(self,genreID,keywordID):
            url = 'https://api.themoviedb.org/3/discover/movie?api_key=' + self.key + '&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_genres='
            if ' ' in keywordID:
                keywordID.replace(' ','%2C')
            search = url + genreID
            search = search + "&with_keywords=" + keywordID
            return requests.get(search).json()

        def simpleSearch(self,genre,keyword):
            title="NO MOVIE FOUND"
            keyWordID = ""
            genreID=""
            genreID+=str(self.searchGenre(genre))
            for y in keyword:
                key = self.searchKeyword(y)
                res = key['results']
                id = 0
                for x in res:
                    #compare case insensitive
                    if x['name'].casefold() == y.casefold():
                        id = x['id']
                        #print("keyword: ", y)
                        #print("keywordID: ", id)
                        keyWordID += str(id) + ","

            movieList = self.discover(genreID,keyWordID)
            #print(movieList)
            list = self.parseTimes(movieList, time)
            if (movieList.get("total_results")!=0):
                if (len(list) > 0):
                    title = list[0]['title']
            return title
    ######################


    ###startup
    authenticator = IAMAuthenticator('Urysw6Zb3FD5CDASMUiyZEnmcctbDIuPpFUdyTCH3KrL')
    assistant = AssistantV2(
        version='2020-09-26',
        authenticator=authenticator
    )
    assistant.set_service_url('https://api.us-south.assistant.watson.cloud.ibm.com')
    ass_id = '2120d4b4-5d21-4880-981c-245436c7e12f'

    #print(response)
    startstate = 'eyJzZXNzaW9uX2lkIjoiNjc3OGFmYzUtNjExYi00ODQzLWIxMTgtMWRjNjMzZWZiMDg3Iiwic2tpbGxfcmVmZXJlbmNlIjoibWFpbiBza2lsbCIsImFzc2lzdGFudF9pZCI6IjIxMjBkNGI0LTVkMjEtNDg4MC05ODFjLTI0NTQzNmM3ZTEyZiIsImluaXRpYWxpemVkIjp0cnVlLCJkaWFsb2dfc3RhY2siOlt7ImRpYWxvZ19ub2RlIjoiV2VsY29tZSJ9XSwiX25vZGVfb3V0cHV0X21hcCI6eyJXZWxjb21lIjp7IjAiOlswLDBdfX0sImxhc3RfYnJhbmNoX25vZGUiOiJXZWxjb21lIn0='
    state = startstate

    likesActor = []
    dislikesActor = []
    likesGenre = []
    dislikesGenre = []
    ###

    #if/else to see if startstate or not?

    response = assistant.message_stateless(
                assistant_id=ass_id,
                input={
                    'message_type': 'text',
                    'text': inputValue,
                    'options': {
                            'return_context': True
                    }
                },
                context={
                    'skills': {
                        'main skill': {
                            "system": {
                                    'state': state
                            }
                        }
                    }
                }
            ).get_result()
    
    output = response["output"]["generic"]
    print("OUTPUT: ", output)

    if output[0]["text"] == "SEARCH":
        json_str = json.dumps(response, indent=2)
        #SIZE
        size = len(response["output"]["entities"])
        #print(response["output"]["entities"])
        #GENRE
        genre=""
        for word in response["output"]["entities"]:
            if word.get("entity")=="genre":
                    genre = word.get("value")
                    break
        #KEYWORD
        keywords = []
        for word in response["output"]["entities"]:
            if word.get("entity")=="keywords":
                    keywords.append(word.get("value"))
        #TIME
        time = ""
        for word in response["output"]["entities"]:
            if word.get("entity")=="times":
                    time = (word.get("value"))
                    break


        test = Tmdb("6ca5bdeac62d09b1186aa4b0fd678720")
        #print(test.simpleSearch(genre,keywords))
        state=startstate
        #print("THIS IS THE HOME NODE")
        return(test.simpleSearch(genre,keywords))
    else:
        state = response["context"]["skills"]["main skill"]["system"]["state"]
        if output[0]["text"] == "ACTORLIKE":
            for word in response["output"]["entities"]:
                if word.get("entity")=="actornames":
                    #print("YOU LIKE: ", word.get("value"))
                    likesActor.append(word.get("value"))
                    #print("Tell me the actor's/actresses' name and if you like/dislike them. Type \"return\" to go back, or \"list\" to see a list of your preferences.")
                    if word.get("value") in dislikesActor:
                        dislikesActor.remove(word.get("value"))
                    return "ACTORLIKE"
        elif output[0]["text"] == "ACTORDISLIKE":
            for word in response["output"]["entities"]:
                if word.get("entity")=="actornames":
                    print("YOU DISLIKE: ", word.get("value"))
                    print("Tell me the actor's/actresses' name and if you like/dislike them. Type \"return\" to go back, or \"list\" to see a list of your preferences.")
                    dislikesActor.append(word.get("value"))
                    if word.get("value") in likesActor:
                        likesActor.remove(word.get("value"))
                    return "ACTORDISLIKE"
        elif output[0]["text"] == "GENRELIKE":
            for word in response["output"]["entities"]:
                if word.get("entity")=="genre":
                    print("YOU LIKE: ", word.get("value"))
                    likesGenre.append(word.get("value"))
                    print("Tell me the genre name and if you like/dislike them. Type \"return\" to go back, or \"list\" to see a list of your preferences.")
                    if word.get("value") in dislikesGenre:
                        dislikesGenre.remove(word.get("value"))
                    return "GENRELIKE"
        elif output[0]["text"] == "GENREDISLIKE":
            for word in response["output"]["entities"]:
                if word.get("entity")=="genre":
                    print("YOU DISLIKE: ", word.get("value"))
                    dislikesGenre.append(word.get("value"))
                    print("Tell me the genre and if you like/dislike them. Type \"return\" to go back, or \"list\" to see a list of your preferences.")
                    if word.get("value") in likesGenre:
                        likesGenre.remove(word.get("value"))
                    return "GENREDISLIKE"
        elif output[0]["text"] == "ACTORLIST":
            print("YOU LIKE: ", likesActor)
            print("YOU DISLIKE: ", dislikesActor)
            return "ACTORLIST"
        elif output[0]["text"] == "GENRELIST":
            print("YOU LIKE: ", likesGenre)
            print("YOU DISLIKE: ", dislikesGenre)
            return "GENRELIST"
        elif output[0]["text"] == "GENREALL":
            print("ACTION, ADVENTURE, COMEDY, CRIME")
            print("DRAMA, FAMILY, FANTASY, HISTORY")
            print("HORROR, MUSIC, MYSTERY, ROMANCE")
            print("SCI-FI, THRILLER, WAR, WESTERN")
            return "GENREALL"
        else:
            #print(output)
            for resp in output:
                print(resp["text"])
            return (output[0]["text"])

    #usertext = input("YOUR INPUT HERE: ")
    #print(state)
