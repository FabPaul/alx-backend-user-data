#!/usr/bin/env python3
"""New flask view module to handle session Auth"""


from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth():
    """Session auth route"""
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400
    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400

    user = User.search({"email": email})

    if not user or user == []:
        return jsonify({"error": "no user found for this email"}), 404
    for u in user:
        if u.is_valid_password(password):

            from api.v1.app import auth
            session_id = auth.create_session(u.id)
            response = jsonify(u.to_json())
            session_cookie_name = getenv("SESSION_NAME")
            response.set_cookie(session_cookie_name, session_id)
            return response

    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def session_logout():
    """Logout/delete auth route"""
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
