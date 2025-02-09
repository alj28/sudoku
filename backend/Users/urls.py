from django.urls import path
from .views import sign_up_view, change_password_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshSlidingView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshSlidingView.as_view(), name='token_refresh'),
    path('new/', sign_up_view, name='signup'),
    path('password_update/', change_password_view, name='change_password')
]