from django.shortcuts import render

from django.shortcuts import render

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from dataclasses import asdict

from .services import generate_sudoku_game, DifficultyLevel

# Create your views here.
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_new_game_view(request):
    
    try:
        game = generate_sudoku_game(DifficultyLevel.MEDIUM)
    except ConnectionError:
        return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(
        {
            'board' :   game.board,
            'solution'  :   game.solution,
            'difficulty'    :   game.difficulty_level
        },
        status=status.HTTP_200_OK
    )
