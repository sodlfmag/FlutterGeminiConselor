import firebase_admin
from firebase_admin import credentials, auth
from flask import request, jsonify

# Firebase Admin SDK 초기화
try:
    # Firebase Admin SDK 초기화, 앱이 이미 초기화된 경우 오류가 발생하지 않도록 처리
    cred = credentials.Certificate("geminicounselorapp-firebase-adminsdk-r67fn-5d088200f2.json")
    firebase_admin.initialize_app(cred)
except ValueError:
    # 이미 Firebase가 초기화된 경우 추가 초기화하지 않음
    pass

# 회원가입 API
def signup():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    try:
        # Firebase Authentication을 사용하여 회원가입 처리
        user = auth.create_user(
            name=name,
            email=email,
            password=password
        )
        return jsonify({"message": "User created successfully", "uid": user.uid}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# 로그인 API
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    try:
        id_token = data.get('idToken')  # 클라이언트에서 Firebase ID 토큰을 받아옴
        
        if id_token is None:
            return jsonify({"error": "ID Token is required"}), 400
        
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']  # 사용자의 UID를 가져옴
        
        return jsonify({"message": "Login successful", "uid": uid}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401
