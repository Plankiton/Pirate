from pirate.session import pirate_session as session
from flask import (Flask,
                   request,
                   jsonify,
                   redirect,
                   render_template as render)

pirate = Flask('Pirate Society')
pirate.config['SECRET_KEY'] = 'generic_secret_key'

from pirate.database import pirate_db, hash
@pirate.route('/', methods = ['GET'])
def index():
    return 'Hello World'


@pirate.route('/sign-up', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        try:
            return redirect(f'/{session["pirate_user"]}')
        except KeyError: return render('register.html')

    data = request.json
    usernames = list(pirate_db.db.user.find({'username': data['username']}))
    emails = list(pirate_db.db.user.find({'email': data['email']}))

    if emails == [] and usernames == []:
        data['password'] = hash(data['password'])

        session['pirate_user'] = data['username']
        session['pirate_pass'] = data['password']

        user_id = pirate_db.db.user.insert_one(data).inserted_id
        if 'json' in request.mimetype:
            return jsonify({ 'success': True })
    else:
        if 'json' in request.mimetype:
            return jsonify({ 'success': False }), 500
        return render('register.html', warning = 'Your email or username did registered!'), 500


@pirate.route('/<username>', methods = ['GET'])
def user(username):
    user = pirate_db.db.user.find_one({'username': username})
    if 'json' in request.mimetype:
        return jsonify(user)
    if user:
        return render('profile.html', data=user)
    return '<h1>User not found!</h1>', 404


@pirate.route('/editor', methods = ['GET'])
def editor():
    return render('editor.html')
