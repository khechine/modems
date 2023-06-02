from django.shortcuts import render
from modems.models import stock_modemsn_gpon,numacces 
from .forms import NumaccesForm,SerialNumberStatut1Form,numreserveForm,numreserveagenceconnecteForm
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from modems.views import login_required
from django.contrib import messages
import csv
from modems.decorator import unauthenticated_user,allowed_users
#@login_required(login_url='login')

def insertnumber(request):
    return render(request,'swapmodem.html')

def importernumero(request):
    return render(request,'importernumero.html')

def consulternumero(request):
    return render(request,'consulternumero.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['agenceMarsa', 'admin','agenceMourouj','agenceSousse'])
def get_numacces(request):
    form = NumaccesForm()
    context = {'form': form}

    type_modem_value = 'oui'  # Valeur souhaitée

    if request.method == 'POST':
        num = request.POST.get('num')
        nom_group = request.POST.get('nom_group')
        numacces_list = numacces.objects.filter(num=num).all()

        if numacces_list:
            first_numacces = numacces_list[0]
            equipement = first_numacces.equipement
            form = SerialNumberStatut1Form(equipementName=equipement, societeAff_value=nom_group)
            context['form'] = form
            user_group = str(request.user.groups.first())

            if 'serial_number_form_submit' in request.POST:
                serial_number_select = request.POST.get('serialNumber')
                first_numacces.reserve = 1
                first_numacces.serialNum = serial_number_select
                first_numacces.agenceAff = user_group   # Changer la valeur de l'attribut 'reserve'
                first_numacces.save()  # Enregistrer les modifications dans la base de données
                nom_agent = request.POST.get('nom_agent')
                try:
                    modem = stock_modemsn_gpon.objects.get(serialNumber=serial_number_select)
                    modem.statut = 3
                    modem.agent = nom_agent
                    #modem.numAcces=num
                    modem.save()
                    # Supprimer la ligne contenant la référence du contrat de la table contrat
                    # contrat_info.delete()
                    message = 'Affectation du modem {} réussie.'.format(serial_number_select)
                    messages.success(request, message)
                except modem.DoesNotExist:
                    messages.error(request, 'Le contrat sélectionné n\'existe pas.')
                except stock_modemsn_gpon.DoesNotExist:
                    messages.error(request, 'Le numéro de série sélectionné n\'existe pas.')

            return render(request, 'swapmodem.html', {'numacces_list': numacces_list, 'num': num, **context})
        else:
            return render(request, 'swapmodem.html', {'error_message': 'Numéro invalide'})

    return render(request, 'swapmodem.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','intervention'])
def importernumero(request):
    error_message = None
    success_message = None
    
    if request.method == 'POST':
        if 'csv_file' not in request.FILES:
            error_message = 'Aucun fichier sélectionné'
            return render(request, 'importernumero.html', {'error_message': error_message})
        
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file, delimiter=';')
        typemodem = request.POST.get('typemodem')
        existing_numacces = []
        new_numacces = []
        
        for row in reader:
            try:
                numabonne = row[0]
                numeros = numacces.objects.filter(num=numabonne)
                
                if numeros.exists():
                    existing_numacces.append(numeros.first())
                else:
                    new_numacces.append(numacces(num=numabonne, region=row[1], equipement=typemodem))
            except IndexError:
                error_message = 'Le format du fichier CSV est incorrect'
                return render(request, 'importernumero.html', {'error_message': error_message})
        
        if new_numacces:
            numacces.objects.bulk_create(new_numacces)
            success_message = 'Import effectué avec succès'
        
        if existing_numacces:
            return render(request, 'importernumero.html', {'existing_numacces': existing_numacces, 'success_message': success_message})
        
        return render(request, 'importernumero.html', {'success_message': success_message})
    
    return render(request, 'importernumero.html', {'error_message': error_message})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','intervention'])
def consulternumero(request):
    all_modems = numacces.objects.filter(reserve=1)  # Tous les modems avec statut=1
    agents = []  # Initialize agents list

    for modem in all_modems:
        serialNum = modem.serialNum  # Récupérer le serialNum de l'objet numacces
        # Récupérer les agents pour le serialNum actuel
        agents_for_num = stock_modemsn_gpon.objects.filter(serialNumber=serialNum)
        agents.extend([(agent.agent, modem.region, agent.societeAff, modem.serialNum) for agent in agents_for_num])

    if request.method == 'POST':
        form = numreserveForm(request.POST)
        if form.is_valid():
            selected_modem = form.cleaned_data['num']
            modems = all_modems.filter(num=selected_modem)
    else:
        form = numreserveForm()
        modems = all_modems  # Afficher tous les modems par défaut

    context = {'form': form, 'modems': modems, 'agents': agents}
    return render(request, 'consulternumero.html', context)


from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
@allowed_users(allowed_roles=['agenceMarsa', 'admin','agenceMourouj','agenceSousse'])
def consulternumparagence(request):
    user_group = request.user.groups.first()
    all_modems = numacces.objects.filter(reserve=1, agenceAff=user_group)  # Tous les modems avec statut=1
    agents = []  # Initialize agents list

    for modem in all_modems:
        serialNum = modem.serialNum  # Récupérer le serialNum de l'objet numacces
        # Récupérer les agents pour le serialNum actuel
        agents_for_num = stock_modemsn_gpon.objects.filter(serialNumber=serialNum)
        agents.extend([(agent.agent, modem.region, agent.societeAff, modem.serialNum) for agent in agents_for_num])

    if request.method == 'POST':
        form = numreserveForm(request.POST)
        if form.is_valid():
            selected_modem = form.cleaned_data['num']
            modems = all_modems.filter(num=selected_modem)
    else:
        user_group = str(request.user.groups.first())
        form = numreserveagenceconnecteForm(groupe_connecte=user_group)
        modems = all_modems  # Afficher tous les modems par défaut

    context = {'form': form, 'modems': modems, 'agents': agents}
    return render(request, 'consulternumparagence.html', context)





    


