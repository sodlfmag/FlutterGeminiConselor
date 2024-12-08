import unittest
from flask import Flask
from user_posts_service import handle_add_post, handle_delete_post, handle_edit_post, handle_get_post, handle_get_user_data
from unittest.mock import MagicMock

class TestUserPostsService(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """테스트 클래스가 실행되기 전에 한 번만 호출되어 Flask 앱을 설정합니다."""
        cls.app = Flask(__name__)

    def setUp(self):
        """각 테스트 메소드 실행 전에 호출됩니다."""
        self.client = self.app.test_client()

    def test_handle_add_post(self):
        """handle_add_post 함수 테스트"""
        request_mock = MagicMock()  # 요청 객체에 대한 Mock 객체 생성
        with self.app.app_context():  # 애플리케이션 컨텍스트 설정
            response = handle_add_post('test_uid', request_mock)
            # 튜플로 반환되므로, 두 번째 값(status_code)을 체크합니다.
            self.assertEqual(response[1], 200)

    def test_handle_delete_post(self):
        """handle_delete_post 함수 테스트"""
        with self.app.app_context():  # 애플리케이션 컨텍스트 설정
            response = handle_delete_post('test_uid', '0')
            # 튜플로 반환되므로, 두 번째 값(status_code)을 체크합니다.
            self.assertEqual(response[1], 200)

    def test_handle_edit_post(self):
        """handle_edit_post 함수 테스트"""
        request_mock = MagicMock()  # 요청 객체에 대한 Mock 객체 생성
        with self.app.app_context():  # 애플리케이션 컨텍스트 설정
            response = handle_edit_post('test_uid', '0', request_mock)
            # 튜플로 반환되므로, 두 번째 값(status_code)을 체크합니다.
            self.assertEqual(response[1], 200)

    def test_handle_get_post(self):
        """handle_get_post 함수 테스트"""
        request_mock = MagicMock()  # 요청 객체에 대한 Mock 객체 생성
        with self.app.app_context():  # 애플리케이션 컨텍스트 설정
            response = handle_get_post(request_mock)
            # 튜플로 반환되므로, 두 번째 값(status_code)을 체크합니다.
            self.assertEqual(response[1], 200)

    def test_handle_get_user_data(self):
        """handle_get_user_data 함수 테스트"""
        with self.app.app_context():  # 애플리케이션 컨텍스트 설정
            response = handle_get_user_data('test_uid')
            # 튜플로 반환되므로, 두 번째 값(status_code)을 체크합니다.
            self.assertEqual(response[1], 200)

if __name__ == '__main__':
    unittest.main()
