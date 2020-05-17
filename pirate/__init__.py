from flask import (Flask,
                   request,
                   jsonify,
                   redirect,
                   make_response as mkres,
                   render_template as render)

pirate = Flask('Pirate Society')
pirate.config['SECRET_KEY'] = 'generic_secret_key'

from pirate.database import pirate_db, hash
@pirate.route('/', methods = ['GET'])
def index():
    return 'Hello World'


@pirate.route('/logout', methods = ['GET', 'POST'])
def logout():
    response = redirect('/sign-in')
    response.set_cookie('user', 'null',
                        max_age=0)
    response.set_cookie('pass', 'null',
                        max_age=0)

    return response

@pirate.route('/sign-in', methods = ['GET', 'POST'])
def login():
    response = None
    if request.method == 'GET':
        user = request.cookies.get("user")
        if user:
            response = redirect('/')
        elif request.args.get('error', default=False):
                response = mkres(
                    render('login.html',
                           warning = 'This user not exists')
                )
        else:
            response = mkres(render('login.html', warning = None))
        return response

    data = request.form.to_dict()
    if 'json' in request.mimetype:
        data = request.json

    username = pirate_db.db.user.find_one({'username': data['login']})
    email = pirate_db.db.user.find_one({'email': data['login']})
    user = email if email else username

    data['password'] = hash(data['password'])
    if user and data['password'] == user['password']:
        if 'json' in request.mimetype:
            response = jsonify({ 'success': True })
        else:
            response = redirect('/')

        response.set_cookie('user',
                            user['username'],
                            max_age=60**2*30)
        response.set_cookie('pass',
                            user['password'],
                            max_age=60**2*30)

    else:
        if 'json' in request.mimetype:
            response = jsonify({ 'success': False }), 500

        response = redirect('/sign-in?error=true')

    print(
        dict(zip(request.cookies.keys(),
                 request.cookies.items()))
    )

    return response

@pirate.route('/sign-up', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        warning = 'The username or email alredy exists!!'
        error = request.args.get('error', default=False)
        return render('register.html', warning = warning if error else None)

    data = request.form.to_dict()
    if 'json' in request.mimetype:
        data = request.json

    usernames = list(pirate_db.db.user.find({'username': data['username']}))
    emails = list(pirate_db.db.user.find({'email': data['email']}))

    if emails == [] and usernames == []:
        data['password'] = hash(data['password'])
        user_id = pirate_db.db.user.insert_one(data).inserted_id
        if 'json' in request.mimetype:
            response = jsonify({ 'success': True })
        else:
            response = redirect('/')

        response.set_cookie('user',
                            data['username'],
                            max_age=60**2*30)
        response.set_cookie('pass',
                            data['password'],
                            max_age=60**2*30)

    else:
        if 'json' in request.mimetype:
            response = jsonify({ 'success': False }), 500
        response = render('register.html', warning = 'Your email or username already exists!'), 500

    return response


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
