
from rest_framework import serializers, status
from password_strength import PasswordPolicy
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

PASSWORD_CHARFIELD_ARGS = {
    "write_only"    :   True, 
    "style"         :   {
        'input_type': 'password'
    }
}

def password_policy_check(password: str):
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
        raise serializers.ValidationError('Password too weak', code=status.HTTP_400_BAD_REQUEST)

class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password_1 = serializers.CharField(**PASSWORD_CHARFIELD_ARGS)
    password_2 = serializers.CharField(**PASSWORD_CHARFIELD_ARGS)

    def validate(self, data):
        # explicitly check whether email and username are unique
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('User already exists.', code=status.HTTP_409_CONFLICT)
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('User already exists.', code=status.HTTP_409_CONFLICT)
        if data['password_1'] != data['password_2']:
            raise serializers.ValidationError('Passwords do not match', code=status.HTTP_400_BAD_REQUEST)
        if data['username'] == data['password_1']:
            raise serializers.ValidationError('Password too weak', code=status.HTTP_400_BAD_REQUEST)
        password_policy_check(data['password_1'])
        return data
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(**PASSWORD_CHARFIELD_ARGS)
    new_password_1 = serializers.CharField(**PASSWORD_CHARFIELD_ARGS)
    new_password_2 = serializers.CharField(**PASSWORD_CHARFIELD_ARGS)

    def validate(self, data):
        try:
            authenticated_user = self.context.get('authenticated_user')
        except:
            raise serializers.ValidationError('User do not exists.', code=status.HTTP_400_BAD_REQUEST)
        username = authenticated_user.username

        if data['new_password_1'] != data['new_password_2']:
            raise serializers.ValidationError('Passwords do not match', code=status.HTTP_400_BAD_REQUEST)
        if username == data['new_password_1']:
            raise serializers.ValidationError('Password too weak', code=status.HTTP_400_BAD_REQUEST)
        if data['old_password'] == data['new_password_1']:
            raise serializers.ValidationError('Bad password', code=status.HTTP_400_BAD_REQUEST)
        password_policy_check(data['new_password_1'])


        if True == check_password(data['new_password_1'], authenticated_user.password):
            raise serializers.ValidationError('Invalid password', code=status.HTTP_400_BAD_REQUEST)
        if False == check_password(data['old_password'], authenticated_user.password):
            raise serializers.ValidationError('Invalid password', code=status.HTTP_400_BAD_REQUEST)
        return data
