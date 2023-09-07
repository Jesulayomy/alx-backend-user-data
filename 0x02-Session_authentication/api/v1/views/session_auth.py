#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.user import User
from os import getenv


@app_views.route(
    '/auth_session/login',
    methods=['POST'],
    strict_slashes=False)
def auth_login() -> str:
    """ provides the login feaure for the authenticated sessions """
    email = request.form.get('email')
    if email is None or email == '':
        return jsonify({'error': 'email missing'}), 400
    password = request.form.get('password')
    if password is None or password == '':
        return jsonify({'error': 'password missing'}), 400
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({'error': 'no user found for this email'}), 404

    if users is None:
        return jsonify({'error': 'no user found for this email'}), 404

    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            session_name = getenv('SESSION_NAME')
            response = jsonify(user.to_json())
            response.set_cookie(session_name, session_id)
            return response

    return jsonify({'error': 'wrong password'}), 401


@app_views.route(
        '/auth_session/logout',
        methods=['DELETE'],
        strict_slashes=False)
def auth_logout() -> str:
    """ logs out the authenticated user from the session """
    from api.v1.app import auth

    if auth.destroy_session(request):
        return jsonify({}), 200
    return False, abort(404)
