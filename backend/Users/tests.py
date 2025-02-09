from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password

"""
    TODO:
        -   refactor password tests
            Create list of invalid passwords so the same passwords can be applied
            in multiple test classes.
"""

TEST_USER_SIGN_UP_PAYLOAD_1 = {
    "username"      :   "1-username",
    "first_name"          :   "1-test-user-name",
    "last_name"      :   "1-test-user-last_name",
    "email"         :   "1.test@test.com",
    "password_1"    :   "1-Test-Password-1-2",
    "password_2"    :   "1-Test-Password-1-2",
}

TEST_USER_SIGN_UP_PAYLOAD_2 = {
    "username"      :   "2-username",
    "first_name"          :   "2-test-user-name",
    "last_name"      :   "2-test-user-last_name",
    "email"         :   "2.test@test.com",
    "password_1"    :   "2-Test-Password-1-2",
    "password_2"    :   "2-Test-Password-1-2",
}

LIST_OF_INVALID_PASSWORDS = [
    "UUll##Ul",         #   no numbers
    "UUllUl12",         #   no special characters
    "llll##12",         #   no upper case   
    "UUUU##12",         #   no lower case
]

SIGN_UP_URL = reverse('signup')
CHANGE_PASSWORD_URL = reverse('change_password')

class SignUpViewTestCase(TestCase):

    def test_new_user(self):
        response = self.client.post(
            SIGN_UP_URL,
            TEST_USER_SIGN_UP_PAYLOAD_1
        )
        self.assertEqual(response.status_code, 201)

    def test_two_users_with_same_name_different_email_and_username(self):
        payload_1 = TEST_USER_SIGN_UP_PAYLOAD_1.copy()
        payload_2 = TEST_USER_SIGN_UP_PAYLOAD_1.copy()                      # 
        payload_2['username'] = TEST_USER_SIGN_UP_PAYLOAD_2['username']
        payload_3 = TEST_USER_SIGN_UP_PAYLOAD_1.copy()
        payload_3['email'] = TEST_USER_SIGN_UP_PAYLOAD_2['email']
        payload_4 = TEST_USER_SIGN_UP_PAYLOAD_1.copy()
        payload_4['username'] = TEST_USER_SIGN_UP_PAYLOAD_2['username']
        payload_4['email'] = TEST_USER_SIGN_UP_PAYLOAD_2['email']
        response_1 = self.client.post(SIGN_UP_URL, payload_1)
        response_2 = self.client.post(SIGN_UP_URL, payload_2)
        response_3 = self.client.post(SIGN_UP_URL, payload_3)
        response_4 = self.client.post(SIGN_UP_URL, payload_4)
        self.assertEqual(response_1.status_code, 201)
        self.assertEqual(response_2.status_code, 400)   # different username
        self.assertEqual(response_3.status_code, 400)   # different email
        self.assertEqual(response_4.status_code, 201)   # different username and email

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
        self.assertEqual(response_2.status_code, 400)   # 400 - bad request

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

        def test_method_without_payload(method):
            response = method(
                SIGN_UP_URL
            )
            self.assertEqual(response.status_code, 405) # 405 - method not allowed
        test_method_without_payload(self.client.get)
        test_method_without_payload(self.client.put)
        test_method_without_payload(self.client.delete)

    def test_post_without_payload(self):
        response = self.client.post(
            SIGN_UP_URL
        )
        self.assertEqual(response.status_code, 400) # 400 - bad request

    def test_passwords(self):
        # same password as user name
        payload_local = TEST_USER_SIGN_UP_PAYLOAD_1.copy()
        payload_local['username'] = payload_local['password_1']
        response = self.client.post(
            SIGN_UP_URL,
            payload_local
        )
        self.assertEqual(response.status_code, 400)

        # password too short - not able to achieve that
        #payload_local = TEST_USER_SIGN_UP_PAYLOAD_1.copy()
        #payload_local['password_1'] = 'UUll##12'
        #payload_local['password_2'] = payload_local['password_1']
        #response = self.client.post(
        #    SIGN_UP_URL,
        #    payload_local
        #)
        #self.assertEqual(response.status_code, 400)

        # no numbers
        payload_local = TEST_USER_SIGN_UP_PAYLOAD_1.copy()
        payload_local['password_1'] = 'UUll##Ul'
        payload_local['password_2'] = payload_local['password_1']
        response = self.client.post(
            SIGN_UP_URL,
            payload_local
        )
        self.assertEqual(response.status_code, 400)

        # no special character
        payload_local = TEST_USER_SIGN_UP_PAYLOAD_1.copy()
        payload_local['password_1'] = 'UUllUl12'
        payload_local['password_2'] = payload_local['password_1']
        response = self.client.post(
            SIGN_UP_URL,
            payload_local
        )
        self.assertEqual(response.status_code, 400)

        # no upper case
        payload_local = TEST_USER_SIGN_UP_PAYLOAD_1.copy()
        payload_local['password_1'] = 'llll##12'
        payload_local['password_2'] = payload_local['password_1']
        response = self.client.post(
            SIGN_UP_URL,
            payload_local
        )
        self.assertEqual(response.status_code, 400)

        # no lower case
        payload_local = TEST_USER_SIGN_UP_PAYLOAD_1.copy()
        payload_local['password_1'] = 'UUUU##12'
        payload_local['password_2'] = payload_local['password_1']
        response = self.client.post(
            SIGN_UP_URL,
            payload_local
        )
        self.assertEqual(response.status_code, 400)


