#!/usr/bin/env python3
""" A flask app running the user session """
from flask import Flask, jsonify, request
from auth import Auth



app = Flask(__name__)
AUTH = Auth()


@app.route('/', strict_slashes=False)
def index() -> str:
    """ the base index route for api """
    return jsonify({'message': 'Bienvenue'})

@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user() -> str:
    """ end point to register a user """
    email = request.get('email')
    password = request.get('password')

    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": f"{email}", "message": "user created"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
