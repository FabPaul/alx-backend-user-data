#!/usr/bin/env python3
"""
Main file
"""

import requests
import json


BASE_URL = 'http://127.0.0.1:5000'


def register_user(email: str, password: str) -> None:
    """Register new user"""
    data = {"email": email, "password": password}
    response = requests.post(f'{BASE_URL}/users', data=data)
    assert response.status_code == 200
    assert response.json()["message"] == "user created"


def log_in_wrong_password(email: str, password: str) -> None:
    """Login with wrong password"""
    response = requests.post(f'{BASE_URL}/sessions',
                             data={"email": email, "password": password})
    assert response.status_code == 401

    try:
        response_data = response.json()
        assert response_data["message"] == "Invalid email/password"
    except json.JSONDecodeError:
        # Handle JSON decoding error
        print("Error: Invalid JSON response from server")
    except KeyError:
        # Handle missing "message" key in response
        print("Error: Unexpected response from server")


def log_in(email: str, password: str) -> str:
    """Login """
    data = {"email": email, "password": password}
    response = requests.post(f'{BASE_URL}/sessions', data=data)
    try:
        response_json = response.json()
        assert response.status_code == 200
        assert "session_id" in response_json
        return response_json["session_id"]
    except json.JSONDecodeError:
        raise
    except AssertionError:
        raise


def profile_unlogged() -> None:
    """Profile unlogged"""
    response = requests.get(f'{BASE_URL}/profile')
    try:
        assert response.status_code == 403
    except AssertionError:
        raise


def profile_logged(session_id: str) -> None:
    """Profile logged"""
    headers = {"session_id": session_id}
    response = requests.get(f'{BASE_URL}profile', headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == EMAIL


def log_out(session_id: str) -> None:
    """Log out"""
    headers = {"session_id": session_id}
    response = requests.delete(f'{BASE_URL}/sessions', headers=headers)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """Reset password token"""
    data = {"email": email}
    response = requests.post(f'{BASE_URL}/reset_password', data=data)
    assert response.status_code == 200
    assert "reset_token" in response.json()
    return response.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update password"""
    data = {"email": email, "reset_token": reset_token,
            "new_password": new_password}
    response = requests.put(f'{BASE_URL}/reset_password', data=data)
    assert response.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
