from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>', views.UserViewSet.as_view({'get': 'get', 'put': 'put'})),
]