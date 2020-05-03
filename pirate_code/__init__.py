from flask import Flask, request, render_template as render, jsonify

pirate = Flask('Pirate Code')

from pirate.database import pirate_db, hash
@pirate.route('/', methods = ['GET'])
def index():
    return 'Hello World'

@pirate.route('/sign-up', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render('register.html')

    data = request.json
    usernames = list(pirate_db.db.user.find({'username': data['username']}))
    emails = list(pirate_db.db.user.find({'email': data['email']}))

    if emails == [] and usernames == []:
        data['password'] = hash(data['password'])

        user_id = pirate_db.db.user.insert_one(data).inserted_id
        if 'json' in request.mimetype:
            return jsonify({ 'success': True })
    else:
        if 'json' in request.mimetype:
            return jsonify({ 'success': False }), 500
        return render('register.html', warning = 'Your email or username did registered!'), 500


@pirate.route('/editor', methods = ['GET'])
def editor():
    return render('editor.html')
