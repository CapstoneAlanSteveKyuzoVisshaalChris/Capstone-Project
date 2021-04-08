import requests
import json
import storage
import statelist
import difflib

from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

###Return a list: the string to output, and the state
retpack = ["returnstmt", "statestring"]
def assistant(inputValue, storage):
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

    #gets person name from tmdb using search func and return the json output
        def searchPerson(self, person):
            url = 'https://api.themoviedb.org/3/search/person?api_key=' + self.key + '&query='
            if ' ' in person:
                person.replace(' ','%20')
            search = url + person
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
        #discover function with all relevant searches that we need. In depth search discover
        def discover(self,genreID,keywordID,personID):
            url = 'https://api.themoviedb.org/3/discover/movie?api_key=' + self.key + '&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_people='
            if ' ' in keywordID:
                keywordID.replace(' ','%2C')
            #dont need to replace because there is only 1 person that we are searching for
            search = url + personID
            search = search + "&with_genres=" + genreID
            search = search + "&with_keywords=" + keywordID
            return requests.get(search).json()

        #discover with only keywords and genre needed
        def simpleDiscover(self,genreID,keywordID):
                url = 'https://api.themoviedb.org/3/discover/movie?api_key=' + self.key + '&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_genres='
                if ' ' in keywordID:
                    keywordID.replace(' ','%2C')
                search = url + genreID
                search = search + "&with_keywords=" + keywordID + "&without_keywords=9663" #remove sequels
                return requests.get(search).json()

        def simpleSearch(self,genre,keyword,person):
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

            personJson = self.searchPerson(person)
            personID = str(personJson["results"][0]["id"])
        

            movieList = self.discover(genreID,keyWordID,personID)
            list = self.parseTimes(movieList, time)
            if (movieList.get("total_results")!=0):
                if (len(list) > 0):
                    title = list[0]['title']
            return title

        #want to return a list of jsons for each movie
        def advancedSearch(self,genre,keyword):
            people = storage.getLikesActor()
            badppl = storage.getDislikesActor()
            recommendList = []
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
        
            #must check if there are person preferences
            if len(people) != 0:
                for name in people:
                    personJson = self.searchPerson(name)
                    personID = str(personJson["results"][0]["id"])
                    movieList = self.discover(genreID,keyWordID,personID)
                    list = self.parseTimes(movieList, time)
                    if (movieList.get("total_results")!=0):
                        if (len(list) > 0):
                            result = list[0]
                            #for loop here iterating through the list of movies (get like the 3 top movies)
                            i = 0;
                            for result in list:
                                recommendList.append(result)
                                if i >2:
                                    break
                                i+=1
                #now that we have some movies with people, now we need to find movies without people and where time does not matter
            simpleMovieList = self.simpleDiscover(genreID,keyWordID)
            if simpleMovieList["total_results"] != 0:
                for result in simpleMovieList["results"]:
                    #print("results: " + result)
                    recommendList.append(result)

            #get cast of movies, exclude any with actors u dont like
            #print("lis" + recommendList)
            #print("RL", recommendList)
            #print(recommendList[0]["id"])
            if(recommendList):
                print(recommendList[0]["id"])
            for movie in recommendList:
                cast = requests.get("https://api.themoviedb.org/3/movie/" + str(movie["id"]) + "/credits?api_key=6ca5bdeac62d09b1186aa4b0fd678720&language=en-US").json()
                #print(movie)
                minsize = 10
                castsize = len(cast["cast"])
                if castsize < 10:
                    minsize = castsize
                for member in range(minsize):
                    for badperson in badppl: 
                        if cast["cast"][member]["name"] == badperson:
                            recommendList.remove(movie)


            storage.updateRecommends(recommendList)
            print(recommendList)
            return recommendList
        
    #test = Tmdb("")
    #print(test.advancedSearch(genre,keywords,likesActor))

    def splitter(s):
        slen = len(s)
        i = 0
        phrases = 0
        current = ""
        ch = ""
        sep = []
        while (i < slen):
          ch = s[i]
          if phrases == 0 :
            if (ch == "/"):
              i -=1
              phrases = 1
            else:  
              if (ch != " "):
                current = current + str(ch)
              else:
                if current != " " and len(current) != 0:
                  sep.append(current)
                current = ""
          if phrases == 1:
            if ch != "/":
              current = current + str(ch)
            else:
              if current != " " and len(current) != 0:
                phrases = 0
                sep.append(current)
              current = ""
          i+=1
        sep.append(current)
        for a in sep: 
          if a.isspace() or len(a) == 0:
            sep.remove(a)
        return sep

    ###startup
    authenticator = IAMAuthenticator('Urysw6Zb3FD5CDASMUiyZEnmcctbDIuPpFUdyTCH3KrL')
    assistant = AssistantV2(
        version='2020-09-26',
        authenticator=authenticator
    )
    assistant.set_service_url('https://api.us-south.assistant.watson.cloud.ibm.com')
    ass_id = '2120d4b4-5d21-4880-981c-245436c7e12f'

    #print(response)
    startstate = statelist.startState()
    searchstate = '0'
    state = storage.getState()

    inp_arr = splitter(inputValue)

    #likesActor = []
    #dislikesActor = []
    #likesGenre = []
    #dislikesGenre = []
    ###

    #if/else to see if startstate or not?

    if state != "CONFIRM":

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
        if ("text" in output[0]):

            print("OUTPUT[0][\"text\"]: ", output[0]["text"])

            if output[0]["text"] == "SEARCH":
                json_str = json.dumps(response, indent=2)
                #SIZE
                size = len(response["output"]["entities"])
                print(response)
                print(response["output"]["entities"])
                #GENRE
                genre=""
                for word in response["output"]["entities"]:
                    if word.get("entity")=="genre":
                            genre = word.get("value")
                            break
                #KEYWORD
                keywords = []
                keywordscand = []
                for word in response["output"]["entities"]:
                    if word.get("entity")=="keywords":
                            keywordscand.append(word.get("value"))
                for w in inp_arr:
                    close = difflib.get_close_matches(w, keywordscand)
                    if len(close) > 0:
                        keywords.append(close[0])
                print(keywordscand)
                print(keywords)
                #TIME
                time = ""
                for word in response["output"]["entities"]:
                    if word.get("entity")=="times":
                            time = (word.get("value"))
                            break


                test = Tmdb("6ca5bdeac62d09b1186aa4b0fd678720")
                #print("genre", genre)
                print("kiwi", keywords)
                #print(test.simpleSearch(genre,keywords))
                state=statelist.searchState()
                #print("THIS IS THE HOME NODE")
                movieList = test.advancedSearch(genre,keywords)
                print("MOVIELIST")
                print(movieList)
                if len(movieList) != 0:
                    title = movieList[0]["title"]
                    overview = movieList[0]["overview"]
                    poster = "https://www.themoviedb.org/t/p/original" + movieList[0]["poster_path"]
                    storage.popRecommends()
                    storage.setChosenMovie(title)
                    return[[poster, "'<b>" + title + "</b>' ~~~~~ Here is an overview: " + overview , "\nDo you want this movie?\t- [Y/N]"],"CONFIRM"]
                else:
                    return[["Sorry, there are no movies that fit your query :(" , "Are you looking for a movie recommendation, trying to update your movie preferences, or trying to learn more about Recommend-Man?"], statelist.startState()]
            else:
                state = response["context"]["skills"]["main skill"]["system"]["state"]
                if output[0]["text"] == "ACTORLIKE":
                    for word in response["output"]["entities"]:
                        if word.get("entity")=="actornames":
                            storage.addLikesActor(word["value"])
                            return [["You like "+word["value"], "Tell me if you like/dislike another actor, type \"list\" to see a list of preferences, or \"return\" to go back."] ,state]
                elif output[0]["text"] == "ACTORDISLIKE":
                    for word in response["output"]["entities"]:
                        if word.get("entity")=="actornames":
                            storage.addDislikesActor(word["value"])
                            return [["You dislike "+word["value"],  "Tell me if you like/dislike another actor, type \"list\" to see a list of preferences, or \"return\" to go back."],state]
                elif output[0]["text"] == "GENRELIKE":
                    for word in response["output"]["entities"]:
                        if word.get("entity")=="genre":
                            storage.addLikesGenre(word["value"])
                            return [["You like "+word["value"], "Tell me if you like/dislike another genre, type \"list\" to see a list of preferences, or \"return\" to go back."],state]
                elif output[0]["text"] == "GENREDISLIKE":
                    for word in response["output"]["entities"]:
                        if word.get("entity")=="genre":
                            storage.addDislikesGenre(word["value"])
                            return [["You dislike "+word["value"], "Tell me if you like/dislike another genre, type \"list\" to see a list of preferences, or \"return\" to go back."],state]
                elif output[0]["text"] == "ACTORLIST":
                    likeslist = storage.printLikesActor()
                    dislikeslist = storage.printDislikesActor()
                    return [[likeslist+"  "+dislikeslist , "Tell me the actor's/actresses' name and if you like/dislike them. Type \"return\" to go back, or \"list\" to see a list of your preferences."],state]
                elif output[0]["text"] == "GENRELIST":
                    likeslist = storage.printLikesGenre()
                    dislikeslist = storage.printDislikesGenre()
                    return [[likeslist+"  "+dislikeslist,  "Tell me the actor's/actresses' name and if you like/dislike them. Type \"return\" to go back, or \"list\" to see a list of your preferences."],state]
                #elif output[0]["text"] == "RESET":
                #    storage.clearPrefs()
                #    return ["Preferences are reset. Are you looking for a movie recommendation, trying to update your movie preferences, or trying to learn more about Recommend-Man?", statelist.startState]
                elif output[0]["text"] == "GENREALL":
                    #print("ACTION, ADVENTURE, COMEDY, CRIME")
                    #print("DRAMA, FAMILY, FANTASY, HISTORY")
                    #print("HORROR, MUSIC, MYSTERY, ROMANCE")
                    #print("SCI-FI, THRILLER, WAR, WESTERN")
                    return [["ACTION, ADVENTURE, COMEDY, CRIME, DRAMA, FAMILY, FANTASY, HISTORY, HORROR, MUSIC, MYSTERY, ROMANCE, SCI-FI, THRILLER, WAR, WESTERN",  "Do you want a list of genres, an example of keywords, or return?"],state]
                else:
                    responses = []
                    for resp in output:
                        print(resp["text"])
                        responses.append(resp["text"])
                    if len(responses) == 1:
                        retpack[0] = responses[0]
                    else:
                        retpack[0] = responses
                    retpack[1] = state
                    print(retpack[0])
                    return retpack
        else:
            return[["Sorry, I didn't understand.", "Are you looking for a movie recommendation, trying to update your movie preferences, or trying to learn more about Recommend-Man?"], state]

    elif state == "CONFIRM":
        if inputValue=="Y" or inputValue == "y":
            return [["OK! Have fun watching " + storage.getChosenMovie() + "!", "Are you looking for a movie recommendation, trying to update your movie preferences, or trying to learn more about Recommend-Man?"], statelist.startState()]
        elif inputValue=="N" or inputValue == "n":
            if len(storage.getRecommends()) > 0:
                title = storage.getRecommends()[0]["title"]
                overview = storage.getRecommends()[0]["overview"]
                poster = "https://www.themoviedb.org/t/p/original" + storage.getRecommends()[0]["poster_path"]
                storage.popRecommends()
                storage.setChosenMovie(title)
                return [[poster, "'<b>" + title + "</b>' ~~~~~ Here is an overview: " + overview , "\nHow about this one?\t- [Y/N]"], "CONFIRM"]
            else:
                return[["Sorry, there are no more movies that fit your query :(" , "Are you looking for a movie recommendation, trying to update your movie preferences, or trying to learn more about Recommend-Man?"], statelist.startState()]


    #usertext = input("YOUR INPUT HERE: ")
    #print(state)
