#!/usr/bin/env python3
"""Flask module"""

from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
