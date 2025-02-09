from django.shortcuts import render

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from .serializers import SignUpSerializer, ChangePasswordSerializer


# Create your views here.
@api_view(['POST'])
@authentication_classes([]) 
@permission_classes([AllowAny])
def sign_up_view(request):
    if 'POST' != request.method:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        first_name = serializer.validated_data['first_name']
        last_name = serializer.validated_data['last_name']
        password = serializer.validated_data['password_1']
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']

        try:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
                email=email
            )
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            # TODO: fix that as it may reveal too much data
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def change_password_view(request):
    if 'POST' != request.method:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    authenticated_user = request.user

    serializer = ChangePasswordSerializer(
        data=request.data,
        context={
            'authenticated_user'    :   authenticated_user
        }
    )
    if serializer.is_valid():
        #try:
        #    user = User.objects.get(username=serializer.validated_data['username'])
        #except:
        #    return Response("Unknown user.", status=status.HTTP_400_BAD_REQUEST)
        try:
            # hashed password should be stored
            authenticated_user.set_password(serializer.validated_data['new_password_1'])
            authenticated_user.save()
        except:
            return Response("Unable to update password", status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)