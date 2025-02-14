import copy
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from dataclasses import dataclass, fields, asdict
from django.contrib.auth.hashers import check_password

@dataclass
class TestUser:
    username: str
    first_name: str
    last_name: str
    email: str
    password: str
    
    def signup_payload(self) -> dict:
        output = {}
        for k, v in asdict(self).items():
            if 'password' == k:
                output['password_1'] = v
                output['password_2'] = v
                continue
            output[k] = v
        return output
    
    def change_password_payload(self, new_password: str) -> dict:
        output = {}
        for k, v in asdict(self).items():
            if 'password' == k:
                output['old_password'] = v
                continue
            output[k] = v
        output['new_password_1'] = new_password
        output['new_password_2'] = new_password
        return output
    
TEST_USER_1 = TestUser(
    username='test_user_1_username',
    first_name='test_user_1_first_name',
    last_name='test_user_1_last_name',
    email='test_user_1@email.com',
    password='test_user_1_PassWord12#$'
)

TEST_USER_2 = TestUser(
    username='test_user_2_username',
    first_name='test_user_2_first_name',
    last_name='test_user_2_last_name',
    email='test_user_2@email.com',
    password='test_user_2_PassWord12#$'
)

TEST_USER_3 = TestUser(
    username='test_user_3_username',
    first_name='test_user_3_first_name',
    last_name='test_user_3_last_name',
    email='test_user_3@email.com',
    password='test_user_3_PassWord12#$'
)

TEST_USER_4 = TestUser(
    username='test_user_4_username',
    first_name='test_user_4_first_name',
    last_name='test_user_4_last_name',
    email='test_user_4@email.com',
    password='test_user_4_PassWord12#$'
)

SIGN_UP_URL = reverse('signup')
LOGIN_URL = reverse('token_obtain_pair')
CHANGE_PASSWORD_URL = reverse('change_password')

LIST_OF_INVALID_PASSWORDS = [
    "UUll##Ul",         #   no numbers
    "UUllUl12",         #   no special characters
    "llll##12",         #   no upper case   
    "UUUU##12",         #   no lower case
]

class SignUpViewTestCase(TestCase):
    
    def test_new_user(self):
        response = self.client.post(
            SIGN_UP_URL,
            TEST_USER_1.signup_payload()
        )
        self.assertEqual(response.status_code, 201)
        response = self.client.post(
            SIGN_UP_URL,
            TEST_USER_2.signup_payload()
        )
        self.assertEqual(response.status_code, 201)
        
    def test_user_already_exists(self):
        response = self.client.post(
            SIGN_UP_URL,
            TEST_USER_1.signup_payload()
        )
        self.assertEqual(response.status_code, 201)
        response = self.client.post(
            SIGN_UP_URL,
            TEST_USER_1.signup_payload()
        )
        self.assertEqual(response.status_code, 400)
        
    def test_username_or_email_already_exists(self):
        response = self.client.post(
            SIGN_UP_URL,
            TEST_USER_1.signup_payload()
        )
        self.assertEqual(response.status_code, 201)
        
        user_with_same_username = copy.copy(TEST_USER_2)
        user_with_same_username.username = TEST_USER_1.username
        response = self.client.post(
            SIGN_UP_URL,
            user_with_same_username.signup_payload()
        )
        self.assertEqual(response.status_code, 400)
        
        user_with_same_email = copy.copy(TEST_USER_2)
        user_with_same_email.email = TEST_USER_1.email
        response = self.client.post(
            SIGN_UP_URL,
            user_with_same_email.signup_payload()
        )
        self.assertEqual(response.status_code, 400)
        
    def test_firstname_or_lastname_already_exists(self):
        response = self.client.post(
            SIGN_UP_URL,
            TEST_USER_1.signup_payload()
        )
        self.assertEqual(response.status_code, 201)
        
        user_with_same_firstname = copy.copy(TEST_USER_2)
        user_with_same_firstname.first_name = TEST_USER_1.first_name
        response = self.client.post(
            SIGN_UP_URL,
            user_with_same_firstname.signup_payload()
        )
        self.assertEqual(response.status_code, 201)
        
        user_with_same_lastname = copy.copy(TEST_USER_3)
        user_with_same_lastname.last_name = TEST_USER_1.last_name
        response = self.client.post(
            SIGN_UP_URL,
            user_with_same_lastname.signup_payload()
        )
        self.assertEqual(response.status_code, 201)
        
        user_with_same_firstname_and_lastname = copy.copy(TEST_USER_4)
        user_with_same_firstname_and_lastname.first_name = TEST_USER_1.first_name
        user_with_same_firstname_and_lastname.last_name = TEST_USER_1.last_name
        response = self.client.post(
            SIGN_UP_URL,
            user_with_same_firstname_and_lastname.signup_payload()
        )
        self.assertEqual(response.status_code, 201)
        
    def test_password(self):
        def send_signup_request_with_invalid_password(password: str):
            user = copy.copy(TEST_USER_1)
            user.password = password
            response = self.client.post(
                SIGN_UP_URL,
                user.signup_payload()
            )
            self.assertEqual(response.status_code, 400)
            
        # password same as username
        send_signup_request_with_invalid_password(TEST_USER_1.username)
        
        # password same as email
        send_signup_request_with_invalid_password(TEST_USER_1.email)
        
        # no digits
        send_signup_request_with_invalid_password("UUll####")
        
        # no special characters
        send_signup_request_with_invalid_password("UUll1212")
        
        # no upper case characters
        send_signup_request_with_invalid_password("llll##12")
        
        # no lower case characters
        send_signup_request_with_invalid_password("UUUU##12")
        
    def test_password_confirmation(self):
        payload = TEST_USER_1.signup_payload()
        payload['password_2'] += '123'
        response = self.client.post(
            SIGN_UP_URL,
            payload
        )
        self.assertEqual(response.status_code, 400)
        
    def test_all_methods_without_payload(self):
        def send_method_request(method, expected_error_code: int = 405):
            response = method(
                SIGN_UP_URL
            )
            self.assertEqual(response.status_code, expected_error_code)
        send_method_request(self.client.get)
        send_method_request(self.client.post, 400)
        send_method_request(self.client.put)
        send_method_request(self.client.delete)
        
    def test_not_allowed_methods(self):
        def send_method_request(method):
            response = method(
                SIGN_UP_URL,
                TEST_USER_1.signup_payload()
            )
            self.assertEqual(response.status_code, 405)
        send_method_request(self.client.get)
        send_method_request(self.client.put)
        send_method_request(self.client.delete)
        
    def test_missing_payload_fields(self):
        def remove_field_and_send_request(field: str):
            payload = TEST_USER_1.signup_payload()
            payload.pop(field)
            response = self.client.post(
                SIGN_UP_URL,
                payload
            )
            self.assertEqual(response.status_code, 400)
        for k in TEST_USER_1.signup_payload():
            remove_field_and_send_request(k)
            
            
