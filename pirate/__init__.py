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


@pirate.route('/logout', methods = ['GET', 'POST'])
def logout():
    try:
        session.pop("pirate_user")
        session.pop("pirate_pass")
    except:pass
    return redirect('/sign-in')

@pirate.route('/sign-in', methods = ['GET', 'POST'])
def login():
    return redirect('/sign-up')

@pirate.route('/sign-up', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        try:
            return redirect(f'/{session["pirate_user"]}')
        except KeyError:
            try:
                return render('register.html',
                              warning = session["pirate_warning"])
            except KeyError:return render('register.html',
                                          warning = None)

    data = request.form.to_dict()
    if 'json' in request.mimetype:
        data = request.json
    print(data)

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
            return redirect(f'/{session["pirate_user"]}')
    else:
        if 'json' in request.mimetype:
            return jsonify({ 'success': False }), 500
        session["pirate_warning"] = 'Your email or username already exists!'
        return render('register.html', warning = 'Your email or username already exists!'), 500


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
