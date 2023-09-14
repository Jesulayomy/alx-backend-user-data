#!/usr/bin/env python3
""" A flask app running the user session """
from flask import (
    Flask,
    abort,
    jsonify,
    make_response,
    request,
    redirect,
    url_for,
)
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """ the base index route for api """
    return jsonify({'message': 'Bienvenue'})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """ end point to register a user """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
        Create a new session for the user, store it the session ID as a
        cookie with key "session_id" on the response and return a
        JSON payload of the form
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = make_response(jsonify(
        {"email": email, "message": "logged in"}))
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """ logs out the user and deletes the session """
    session_id = request.cookies.get('session_id')

    try:
        user = AUTH.get_user_from_session_id(session_id)
    except Exception:
        abort(403)

    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """ Returns the user's profile as a dict of email """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({'email': user.email})
    abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """ Returns a json payload and the http status """

    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({'email': email, 'reset_token': token}), 200
    except ValueError:
        abort(403)
    abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """ Updates the password with a new one """
    email = request.form.get('email')
    password = request.form.get('password')
    reset_token = request.form.get('new_password')

    try:
        AUTH.update_password(reset_token, password)
        return jsonify({'email': email, 'message': 'Password updated'})
    except ValueError:
        abort(403)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
