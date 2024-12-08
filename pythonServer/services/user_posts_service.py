import datetime
from flask import jsonify
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

# Firebase Admin SDK 초기화
try:
    # Firebase Admin SDK 초기화, 앱이 이미 초기화된 경우 오류가 발생하지 않도록 처리
    cred = credentials.Certificate("geminicounselorapp-firebase-adminsdk-r67fn-5d088200f2.json")
    firebase_admin.initialize_app(cred)
except ValueError:
    # 이미 Firebase가 초기화된 경우 추가 초기화하지 않음
    pass
db = firestore.client()

def handle_get_user_data(uid):
    try:
        user_ref = db.collection('users').document(uid)
        user_doc = user_ref.get()

        if user_doc.exists:
            user_data = user_doc.to_dict()
            return jsonify(user_data), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def handle_get_post(request):
    uid = request.args.get('uid')
    post_id = request.args.get('postId')

    if not uid or not post_id:
        return jsonify({"error": "Missing uid or postId"}), 400

    try:
        post_id = int(post_id)
        user_ref = db.collection('users').document(uid)
        user_data = user_ref.get()

        if not user_data.exists:
            return jsonify({"error": "User not found"}), 404

        conversation_history = user_data.to_dict().get('conversationHistory', [])
        post = None

        if 0 <= post_id < len(conversation_history):
            post = conversation_history[post_id]

        if post is None:
            return jsonify({"error": "Post not found"}), 404

        return jsonify(post), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def handle_add_post(uid, request):
    try:
        data = request.json
        if not data or 'title' not in data or 'content' not in data:
            return jsonify({"error": "Invalid request. 'title' and 'content' are required"}), 400

        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        user_ref = db.collection('users').document(uid)
        user_doc = user_ref.get()

        conversation_history = []
        if user_doc.exists:
            conversation_history = user_doc.to_dict().get('conversationHistory', [])

        post_id = str(len(conversation_history))

        new_post = {
            "postId": post_id,
            "date": current_date,
            "title": data['title'],
            "content": data['content']
        }

        conversation_history.append(new_post)
        user_ref.set({"conversationHistory": conversation_history}, merge=True)

        return jsonify({"message": "Post added successfully.", "data": new_post}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def handle_delete_post(uid, post_id):
    try:
        user_ref = db.collection('users').document(uid)
        user_doc = user_ref.get()

        if not user_doc.exists:
            return jsonify({"error": "User not found"}), 404

        conversation_history = user_doc.to_dict().get('conversationHistory', [])
        post_id = int(post_id)

        if 0 <= post_id < len(conversation_history):
            deleted_post = conversation_history.pop(post_id)
            user_ref.set({"conversationHistory": conversation_history}, merge=True)

            return jsonify({"message": "Post deleted successfully", "deleted_post": deleted_post}), 200
        else:
            return jsonify({"error": "Post not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def handle_edit_post(uid, post_id, request):
    try:
        data = request.json
        if not data or 'title' not in data or 'content' not in data:
            return jsonify({"error": "Invalid request. 'title' and 'content' are required"}), 400

        user_ref = db.collection('users').document(uid)
        user_doc = user_ref.get()

        if not user_doc.exists:
            return jsonify({"error": "User not found"}), 404

        conversation_history = user_doc.to_dict().get('conversationHistory', [])
        post_id = int(post_id)

        if 0 <= post_id < len(conversation_history):
            post = conversation_history[post_id]

            post['title'] = data['title']
            post['content'] = data['content']
            post['date'] = datetime.datetime.now().strftime("%Y-%m-%d")

            user_ref.set({"conversationHistory": conversation_history}, merge=True)

            return jsonify({"message": "Post updated successfully", "data": post}), 200
        else:
            return jsonify({"error": "Post not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
