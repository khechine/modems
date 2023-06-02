from django.urls import path
from . import views 
from .views import loginPage
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('login/', loginPage, name='login'),
    path('logout/', views.logoutUser,name='logout'),
]