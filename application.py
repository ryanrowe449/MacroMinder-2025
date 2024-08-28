from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
#mysql://username:password@localhost/TableName
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ryanrowe:monkeyinhospital@rds-macro-minder-db.cj4wu2og693k.us-east-1.rds.amazonaws.com/macrominder'
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