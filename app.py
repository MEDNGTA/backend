from flask import Blueprint, request
from flask_restful import Api, Resource
from resources.User import  User


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(User, '/User')