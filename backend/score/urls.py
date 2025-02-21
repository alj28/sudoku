from django.urls import path
from .views import get_new_game_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshSlidingView

urlpatterns = [
    path('get_new_game/', get_new_game_view, name='get_new_game')
]