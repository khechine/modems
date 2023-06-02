from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

class User(models.Model):
    choix = [
        ("Sotetel", "Sotetel"),
        ("Stock", "Stock"),
        ("AjoutParaVoip", "AjoutParaVoip"),
    ]
    name = models.CharField(max_length=100,null=True)
    email = models.CharField(max_length=100,null=True)
    phone = models.CharField(max_length=15,null=True)
    age = models.CharField(max_length=10,null=True)
    service = models.CharField(max_length=30,choices=choix,null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.name
    
class stock_modemsn_gpon(models.Model):
       choixModem = [
        ("oui", "oui"),
        ("non", "non"),
    ]
       equipementName = models.CharField(max_length=100,null=True)
       macAdress = models.CharField(max_length=32,null=True)
       serialNumber = models.CharField(max_length=32,null=True)
       etatModem = models.CharField(max_length=2,null=True)
       refDemande = models.CharField(max_length=100,null=True)
       typeModem = models.CharField(max_length=5,choices=choixModem,null=True)
       loginParDefaut = models.CharField(max_length=100,null=True)
       pwdParDefaut = models.CharField(max_length=100,null=True)
       loginVoip = models.CharField(max_length=100,null=True)
       pwdVoip = models.CharField(max_length=100,null=True)
       statut = models.IntegerField(null=True)
       dateStatut = models.DateTimeField(auto_now_add=True,null=True)
       agent = models.CharField(max_length=100,null=True)
       societeAff = models.CharField(max_length=100,null=True)
       numAcces = models.IntegerField( null=True)


       dateInsertion = models.DateTimeField(auto_now_add=True,null=True)
       def __str__(self):
        return self.equipementName
       

class stock_modemsn(models.Model):
       choixModem = [
        ("oui", "oui"),
        ("non", "non"),
    ]
       equipement = models.CharField(max_length=100,null=True)
       macAdress = models.CharField(max_length=32,null=True)
       serialNumber = models.CharField(max_length=32,null=True)
       etatModem = models.CharField(max_length=2,null=True)
       refDemande = models.CharField(max_length=100,null=True)
       typeModem = models.CharField(max_length=5,choices=choixModem,null=True)
       loginParDefaut = models.CharField(max_length=100,null=True)
       pwdParDefaut = models.CharField(max_length=100,null=True)
       loginVoip = models.CharField(max_length=100,null=True)
       pwdVoip = models.CharField(max_length=100,null=True)
       statut = models.IntegerField(null=True)
       dateStatut = models.DateTimeField(auto_now_add=True,null=True)
       agent = models.CharField(max_length=100,null=True)
       dateInsertion = models.DateTimeField(auto_now_add=True,null=True)
       def __str__(self):
        return self.equipement



class GenerateLogin(models.Model):
    type_acces = models.IntegerField()
    nombre = models.IntegerField()
    prefix = models.CharField(max_length=10)
    prefix_top = models.CharField(max_length=15)


class contrat(models.Model):
    reference_contrat = models.CharField(max_length=30)
    nom_client = models.CharField(max_length=30)
    prenom_client = models.CharField(max_length=30)
    gsm_client = models.IntegerField(null=True)

    def __str__(self):
        return self.reference_contrat

class numacces(models.Model):
  
    num = models.IntegerField( null=True)
    region = models.CharField(max_length=50)
    equipement = models.CharField(max_length=100,null=True)
    reserve = models.BooleanField(default=False)  # New field
    serialNum = models.CharField(max_length=100,null=True)
    agenceAff = models.CharField(max_length=100,null=True)
    def __str__(self):
        return str(self.num) 
   