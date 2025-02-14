
from dataclasses import dataclass
from django.contrib.auth.models import User
from password_strength import PasswordPolicy
from rest_framework import serializers, status
from django.contrib.auth.hashers import check_password

PASSWORD_CHARFIELD_ARGS = {
    "write_only"    :   True, 
    "style"         :   {
        'input_type': 'password'
    }
}

def is_password_strong(password: str):
    policy = PasswordPolicy.from_names(
        length=8,
        uppercase=2,
        numbers=2,
        special=2,
        nonletters=2
    )
    # PasswordPolicy does not support definition for minimum number of lower-case characters
    n_lower_case = len([c for c in password if c.islower()])
    if 0 != len(policy.test(password)) or n_lower_case < 2:
        return False
    return True

def password_policy_check(password: str):
    if False == is_password_strong(password):
        raise serializers.ValidationError('Password too weak', code=status.HTTP_400_BAD_REQUEST)
    
def add_error_to_dict(key: str, errors_dict: dict, msg: str):
    if key not in errors_dict:
        errors_dict[key] = []
    errors_dict[key].append(msg)
@dataclass
class NewPasswordValidator:
    username: str
    email: str
    password_1: str
    password_2: str
    
    def validate(self, errors_state: dict):
        if self.password_2 != self.password_1:
            add_error_to_dict('password_2', errors_state, 'Passwords do not match')
        if self.username == self.password_1:
            add_error_to_dict('password_1', errors_state, 'Password too weak')
        if self.email == self.password_1:
            add_error_to_dict('password_1', errors_state, 'Password too weak')
        if False == is_password_strong(self.password_1):
            add_error_to_dict('password_1', errors_state, 'Password too weak')
            
@dataclass
class NewUserValidator:
    username: str
    email: str
    
    def validate(self, errors_state):
        if User.objects.filter(email=self.email).exists():
            add_error_to_dict('email', errors_state, 'User already exists.')
        if User.objects.filter(username=self.username).exists():
            add_error_to_dict('username', errors_state, 'User already exists.')

class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password_1 = serializers.CharField(**PASSWORD_CHARFIELD_ARGS)
    password_2 = serializers.CharField(**PASSWORD_CHARFIELD_ARGS)

    def validate(self, data):
        errors = {}
        user_validator = NewUserValidator(
            username=data['username'],
            email=data['email']
        )
        user_validator.validate(errors)
        password_validator = NewPasswordValidator(
            username=data['username'],
            email=data['email'],
            password_1=data['password_1'],
            password_2=data['password_2']
        )
        password_validator.validate(errors)
        if errors:
            raise serializers.ValidationError(errors)
        return data
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(**PASSWORD_CHARFIELD_ARGS)
    new_password_1 = serializers.CharField(**PASSWORD_CHARFIELD_ARGS)
    new_password_2 = serializers.CharField(**PASSWORD_CHARFIELD_ARGS)
    
    def __get_user_object(self, data):
        try:
            authenticated_user = self.context.get('authenticated_user')
        except:
            raise serializers.ValidationError('User do not exists.')
        return authenticated_user

    def validate(self, data):
        authenticated_user = self.__get_user_object(data)
        if False == check_password(data['old_password'], authenticated_user.password):
            raise serializers.ValidationError({'old_password' : "Invalid old password."})
        username = authenticated_user.username
        email = authenticated_user.email
        errors = {}
        password_validator = NewPasswordValidator(
            username=username,
            email=email,
            password_1=data['new_password_1'],
            password_2=data['new_password_2']
        )
        password_validator.validate(errors)
        if errors:
            raise serializers.ValidationError(errors)
        return data
