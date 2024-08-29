from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO

application = Flask(__name__)
application.config['SECRET_KEY'] = 'your_secret_key'
#mysql://username:password@localhost/TableName
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ryanrowe:monkeyinhospital@rds-macro-minder-db.cj4wu2og693k.us-east-1.rds.amazonaws.com/macrominder'


db = SQLAlchemy(application)
bcrypt = Bcrypt(application)
socketio = SocketIO(application)

#import the routes after the app & db is initialized and before the app runs (need routes to be initialized)
import routes

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    #app.debug = True
    application.run(debug=True)