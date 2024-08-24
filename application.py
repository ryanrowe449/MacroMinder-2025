from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO
#import os

#have to se the FLASK_APP environment variable
#os.environ['FLASK_APP'] = 'application.py'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
# ALWAYS REPLACE THIS LINE WITH YOUR LOCAL DATABASE PATH - Ori
# For example: mysql://username:password@localhost/TableName
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:monkeyinhospital@localhost/users'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
socketio = SocketIO(app)

#import the routes after the app & db is initialized and before the app runs (need routes to be initialized)
import routes

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    #app.debug = True
    app.run(debug=True)