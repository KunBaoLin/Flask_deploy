from flask_app import app
from flask_app.controllers import users, bands
import os

if __name__=="__main__":
    print(os.environ.get("test"))
    app.run(debug=True)