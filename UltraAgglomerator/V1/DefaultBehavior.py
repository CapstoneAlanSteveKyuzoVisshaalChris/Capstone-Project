from flask import Flask, abort, session, redirect, url_for, request, render_template, json
from markupsafe import escape 

# Basically "name = __init___", but for web servers
app = Flask(__name__)

# The secret ingredient is... how we store session data.
app.secret_key = b'\xe1q\xf5\xd4\xa3=\xa8\xc0\x18\xf9\xb3G`\xe0"\xa2'

"""CAUTION: PREFERENCES ARE DELETED UPON SERVER SHUTDOWN"""
prefs_saved = {} 

# Main Page
@app.route('/', methods=['POST'])
def index():
    # Check that JSON was received
    if request.is_json == False:
        return "Bad Request", 400
    
    # "Log in" the user
    user = request.json['username'] 
    
    # Get list of new preferences
    prefs_new = request.json['pref_data']

    # Combine old and new preferences
    prefs_all = prefs_saved[user] + prefs_new if user in prefs_saved else prefs_new

    # TODO: De-Duplicate prefs and remove conflicting prefs (i.e. "no Will Farrel" and "must have Will Farrel"
    # TODO: New prefs take precedent
    pref_set = set(prefs_all)
    prefs_all = list(pref_set)

    # Update saved preferences
    prefs_saved[user] = prefs_all

    # TODO: Neural Network ("Pseudo-Netflix problem")

    # TODO: TMDB Search

    TMDB_results = []

    #Return results if there are any, else return "No Results"
    if len(TMDB_results) > 0:
        return json.jsonify("??????") 
    else:
        return json.jsonify("No Results") 
    

# Error Handling
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404template.html'), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return render_template('404template.html'), 405