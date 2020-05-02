from flask import Flask, request, render_template as render, jsonify

pirate = Flask('Pirate Code')

from pirate_code.database import pirate_db
@pirate.route('/', methods = ['GET'])
def index():
    return 'Hello World'

@pirate.route('/editor', methods = ['GET'])
def editor():
    return render(
        'editor.html'
    )
