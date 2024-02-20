#!/usr/bin/env python3
"""Flask module"""

from flask import Flask, jsonify, request, abort, make_response
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'])
def home():
    """Basic flask app"""
    return jsonify({'message': 'Bienvenue'})


@app.route("/users", methods=['POST'])
def users():
    """Users function for the users route"""
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        new_user = AUTH.register_user(email, password)
        return jsonify({"email": new_user.email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"})


@app.route("/sessions", methods=['POST'])
def login():
    """Login function for sessions route"""
    email = request.form.get('email')
    password = request.form.get('password')
    user = AUTH.valid_login(email, password)
    try:
        if not user:
            abort(401)
        else:
            session_id = AUTH.create_session(email)
            response = make_response({"email": email, "message": "logged in"})
            response.set_cookie("session_id", session_id)
        return response
    except Exception:
        raise NoResultFound        


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
