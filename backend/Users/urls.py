from django.urls import path
from .views import sign_up_view, change_password_view

urlpatterns = [
    path('', sign_up_view, name='signup'),
    path('change_password/', change_password_view, name='change_password')
]