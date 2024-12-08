# app.py
from flask import Flask
from flask_cors import CORS
from config import Config
from routes.user_posts import user_posts_bp
from routes.auth import auth_bp
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# CORS 설정
app.config.from_object(Config)
CORS(app, resources={r"/*": {"origins": Config.CORS_ORIGINS}})
jwt = JWTManager(app)

# SECRET_KEY 설정
app.config['SECRET_KEY'] = 'your_secret_key_here'

# bp 등록
app.register_blueprint(user_posts_bp)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
