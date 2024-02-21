#!/usr/bin/env python3
"""Flask module"""

from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth


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
    if not user:
        abort(401)
    else:
        session_id = AUTH.create_session(email)
        response = make_response({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=['DELETE'])
def logout():
    """Logout function for the sessions route"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=['GET'])
def profile():
    """Profile function for the profile route"""
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email}), 200
    abort(403)


@app.route("/reset_password", methods=['POST'])
def get_reset_password_token():
    """Reset password function"""
    email = request.form.get('email')
    if not email:
        return abort(403)
    else:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