class ChangePasswordViewTestCase(TestCase):
    
    def setUp(self):
        def create_user(user: TestUser):
            response = self.client.post(
                SIGN_UP_URL,
                user.signup_payload()
            )
            self.assertEqual(response.status_code, 201)
        for u in [TEST_USER_1, TEST_USER_2, TEST_USER_3, TEST_USER_4]:
            create_user(u)
            
    def _get_authentication_token(self, username, password):
        response = self.client.post(
            LOGIN_URL,
            {
                'username'  :   username,
                'password'  :   password
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue('access' in response.data)
        return response.data['access']
    
    def test_update_password(self):
        token = self._get_authentication_token(
            TEST_USER_1.username, 
            TEST_USER_1.password
        )
        
        new_password = 'TEst##33'
        response = self.client.post(
            CHANGE_PASSWORD_URL,
            TEST_USER_1.change_password_payload(new_password='TEst##33'),
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        self.assertEqual(response.status_code, 202)
        
        # check whether password has been really updated
        new_token = self._get_authentication_token(
            TEST_USER_1.username, 
            new_password
        )
        
    def test_invalid_new_password(self):
        token = self._get_authentication_token(
            TEST_USER_1.username, 
            TEST_USER_1.password
        )
        
        def test(new_invalid_password: str):
            response = self.client.post(
                CHANGE_PASSWORD_URL,
                TEST_USER_1.change_password_payload(new_invalid_password),
                HTTP_AUTHORIZATION=f'Bearer {token}'
            )
            self.assertEqual(response.status_code, 400)
            
        for p in LIST_OF_INVALID_PASSWORDS:
            test(p)

        # check that stored password is still equal to original password
        user = User.objects.get(username=TEST_USER_1.username)
        self.assertTrue(check_password(TEST_USER_1.password, user.password))
        
    def test_invalid_old_password(self):
        token = self._get_authentication_token(
            TEST_USER_1.username, 
            TEST_USER_1.password
        )
        payload = TEST_USER_1.change_password_payload('TEst##33')
        payload['old_password'] += '123'
        response = self.client.post(
            CHANGE_PASSWORD_URL,
            payload,
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        self.assertEqual(response.status_code, 400)

    def test_update_password_without_authentication(self):
        new_password = 'TEst##33'
        response = self.client.post(
            CHANGE_PASSWORD_URL,
            TEST_USER_1.change_password_payload(new_password)
        )
        self.assertEqual(response.status_code, 401) # 401 - unauthorization access

        # check that stored password is still equal to original password
        user = User.objects.get(username=TEST_USER_1.username)
        self.assertTrue(check_password(TEST_USER_1.password, user.password))
        
    def test_invalid_authorization_token(self):
        invalid_token = self._get_authentication_token(
            TEST_USER_2.username, 
            TEST_USER_2.password
        )
        
        response = self.client.post(
            CHANGE_PASSWORD_URL,
            TEST_USER_1.change_password_payload(new_password='TEst##33'),
            HTTP_AUTHORIZATION=f'Bearer {invalid_token}'
        )
        self.assertEqual(response.status_code, 400)
        
        user = User.objects.get(username=TEST_USER_1.username)
        self.assertTrue(check_password(TEST_USER_1.password, user.password))
        
    def test_missing_payload_fields(self):
        new_password = 'TEst##33'
        def remove_field_and_send_request(field: str):
            payload = TEST_USER_1.change_password_payload(new_password)
            payload.pop(field)
            response = self.client.post(
                SIGN_UP_URL,
                payload
            )
            self.assertEqual(response.status_code, 400)
        for k in TEST_USER_1.change_password_payload(new_password):
            remove_field_and_send_request(k)