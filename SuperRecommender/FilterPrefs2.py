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
    return "True" if request.is_json else "False"
    
    # 
    user = request.form['username'] 
    
    # Get list of new preferences
    prefs_new = request.form['data'].split(", ")

    # Combine old and new preferences
    prefs_all = prefs_saved[user] + prefs_new if user in prefs_saved else prefs_new

    # De-Duplicate prefs and remove conflicting prefs (i.e. "no Will Farrel" and "must have Will Farrel"
    # New prefs take precedent.
    pref_set = set(prefs_all)
    prefs_all = list(pref_set)

    # Update saved preferences
    prefs_saved[user] = prefs_all

    return json.jsonify(username=user, data=prefs_saved[user])

# Error Handling
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404template.html'), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return render_template('404template.html'), 405