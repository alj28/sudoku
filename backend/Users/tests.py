from django.test import TestCase
from django.urls import reverse

TEST_USER_SIGN_UP_PAYLOAD_1 = {
    "name"          :   "1-test-user-name",
    "password_1"    :   "1-test-password-1-2",
    "password_2"    :   "1-test-password-1-2",
    "lastname"      :   "1-test-user-lastname",
}

TEST_USER_SIGN_UP_PAYLOAD_2 = {
    "name"          :   "2-test-user-name",
    "password_1"    :   "2-test-password-1-2",
    "password_2"    :   "2-test-password-1-2",
    "lastname"      :   "2-test-user-lastname",
}

SIGN_UP_URL = reverse('signup')

class SignUpViewTestCase(TestCase):

    def test_new_user(self):
        response = self.client.post(
            SIGN_UP_URL,
            TEST_USER_SIGN_UP_PAYLOAD_1
        )
        self.assertEqual(response.status_code, 201)

    def test_user_already_exists(self):
        response_1 = self.client.post(
            SIGN_UP_URL,
            TEST_USER_SIGN_UP_PAYLOAD_1
        )
        self.assertEqual(response_1.status_code, 201)
        response_2 = self.client.post(
            SIGN_UP_URL,
            TEST_USER_SIGN_UP_PAYLOAD_1
        )
        self.assertEqual(response_2.status_code, 409)   # 409 - conflict

    def test_password_confirmation(self):
        local_payload = TEST_USER_SIGN_UP_PAYLOAD_1.copy()
        local_payload['password_2'] += "1234"
        response = self.client.post(
            SIGN_UP_URL,
            local_payload
        )
        self.assertEqual(response.status_code, 400)     # 400 - bad request

    def test_missing_payload_fields(self):
        def remove_field_and_send_request(field: str):
            local_payload = TEST_USER_SIGN_UP_PAYLOAD_1.copy()
            local_payload.pop(field)
            response = self.client.post(
                SIGN_UP_URL,
                local_payload
            )
            self.assertEqual(response.status_code, 400) # 400 - bad request
        for f in TEST_USER_SIGN_UP_PAYLOAD_1:
            remove_field_and_send_request(f)

    def test_not_allowed_methods(self):
        def test_method(method):
            response = method(
                SIGN_UP_URL,
                TEST_USER_SIGN_UP_PAYLOAD_1
            )
            self.assertEqual(response.status_code, 405) # 405 - method not allowed
        test_method(self.client.get)
        test_method(self.client.put)
        test_method(self.client.delete)

    def test_post_without_payload(self):
        response = self.client.post(
            SIGN_UP_URL
        )
        self.assertEqual(response.status_code, 400) # 400 - bad request


    



