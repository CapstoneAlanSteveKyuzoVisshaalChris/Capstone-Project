import requests
import json
import storage
import statelist
import difflib
import random
import girls

from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

###Return a list: the string to output, and the state
retpack = ["returnstmt", "statestring"]
def assistant(inputValue, storage):

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

    #likesActor = []
    #dislikesActor = []
    #likesGenre = []
    #dislikesGenre = []
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
    
    #print(response)
    output = response["output"]["generic"]
    if ("text" in output[0]):

        #print("OUTPUT[0][\"text\"]: ", output[0]["text"])

        if output[0]["text"] == "SEARCH":
            json_str = json.dumps(response, indent=2)
            #SIZE
            size = len(response["output"]["entities"])
            #print(response)

            #HOBBIES
            hobbies = []
            for word in response["output"]["entities"]:
                print(word)
                if word.get("entity")=="hobbies":
                        print("Match!")
                        hobbies.append(word.get("value"))
            print(hobbies)
            #have to fuzze?? TODO
            #print(keywordscand)
            #print(keywords)

            g = girls.Girls()

            bestgirl = g.search(hobbies)
            if bestgirl[0] == "None":
                return[["No matches found!", "Are you looking for a date recommendation, or trying to learn more about Recommend-Man?"], statelist.startState()]
            else:
                return[[bestgirl[0], g.details(hobbies, bestgirl), "Are you looking for a date recommendation, or trying to learn more about Recommend-Man?"], statelist.startState()]
        else:
            state = response["context"]["skills"]["main skill"]["system"]["state"]
            return[[response["output"]["generic"][0]["text"]], state]
    else:
        return[["Sorry, I didn't understand.", "Are you looking for a date recommendation, or trying to learn more about Recommend-Man?"], state]
