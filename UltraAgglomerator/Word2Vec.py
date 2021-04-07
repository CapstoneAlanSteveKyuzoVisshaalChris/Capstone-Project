from flask import Flask, abort, session, redirect, url_for, request, render_template, json
from markupsafe import escape
from GloVe_Python.distance_pre import related_words

# Basically "name = __init___", but for web servers
app = Flask(__name__)

# Main Page
@app.route('/', methods=['POST'])
def index():
    # Check that JSON was received
    if request.is_json == False:
        return "Bad Request", 400
    
    # Retrieve Keywords
    keywords = request.json['keywords']

    # Expand keywords
    keywords_expanded = {}
    for keyword in keywords:
        keywords_expanded[keyword] = related_words(keyword, 5)
    
    # Return expanded list of keywords
    return json.jsonify(keywords_expanded)

# Error Handling
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404template.html'), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return render_template('404template.html'), 405