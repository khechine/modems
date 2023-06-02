from django.urls import path
from . import views
from .views import get_numacces,importernumero

urlpatterns = [
    path('swapmodem/', get_numacces, name='get_numacces'),
    path('importernumero/', importernumero, name='importernumero'),
    path('consulternumero/', views.consulternumero, name='consulternumero'),
    path('consulternumparagence/', views.consulternumparagence, name='consulternumparagence'),
    # Autres URLs spécifiques à votre application
]


