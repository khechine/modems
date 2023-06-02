from django import forms
from .models import contrat
from .models import stock_modemsn_gpon
from django.contrib.auth.models import User

from django_select2.forms import Select2Widget

class ContratReferenceForm(forms.Form):
    reference_contrat = forms.ChoiceField(
        widget=Select2Widget(attrs={'class': 'form-select mb-3'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reference_contrat'].choices = self.get_reference_contrat_choices()

    def get_reference_contrat_choices(self):
        return contrat.objects.all().values_list('reference_contrat', 'reference_contrat')
    

class NumerosSerieForm(forms.Form):
    serialNumber = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-select mb-3'}))

    def __init__(self, *args, user=None, groupe_connecte=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['serialNumber'].choices = self.get_serial_number_choices(groupe_connecte)

    def get_serial_number_choices(self, groupe_connecte):
        
        return stock_modemsn_gpon.objects.filter(statut=2, societeAff=groupe_connecte).values_list('serialNumber', 'serialNumber')


class SerialNumberStatut1Form(forms.Form):
    serialNumber = forms.ChoiceField(
        choices=[],
        widget=forms.Select(
            attrs={
                'class': 'form-control select2',
                'placeholder': 'Enter le N° de série du modem',
                'data-placeholder': 'Sélectionner un N° de série',
            }
        ),
        label=''  # Supprimer le label pour le champ
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['serialNumber'].choices = self.get_serial_number_choices()

    def get_serial_number_choices(self):
        return stock_modemsn_gpon.objects.filter(statut=1).values_list('serialNumber', 'serialNumber')


class SerialNumberStatut2Form(forms.Form):
    serialNumber = forms.ChoiceField(
        choices=[],
        widget=forms.Select(
            attrs={
                'class': 'form-control select2',
                'placeholder': 'Enter le N° de série du modem',
                'data-placeholder': 'Sélectionner un N° de série',
            }
        ),
        label=''  # Supprimer le label pour le champ
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['serialNumber'].choices = self.get_serial_number_choices()

    def get_serial_number_choices(self):
        return stock_modemsn_gpon.objects.filter(statut__gte=1).values_list('serialNumber', 'serialNumber')   





