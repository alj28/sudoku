
from rest_framework import serializers
from password_strength import PasswordPolicy

class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100)
    lastname = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password_1 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password_2 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        if data['password_1'] != data['password_2']:
            raise serializers.ValidationError('Passwords do not match')
        if data['username'] == data['password_1']:
            raise serializers.ValidationError('Password too weak')

        policy = PasswordPolicy.from_names(
            length=8,
            uppercase=2,
            numbers=2,
            special=2,
            nonletters=2
        )
        # PasswordPolicy does not support definition for minimum number of lower-case characters
        n_lower_case = len([c for c in data['password_1'] if c.islower()])
        if 0 != len(policy.test(data['password_1'])) or n_lower_case < 2:
            raise serializers.ValidationError('Password too weak')
        return data