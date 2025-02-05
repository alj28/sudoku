from django.shortcuts import render

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from .serializers import SignUpSerializer


# Create your views here.
@api_view(['POST'])
@authentication_classes([]) 
@permission_classes([AllowAny])
def sign_up_view(request):
    if 'POST' != request.method:
        Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    print(f"{request.data}")
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        name = serializer.validated_data['name']
        lastname = serializer.validated_data['lastname']
        password = serializer.validated_data['password_2']
        username = f"{name.lower()}_{lastname.lower()}"

        try:
            user = User.objects.create_user(
                username=username,
                first_name=name,
                last_name=lastname,
                password=password
            )
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            # TODO: fix that as it may reveal too much data
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
