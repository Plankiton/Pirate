from flask_pymongo import PyMongo
from hashlib import sha512
from pirate import pirate

def hash(string):
    return sha512(bytes(string, 'utf-8')).hexdigest()


pirate.config["MONGO_URI"] = "mongodb://localhost:27017/PirateCode"
pirate_db = PyMongo(pirate)
