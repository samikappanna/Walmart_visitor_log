from flask import Flask
from flask_cors import CORS 
from db import db
from visitor_log import visitor_blueprint
from dashboard import dashboard_blueprint

app=Flask(__name__)
CORS(app)


#database Configurations
username="root"
password=""
userpass='mysql+pymysql://'+username+':'+password+'@'
server='127.0.0.1'
dbname='/walmat_visitors'


app.config['SQLALCHEMY_DATABASE_URI'] = userpass+server+dbname
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db.init_app(app)
#register blueprint
app.register_blueprint(visitor_blueprint)
app.register_blueprint(dashboard_blueprint)
# API-End point -Route
@app.route('/')
def serverStatus():
    return "Server is up and running"

if __name__=='__main__':
    app.debug=True
    app.run()
# server response code 200:success
#server response code 404:not found
#300:reconnect
#500:app crash