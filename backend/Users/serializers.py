
from rest_framework import serializers

class SignUpSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    lastname = serializers.CharField(max_length=100)
    password_1 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password_2 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        if data['password_1'] != data['password_2']:
            raise serializers.ValidationError('Passwords do not match')
        return data