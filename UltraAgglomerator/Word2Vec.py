from flask import Flask, abort, session, redirect, url_for, request, render_template, json
from markupsafe import escape 

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

    # TODO: Expand keywords
    keywords_expanded = {}
    for keyword in keywords:
        keywords_related = {keyword}
        for x in range(5):
            keywords_related.add(x) # TODO: Call a "get related" function
        keywords_expanded[keyword] = keywords_related

    # Return expanded list of keywords
    return json.jsonify(keywords_expanded)

# Error Handling
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404template.html'), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return render_template('404template.html'), 405