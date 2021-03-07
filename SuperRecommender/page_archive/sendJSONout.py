from flask import Flask, abort, session, redirect, url_for, request, render_template, json
from markupsafe import escape 

# ????
app = Flask(__name__)
app.secret_key = b'\xe1q\xf5\xd4\xa3=\xa8\xc0\x18\xf9\xb3G`\xe0"\xa2'

prefs_saved = {} # CAUTION: ONLY SAVED WHILE SERVER IS RUNNING! RESETS EVERY SESSION!


# Main Page
@app.route('/', methods=['POST'])
def index():
    # 
    user = request.form['username'] 
    
    # Get list of new preferences
    prefs_new = request.form['data'].split(", ")

    # Combine new preferences and old preferences
    prefs_all = prefs_saved[user] + prefs_new if user in prefs_saved else prefs_new

    # De-Duplicate prefs and remove conflicting prefs (i.e. "no Will Farrel" and "must have Will Farrel"
    # New prefs take precedent.

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