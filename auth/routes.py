from flask import  Blueprint



auth = Blueprint("auth", __name__)

@auth.route("/getdata")
def getdata():
   return {"message":"authentification"}




# Route
