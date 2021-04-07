from flask import Flask, abort, session, redirect, url_for, request, render_template
from markupsafe import escape 

# ????
app = Flask(__name__)
app.secret_key = b'\xe1q\xf5\xd4\xa3=\xa8\xc0\x18\xf9\xb3G`\xe0"\xa2'

# Main Page
@app.route('/')
def index():
    print(request.content_length)
    button_logout = '''<form method="post" action="/logout"> <p><input type=submit value=Logout> </form>'''
    if 'username' == '':
        return 'Logged in as Guest' + button_logout 
    elif 'username' in session:
        x = 'Logged in as %s' % escape(session['username'])
        return x + button_logout
    return 'You are not logged in' + '''<form method="get" action="/login"> <p><input type=submit value=Login> </form>'''
# Require USERNAME
# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    print(request.content_length)
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''
# Logout "Page"
@app.route('/logout', methods=['POST'])
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

# Error Handling
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404template.html'), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return render_template('404template.html'), 405

