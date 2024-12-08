from flask import Blueprint, request, jsonify
from services.auth import signup, login

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def handle_signup():
    return signup()

@auth_bp.route('/login', methods=['POST'])
def handle_login():
    return login()
