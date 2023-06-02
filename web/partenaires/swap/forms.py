from django import forms
from modems.models import stock_modemsn_gpon,numacces
#from .models import numacces

from django import forms

class NumaccesForm(forms.Form):
    num = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select mb-3'})
    )

    def __init__(self, *args, **kwargs):
        super(NumaccesForm, self).__init__(*args, **kwargs)
        numacces_list = numacces.objects.filter(reserve=0)
        numacces_choices = [(num, num) for num in numacces_list]
        self.fields['num'].choices = numacces_choices


class SerialNumberStatut1Form(forms.Form):
    serialNumber = forms.ChoiceField(choices=(), widget=forms.Select(attrs={'class': 'form-control select2'}))

    def __init__(self, equipementName=None, societeAff_value=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['serialNumber'].choices = self.get_serial_number_choices(equipementName, societeAff_value)

    def get_serial_number_choices(self, type_modem_value, societeAff_value):
        queryset = stock_modemsn_gpon.objects.filter(equipementName=type_modem_value,statut=2)
        if societeAff_value is not None:
            queryset = queryset.filter(societeAff=societeAff_value)
        return queryset.values_list('serialNumber', 'serialNumber')


class numreserveForm(forms.Form):
    num = forms.ChoiceField(
        choices=[],
        widget=forms.Select(
            attrs={
                'class': 'form-control select2',
                'placeholder': 'Enter le N° reservé',
                'data-placeholder': 'Sélectionner un N° d accés',
            }
        ),
        label=''  # Supprimer le label pour le champ
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['num'].choices = self.get_number_choices()

    def get_number_choices(self):
        return numacces.objects.filter(reserve=1).values_list('num', 'num') 

class numreserveagenceconnecteForm(forms.Form):
    num = forms.ChoiceField(
        choices=[],
        widget=forms.Select(
            attrs={
                'class': 'form-control select2',
                'placeholder': 'Enter le N° reservé',
                'data-placeholder': 'Sélectionner un N° d accés',
            }
        ),
        label=''  # Supprimer le label pour le champ
    )

    def __init__(self, *args, groupe_connecte=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['num'].choices = self.get_number_choices(groupe_connecte)

    def get_number_choices(self, groupe_connecte):
        return numacces.objects.filter(reserve=1, agenceAff=groupe_connecte).values_list('num', 'num')       