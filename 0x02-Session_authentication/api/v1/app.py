#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = getenv('AUTH_TYPE')
if auth == 'basic_auth':
    auth = BasicAuth()
elif auth == 'session_auth':
    auth = SessionAuth()
else:
    auth = Auth()


@app.before_request
def preauth() -> None:
    """
        This runs before each request and determines
        if the request needs authentication
    """
    if not auth:
        return
    request.current_user = auth.current_user(request)
    noauth = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/',
            '/api/v1/auth_session/login/'
        ]
    if not auth.require_auth(request.path, noauth):
        return
    if auth.authorization_header(request) is None and\
            auth.session_cookie(request) is None:
        abort(401)
    if auth.current_user(request) is None:
        abort(403)


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler for the flask api """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def noaccess(error) -> str:
    """ No  access to resource for the flask api """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler for the app routes
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
