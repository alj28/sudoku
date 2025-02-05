from django.urls import path
from .views import sign_up_view

urlpatterns = [
    path('', sign_up_view, name='signup'),
]