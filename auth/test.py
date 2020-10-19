@app.route('/api/v1/users/<id>')
def show_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        return jsonify(user.serialize)
    except:
        return not_found("User does not exist")


@app.route('/api/v1/users', methods=['POST'])
def create_user():
    if not request.is_json or 'name' not in request.get_json():
        return bad_request('Missing required data.')
    user = User(request.get_json()['name'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'user': user.serialize}), 201


#register route  ---------------------------------------------------------------------
@app.route('/json-reg', methods=['POST']) #GET requests will be blocked
def json_reg():
 if request.method == 'POST':
    req_data = request.get_json()      # remember to validate data
    return register.main_route(req_data, bcrypt, db, mail)
    
   
@app.route('/update-reg', methods=['POST'])
def update_reg():
 if request.method == 'POST':
  req_data = request.get_json()      # remember to validate data 
  return register.reg_conf(req_data, db)

@app.route('/json-login', methods=['POST'])
def json_login():
    if request.method == 'POST':
      req_data = request.get_json() 
      return login.main_route(req_data, bcrypt, db); 



#     @api.route('/')
# def show_user():
#  return {"message": "Hello, World!"}
#     try:
#        user = User.query.filter_by(id=id).first()
#        return jsonify(user.serialize)
#     except:
#        return not_found("User does not exist")


CREATE TABLE chatevent (
	chatevent_id serial PRIMARY KEY,
	date  date NOT NULL,
	event VARCHAR ( 250 ) NOT NULL,
	usersid int  NOT NULL,
	chatroomid int NOT NULL
        
);
CREATE TABLE chatroom (
	chatroom_id serial PRIMARY KEY,
	roomcode  VARCHAR ( 250 ) UNIQUE NOT NULL,
	admin VARCHAR ( 250 ) NOT NULL
);
CREATE TABLE messages (
	messages_id serial PRIMARY KEY,
	content  VARCHAR ( 2500 ) UNIQUE NOT NULL,
	sender VARCHAR ( 250 ) NOT NULL,
    datemsg  date NOT NULL,
    chatroomid int NOT NULL
);
@app.route("/socket.io/", methods=["GET"])
#@cross_origin()
def get_cors():
    """GET in server"""
    response = jsonify(message="Simple server is running")
    # Enable Access-Control-Allow-Origin
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/socket.io/", methods=["POST"])
#@cross_origin()
def post_cors():
    """POST in server"""
    return jsonify(message="POST request returned")


@property
    def serialize(self):
        return{
           'id':self.id,
           'username':self.username, 
           'password':self.password,
           'email':self.email,
           'firstname':self.firstname,
           'lastname':self.lastname,
           'phonenumber':self.phonenumber,
           'token':self.token,
        }