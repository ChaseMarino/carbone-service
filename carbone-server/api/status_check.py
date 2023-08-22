from flask import make_response
from flask_restful import Resource, request, reqparse


class StatusCheck(Resource):
    def get(self):
        s = "<h1>Welcome to my Carbon Server Service server!</h1>"
        return  make_response(s, 200)
