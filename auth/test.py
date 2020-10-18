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





#     @api.route('/')
# def show_user():
#  return {"message": "Hello, World!"}
#     try:
#        user = User.query.filter_by(id=id).first()
#        return jsonify(user.serialize)
#     except:
#        return not_found("User does not exist")