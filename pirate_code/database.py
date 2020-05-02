from flask_pymongo import PyMongo
from pirate_code import pirate

pirate.config["MONGO_URI"] = "mongodb://localhost:27017/PirateCode"
pirate_db = PyMongo(pirate)
