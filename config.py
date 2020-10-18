import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = "postgresql://mac:lolipop@localhost/jungle"


 query="INSERT INTO users(username, password, email, firstname, lastname, phonenumber, token) VALUES({}, {}, {}, {}, {}, {}, {})".format(username, password, email, firstname, lastname, phonenumber, token)
    db.execute(query)
    db.commit()