class ChangePasswordViewTestCase(TestCase):

    def setUp(self):
        User.objects.create_user(
            first_name = TEST_USER_SIGN_UP_PAYLOAD_1['first_name'],
            last_name = TEST_USER_SIGN_UP_PAYLOAD_1['last_name'],
            email = TEST_USER_SIGN_UP_PAYLOAD_1['email'],
            password = TEST_USER_SIGN_UP_PAYLOAD_1['password_1'],
            username = TEST_USER_SIGN_UP_PAYLOAD_1['username']
        )
        User.objects.create_user(
            first_name = TEST_USER_SIGN_UP_PAYLOAD_2['first_name'],
            last_name = TEST_USER_SIGN_UP_PAYLOAD_2['last_name'],
            email = TEST_USER_SIGN_UP_PAYLOAD_2['email'],
            password = TEST_USER_SIGN_UP_PAYLOAD_2['password_1'],
            username = TEST_USER_SIGN_UP_PAYLOAD_2['username']
        )

    def get_authentication_token(self, username, password):
        response = self.client.post(
            reverse('token_obtain_pair'),
            {
                'username'      :   username,
                'password'      :   password
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue('access' in response.data)
        return response.data['access']


    def test_update_with_valid_password(self):
        token = self.get_authentication_token(
            username = TEST_USER_SIGN_UP_PAYLOAD_1['username'],
            password = TEST_USER_SIGN_UP_PAYLOAD_1['password_1']
        )

        new_password = 'TEst##33'
        response = self.client.post(
            CHANGE_PASSWORD_URL,
            {
                'username'  :   TEST_USER_SIGN_UP_PAYLOAD_1['username'],
                'old_password'  :   TEST_USER_SIGN_UP_PAYLOAD_1['password_1'],
                'new_password_1'    :   new_password,
                'new_password_2'    :   new_password,
            },
            HTTP_AUTHORIZATION=f'Bearer {token}' 
        )
        self.assertEqual(response.status_code, 202) # 202   -   accepted

        # check whether password has been really updated
        new_token = self.get_authentication_token(
            username = TEST_USER_SIGN_UP_PAYLOAD_1['username'],
            password = new_password
        )

    def test_update_with_invalid_password(self):
        token = self.get_authentication_token(
            username = TEST_USER_SIGN_UP_PAYLOAD_1['username'],
            password = TEST_USER_SIGN_UP_PAYLOAD_1['password_1']
        )

        def test(new_invalid_password):
            response = self.client.post(
                CHANGE_PASSWORD_URL,
                {
                    'username'  :   TEST_USER_SIGN_UP_PAYLOAD_1['username'],
                    'old_password'  :   TEST_USER_SIGN_UP_PAYLOAD_1['password_1'],
                    'new_password_1'    :   new_invalid_password,
                    'new_password_2'    :   new_invalid_password,
                },
                HTTP_AUTHORIZATION=f'Bearer {token}' 
            )
            self.assertEqual(response.status_code, 400) # 400   -   bad request
        for p in LIST_OF_INVALID_PASSWORDS:
            test(p)

        # check that stored password is still equal to original password
        user = User.objects.get(username=TEST_USER_SIGN_UP_PAYLOAD_1['username'])
        self.assertTrue(check_password(TEST_USER_SIGN_UP_PAYLOAD_1['password_1'], user.password))

    def test_update_password_without_authentication(self):
        new_password = 'TEst##33'
        response = self.client.post(
            CHANGE_PASSWORD_URL,
            {
                'username'  :   TEST_USER_SIGN_UP_PAYLOAD_1['username'],
                'old_password'  :   TEST_USER_SIGN_UP_PAYLOAD_1['password_1'],
                'new_password_1'    :   new_password,
                'new_password_2'    :   new_password,
            }
        )
        self.assertEqual(response.status_code, 401) # 401 - unauthorization access

        # check that stored password is still equal to original password
        user = User.objects.get(username=TEST_USER_SIGN_UP_PAYLOAD_1['username'])
        self.assertTrue(check_password(TEST_USER_SIGN_UP_PAYLOAD_1['password_1'], user.password))


    def test_missing_fields_in_request(self):
        VALID_PAYLOAD = {
            'username'  :   TEST_USER_SIGN_UP_PAYLOAD_1['username'],
            'old_password'  :   TEST_USER_SIGN_UP_PAYLOAD_1['password_1'],
            'new_password_1'    :   'TEst##33',
            'new_password_2'    :   'TEst##33',
        }
        def test(field_to_exclude):
            token = self.get_authentication_token(
                username = TEST_USER_SIGN_UP_PAYLOAD_1['username'],
                password = TEST_USER_SIGN_UP_PAYLOAD_1['password_1']
            )
            payload_copy = VALID_PAYLOAD.copy()
            payload_copy.pop(field_to_exclude)
            response = self.client.post(
                CHANGE_PASSWORD_URL,
                payload_copy,
                HTTP_AUTHORIZATION=f'Bearer {token}' 
            )
            self.assertEqual(response.status_code, 400) # 400 - bad request
        for f in VALID_PAYLOAD:
            test(f)

    def test_invalid_old_password(self):
        token = self.get_authentication_token(
            username = TEST_USER_SIGN_UP_PAYLOAD_1['username'],
            password = TEST_USER_SIGN_UP_PAYLOAD_1['password_1']
        )
        new_password = 'TEst##33'
        response = self.client.post(
            CHANGE_PASSWORD_URL,
            {
                'username'  :   TEST_USER_SIGN_UP_PAYLOAD_1['username'],
                'old_password'  :   TEST_USER_SIGN_UP_PAYLOAD_1['password_1'] + '123',
                'new_password_1'    :   new_password,
                'new_password_2'    :   new_password,
            },
            HTTP_AUTHORIZATION = f'Bearer {token}'
        )
        self.assertEqual(response.status_code, 400) # 400 - bad request

        # check that stored password is still equal to original password
        user = User.objects.get(username=TEST_USER_SIGN_UP_PAYLOAD_1['username'])
        self.assertTrue(check_password(TEST_USER_SIGN_UP_PAYLOAD_1['password_1'], user.password))


    def test_invalid_authorization_token(self):
        invalid_token = self.get_authentication_token(
            username = TEST_USER_SIGN_UP_PAYLOAD_2['username'],
            password = TEST_USER_SIGN_UP_PAYLOAD_2['password_1']
        )
        new_password = 'TEst##33'
        response = self.client.post(
            CHANGE_PASSWORD_URL,
            {
                'username'  :   TEST_USER_SIGN_UP_PAYLOAD_1['username'],
                'old_password'  :   TEST_USER_SIGN_UP_PAYLOAD_1['password_1'],
                'new_password_1'    :   new_password,
                'new_password_2'    :   new_password,
            },
            HTTP_AUTHORIZATION = f'Bearer {invalid_token}'
        )
        self.assertEqual(response.status_code, 400) # 401 - bad request

        # check that stored password is still equal to original password
        user = User.objects.get(username=TEST_USER_SIGN_UP_PAYLOAD_1['username'])
        self.assertTrue(check_password(TEST_USER_SIGN_UP_PAYLOAD_1['password_1'], user.password))
