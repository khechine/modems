from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import ma_vue
from .views import consulterModem
from .views import import_modems
from .views import ajoutVoip
from .views import modem_list
from .views import importermodems
from .views import attribuermodems
from .views import statistiques
from .views import attribuermodemslot
from .views import consultermodemsvoip,modemaffecte,verifreference,consulterreferenceaffecte
from django.urls import path
from .views import export_csv
from swap.views import get_numacces


urlpatterns = [
    path('', views.home,name='home'),
    path('affectationModem/', ma_vue, name='affectationModem'),
    path('dashboard1/', statistiques, name='statistiques'),
    path('dashboard1/', views.dashboard1, name='dashboard1'),
    path('consulterModem/', consulterModem, name='consulterModem'),
    path('ajouterparamvoip/', ajoutVoip, name='ajouterparamvoip'),
    path('importermodems/', importermodems, name='importermodems'),
    path('attribuermodems/', attribuermodems, name='attribuermodems'),
    path('attribuermodemslot/', views.attribuermodemslot, name='attribuermodemslot'), 
    path('consultermodemsvoip/', views.consultermodemsvoip, name='consultermodemsvoip'),
    path('consultermodemsvoip/', consultermodemsvoip, name='consultermodemsvoip'),
    path('consulterreferenceaffecte/', views.consulterreferenceaffecte, name='consulterreferenceaffecte'),
    path('consulterreferenceaffecte/', consulterreferenceaffecte, name='consulterreferenceaffecte'),
    path('attribuermodemslot/', attribuermodemslot, name='attribuermodemslot'),    
    path('alimentationModem/', import_modems,name='alimentationModem'),
    path('verifReference/', verifreference,name='verifreference'),
    path('verifreference/', views.verifreference,name='verifreference'),
    path('login/', views.login,name='login'),
  # URL pour afficher le tableau des données
    path('ajouterparamvoip/', views.modem_list, name='modem_list'),
    path('modemaffecte/', views.modemaffecte, name='modemaffecte'),
    path('modemaffecte/', modemaffecte, name='modemaffecte'),
    # URL pour télécharger le fichier CSV
    path('export/csv/', views.export_references_csv, name='export_references_csv'),
    path('export/csv2/', views.export_csv, name='export_csv'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('insertnumber/', get_numacces, name='get_numacces'),
]