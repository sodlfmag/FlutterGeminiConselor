from flask import Blueprint, request, jsonify
from services.user_posts_service import (
    handle_get_user_data,
    handle_get_post,
    handle_add_post,
    handle_delete_post,
    handle_edit_post
)

user_posts_bp = Blueprint('user_posts', __name__)

# UID를 통해 사용자 데이터 가져오기
@user_posts_bp.route('/get_user_data/<uid>', methods=['GET'])
def get_user_data(uid):
    return handle_get_user_data(uid)

# 특정 글 조회하기
@user_posts_bp.route('/get_post', methods=['GET'])
def get_post():
    return handle_get_post(request)

# 글 등록하기
@user_posts_bp.route('/add_post/<uid>', methods=['POST'])
def add_post(uid):
    return handle_add_post(uid, request)

# 글 삭제하기
@user_posts_bp.route('/delete_post/<uid>/<post_id>', methods=['DELETE'])
def delete_post(uid, post_id):
    return handle_delete_post(uid, post_id)

# 글 수정하기
@user_posts_bp.route('/edit_post/<uid>/<post_id>', methods=['PUT'])
def edit_post(uid, post_id):
    return handle_edit_post(uid, post_id, request)
