from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .decorator import unauthenticated_user,allowed_users
from django.shortcuts import render
from .models import stock_modemsn_gpon,stock_modemsn,contrat,numacces
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.models import User
import csv
from django.views.generic import View
from django.contrib import messages
from .forms import ContratReferenceForm,NumerosSerieForm,SerialNumberStatut1Form,SerialNumberStatut2Form
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.serializers import serialize
from django.core.serializers import deserialize
from django.http import Http404
from .models import stock_modemsn_gpon, GenerateLogin

@login_required(login_url='login')
def home(request):
    return render(request,'modems/dashboard.html')

def affectationModem(request):
    return render(request,'modems/affectationModem.html')

def dashboard1(request):
    return render(request,'modems/dashboard1.html')

def consulterModem(request):
    return render(request,'modems/consulterModem.html')

def ajouterparamvoip(request):
    return render(request,'modems/ajouterparamvoip.html')

def importermodems(request):
    return render(request,'modems/importermodems.html')

def attribuermodems(request):
    return render(request,'modems/attribuermodems.html')

def attribuermodemslot(request):
    return render(request,'modems/attribuermodemslot.html')

def consultermodemsvoip(request):
    return render(request,'modems/consultermodemsvoip.html')

def modemaffecte(request):
    return render(request,'modems/modemaffecte.html')

def verifreference(request):
    return render(request,'modems/verifreference.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['stockAgent', 'admin'])
def alimentationModem(request):
    return render(request,'modems/alimentationModem.html')

def login(request):
    return render(request,'modems/login.html')



def statistiques(request):
    # Nombre de modems avec le statut 0
    num_statut_0 = stock_modemsn_gpon.objects.filter(statut=0).count()
    
    # Nombre de modems avec le statut 1
    num_statut_1 = stock_modemsn_gpon.objects.filter(statut=1).count()
    
    # Nombre de modems avec le statut 2
    num_statut_2 = stock_modemsn_gpon.objects.filter(statut=2).count()
    
    # Nombre de modems avec le statut 3
    num_statut_3 = stock_modemsn_gpon.objects.filter(statut=3).count()

    # Nombre de modems avec le statut 3 + sotetel
    num_statut_4 = stock_modemsn_gpon.objects.filter(statut=2, societeAff='sotetelAgent').count()
    
    # Nombre de modems avec le statut 3 + sotetel
    num_statut_5 = stock_modemsn_gpon.objects.filter(statut=2, societeAff='snttAgent').count()
    # Nombre de modems avec le statut 3 + sotetel
    societe_aff_values = ['agenceMarsa', 'agenceMourouj', 'agenceSousse']
    num_statut_6 = stock_modemsn_gpon.objects.filter(statut=2,  societeAff__in=societe_aff_values).count()
    
    # Nombre de modems avec le statut 3 + agenceMarsa
    num_statut_7 = stock_modemsn_gpon.objects.filter(statut=2, societeAff='agenceMarsa').count()
    
    # Nombre de modems avec le statut 3 + agenceMourouj
    num_statut_8 = stock_modemsn_gpon.objects.filter(statut=2, societeAff='agenceMourouj').count()
    
    # Nombre de modems avec le statut 3 + agenceMourouj
    num_statut_10 = numacces.objects.filter(reserve=1, agenceAff='agenceMarsa').count()

    # Nombre de modems avec le statut 3 + agenceMourouj
    num_statut_11 = numacces.objects.filter(reserve=1, agenceAff='agenceMourouj').count()

    # Nombre de modems avec le statut 3 + sotetel
    num_statut_12 = stock_modemsn_gpon.objects.filter(statut=3, societeAff='sotetelAgent').count()
    
    # Nombre de modems avec le statut 3 + sotetel
    num_statut_13 = stock_modemsn_gpon.objects.filter(statut=3, societeAff='snttAgent').count()
    # Nombre de modems avec le statut 3 + sotetel
    societe_aff_values = ['agenceMarsa', 'agenceMourouj', 'agenceSousse']
    num_statut_14 = stock_modemsn_gpon.objects.filter(statut=3,  societeAff__in=societe_aff_values).count()
    context = {'num_statut_0': num_statut_0,
               'num_statut_1': num_statut_1,
               'num_statut_2': num_statut_2,
               'num_statut_3': num_statut_3,
               'num_statut_4': num_statut_4,
               'num_statut_5': num_statut_5,
               'num_statut_6': num_statut_6,
               'num_statut_7': num_statut_7,
               'num_statut_8': num_statut_8,
               'num_statut_10': num_statut_10,
               'num_statut_11': num_statut_11,
               'num_statut_12': num_statut_12,
               'num_statut_13': num_statut_13,
               'num_statut_14': num_statut_14}
    
    return render(request, 'modems/dashboard1.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['snttAgent', 'admin','sotetelAgent'])
def ma_vue(request):
    contrat_form = ContratReferenceForm()
    serial_number_form = NumerosSerieForm()
    contrat_info = None

    if request.method == 'POST':
        if 'contrat_form_submit' in request.POST:
            contrat_form = ContratReferenceForm(request.POST)
            if contrat_form.is_valid():
                reference_contrat_select = contrat_form.cleaned_data['reference_contrat']
                try:
                    nom_group = request.POST.get('nom_group')
                    
                    contrat_info = contrat.objects.get(reference_contrat=reference_contrat_select)
                    
                    # Pass the group name to the serial number form
                    serial_number_form = NumerosSerieForm(groupe_connecte=nom_group)
                    
                    serial_number_form.fields['serialNumber'].queryset = stock_modemsn_gpon.objects.filter(societeAff=nom_group)
                except contrat.DoesNotExist:
                    messages.error(request, 'Le contrat sélectionné n\'existe pas.')
        
        elif 'serial_number_form_submit' in request.POST:
                reference_contrat_select = request.POST.get('ref_tt')
                serial_number_select = request.POST.get('serialNumber')
                nom_agent = request.POST.get('nom_agent')
                try:
                    contrat_info = contrat.objects.get(reference_contrat=reference_contrat_select)
                    modem = stock_modemsn_gpon.objects.get(serialNumber=serial_number_select)
                    modem.refDemande = reference_contrat_select
                    modem.statut=3
                    modem.agent=nom_agent
                    modem.save()
                    # Supprimer la ligne contenant la référence du contrat de la table contrat
                    # contrat_info.delete()
                    message = 'Affectation du modem {} au contrat {} réussie.'.format(serial_number_select, reference_contrat_select)
                    messages.success(request, message)
                except contrat.DoesNotExist:
                    messages.error(request, 'Le contrat sélectionné n\'existe pas.')
                except stock_modemsn_gpon.DoesNotExist:
                    messages.error(request, 'Le numéro de série sélectionné n\'existe pas.')

    return render(request, 'modems/affectationModem.html', {'contrat_form': contrat_form, 'serial_number_form': serial_number_form, 'contrat_info': contrat_info})


@login_required(login_url='login')
@allowed_users(allowed_roles=['stockAgent', 'admin'])
def consulterModem(request):
    all_modems = stock_modemsn_gpon.objects.filter(statut=1)  # Tous les modems avec statut=1

    if request.method == 'POST':
        form = SerialNumberStatut1Form(request.POST)
        if form.is_valid():
            selected_modem = form.cleaned_data['serialNumber']
            modems = all_modems.filter(serialNumber=selected_modem)
    else:
        form = SerialNumberStatut1Form()
        modems = all_modems  # Afficher tous les modems par défaut

    context = {'form': form, 'modems': modems}
    return render(request, 'modems/consulterModem.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['stockAgent', 'admin'])
def attribuermodems(request):
    modems_list = stock_modemsn_gpon.objects.filter(statut=1)
    paginator = Paginator(modems_list, 4)  # Divise les modems en pages de 4 modems par page

    page_number = request.GET.get('page')
    try:
        modems = paginator.get_page(page_number)
    except PageNotAnInteger:
        # Si le numéro de page n'est pas un entier, affiche la première page
        modems = paginator.get_page(1)
    except EmptyPage:
        # Si le numéro de page est en dehors de la plage des pages valides, affiche la dernière page
        modems = paginator.get_page(paginator.num_pages)

    if request.method == 'POST':
        modem_id = request.POST.get('modem_id')
        societeAffecte = request.POST.get('societeAffecte')
        nom_agent = request.POST.get('nom_agent')

        if societeAffecte == '0':
            # Afficher un message d'erreur
            messages.error(request, "Vous n'avez pas choisi la société à affecter.")
            return redirect('attribuermodems')

        modem = stock_modemsn_gpon.objects.get(id=modem_id)
        modem.statut = 2
        modem.societeAff = societeAffecte
        modem.agent = nom_agent
        modem.save()

        # Afficher un message de succès
        messages.success(request, "Modem attribué avec succès.")
        return redirect('attribuermodems')

    context = {'modems': modems}
    return render(request, 'modems/attribuermodems.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['voipAgent', 'admin'])
def ajoutVoip(request):
    modems = stock_modemsn_gpon.objects.filter(statut=0)
    return render(request, 'modems/ajouterparamvoip.html', {'modems': modems})





def genere_login(type_acces):
    generate_login = GenerateLogin.objects.get(type_acces=type_acces)
    nombre = generate_login.nombre
    prefix = generate_login.prefix
    prefix_top = generate_login.prefix_top

    generate_login.nombre += 1
    generate_login.save()

    string_number = str(nombre)
    if len(string_number) < 5:
        string_number = "0" * (5 - len(string_number)) + string_number

    return prefix + string_number + prefix_top


import random
import string

def generate_password(size):
    # Initialisation des caractères utilisables
    characters = string.ascii_letters + string.digits

    # Générer un mot de passe aléatoire de la taille spécifiée
    password = ''.join(random.choice(characters) for i in range(size))

    return password


@login_required(login_url='login')
@allowed_users(allowed_roles=['stockAgent', 'admin'])
def import_modems(request):
    existing_serial_numbers = list(stock_modemsn.objects.values_list('serialNumber', flat=True))
    if request.method == 'POST':
        if 'csv_file' not in request.FILES:
            message = 'Aucun fichier sélectionné'
            return render(request, 'modems/alimentationModem.html', {'error_message': message})

        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file, delimiter=';')
        existing_modems = []
        new_modems = []
        missing_modems = []
        duplicate_modems = []
        for row in reader:
            if len(row) < 1:
              continue
            serial_number = row[0]
            if stock_modemsn_gpon.objects.filter(serialNumber=serial_number).exists():
                # Si le modem existe déjà dans stock_modemsn_gpon, on l'ajoute à la liste des modems en double
                duplicate_modems.append(serial_number)
                continue
            try:
                modem = stock_modemsn.objects.get(serialNumber=serial_number)
                # Si le modem existe déjà, on l'ajoute à la liste des modems existants
                existing_modems.append(modem)
                new_modem = stock_modemsn_gpon()
                new_modem.equipementName = modem.equipement
                new_modem.serialNumber = modem.serialNumber
                new_modem.pwdParDefaut = modem.pwdParDefaut
                new_modem.typeModem = modem.typeModem
                new_modem.loginParDefaut = modem.loginParDefaut
                new_modem.statut = 0
                if modem.typeModem.lower() == 'non':
                    generate_login = generate_login = GenerateLogin.objects.get(type_acces=1)
                    loginParDefaut = genere_login(type_acces=2)
                    pwdParDefaut = generate_password(12)
                    new_modem.loginParDefaut = loginParDefaut
                    new_modem.pwdParDefaut = pwdParDefaut
                else:
                    new_modem.pwdParDefaut = modem.pwdParDefaut
                    new_modem.loginParDefaut = modem.loginParDefaut    
                new_modems.append(new_modem)
            except ObjectDoesNotExist:
                # Si le modem n'existe pas, on l'ajoute à la liste des modems manquants
                missing_modems.append(serial_number)
            except MultipleObjectsReturned:
                # Si plusieurs modems ont été trouvés avec le même numéro de série, on les ajoute tous à la liste des modems existants
                modems = stock_modemsn.objects.filter(serialNumber=serial_number)
                existing_modems.extend(modems)

        # On crée les nouveaux modems s'ils existent
        if new_modems:
            stock_modemsn_gpon.objects.bulk_create(new_modems)
            if len(duplicate_modems) > 0:
                # Si des modems en double ont été trouvés, on renvoie une erreur BadRequest avec la liste des modems en double
                return render(request, 'modems/alimentationModem.html', {'success': True, 'existing_modems': existing_modems, 'new_modems': new_modems, 'missing_modems': missing_modems, 'duplicate_modems': duplicate_modems})
            
        return render(request, 'modems/alimentationModem.html', {'success': True, 'existing_modems': existing_modems, 'new_modems': new_modems, 'missing_modems': missing_modems, 'duplicate_modems': duplicate_modems})
        
    return render(request, 'modems/alimentationModem.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['voipAgent', 'admin'])
def modem_list(request):
    modems = stock_modemsn_gpon.objects.filter(statut=0)
    context = {
        'modems': modems,
    }
    return render(request, 'ajouterparamvoip.html', context)

def export_csv(request):
    modems = stock_modemsn_gpon.objects.filter(statut=0)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="modems.csv"'

    writer = csv.writer(response)
    # writer.writerow(['Serial Number'])

    for modem in modems:
        writer.writerow([modem.serialNumber])

    return response

@login_required(login_url='login')
@allowed_users(allowed_roles=['voipAgent', 'admin'])
def importermodems(request):
    error_message = None
    success_message = None
    if request.method == 'POST':
        if 'csv_file' not in request.FILES:
            error_message = 'Aucun fichier sélectionné'
            return render(request, 'modems/importermodems.html', {'error_message': error_message})
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file, delimiter=';')
        new_modems = []
        for row in reader:
            try:
                serial_number = row[0]
                modems = stock_modemsn_gpon.objects.filter(serialNumber=serial_number) 
                if modems.exists():
                    modem = modems.first()
                    modem.loginVoip = row[1]
                    modem.pwdVoip = row[2]
                    modem.statut = 1
                    modem.save()
                else:
                    error_message = 'le fichier est vide'

            except IndexError:
                error_message = 'Le format du fichier CSV est incorrect'
                return render(request, 'modems/importermodems.html', {'error_message': error_message})
        stock_modemsn_gpon.objects.bulk_create(new_modems)
        success_message = 'Import effectué avec succès'
        return render(request, 'modems/importermodems.html', {'success_message': success_message})
    return render(request, 'modems/importermodems.html', {'error_message': error_message})






@login_required(login_url='login')
@allowed_users(allowed_roles=['stockAgent', 'admin'])
def attribuermodemslot(request):
    modems = stock_modemsn_gpon.objects.filter(statut=1)
    users = User.objects.filter(groups__name='sotetelAgent')

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        selected_modems = request.POST.getlist('modem_id')
        societeAffecte = request.POST.get('societeAffecte')

        success_count = 0
        error_count = 0
        error_modems = []

        for modem_id in selected_modems:
            try:
                modem = stock_modemsn_gpon.objects.get(id=modem_id)
            except stock_modemsn_gpon.DoesNotExist:
                continue

            if modem.statut != 2:
                modem.societeAff = societeAffecte
                modem.statut = 2
                modem.save()
                success_count += 1
            else:
                error_count += 1
                error_modems.append(modem)

        if request.FILES.get('csv_file'):
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            csv_data = csv.reader(decoded_file)

            for row in csv_data:
                if len(row) > 0:
                    serial_number = row[0]

                    existing_modems = stock_modemsn_gpon.objects.filter(serialNumber=serial_number)

                    for existing_modem in existing_modems:
                        if existing_modem.statut != 2:
                            existing_modem.societeAff = societeAffecte
                            existing_modem.statut = 2
                            existing_modem.save()
                            success_count += 1
                        else:
                            error_count += 1
                            error_modems.append(existing_modem)
                else:
                    # Gérer le cas où la liste row est vide
                    error_count += 1

        if success_count > 0:
            messages.success(request, f"{success_count} modem(s) affecté(s) avec succès.")

        if error_count > 0:
            error_message = f"{error_count} modem(s) ne sont pas configurés ou déjà affectés."
            messages.error(request, error_message)

        return redirect('attribuermodemslot')

    context = {'modems': modems, 'users': users}
    return render(request, 'modems/attribuermodemslot.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['voipAgent', 'admin'])
def consultermodemsvoip(request):

    all_modems = stock_modemsn_gpon.objects.filter(statut__gte=1)  # Tous les modems avec statut=1

    if request.method == 'POST':
        form = SerialNumberStatut2Form(request.POST)
        if form.is_valid():
            selected_modem = form.cleaned_data['serialNumber']
            modems = all_modems.filter(serialNumber=selected_modem)
    else:
        form = SerialNumberStatut2Form()
        modems = all_modems  # Afficher tous les modems par défaut

    context = {'form': form, 'modems': modems}
    return render(request, 'modems/consultermodemsvoip.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['snttAgent', 'admin','sotetelAgent'])
def modemaffecte(request):
    if request.user.groups.filter(name='sotetelAgent').exists():
        modems = stock_modemsn_gpon.objects.filter(statut=3, societeAff='sotetelAgent')
    elif request.user.groups.filter(name='snttAgent').exists():
        modems = stock_modemsn_gpon.objects.filter(statut=3, societeAff='snttAgent')
    else:
        modems = []

    context = {
        'modems': modems,
    }
    return render(request, 'modems/modemaffecte.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['snttAgent', 'admin','sotetelAgent'])
def verifreference(request):
    error_message = None
    success_message = None
    existing_refs = []
    missing_refs = []

    if request.method == 'POST':
        if 'csv_file' not in request.FILES:
            error_message = 'Aucun fichier sélectionné'
            return render(request, 'modems/verifreference.html', {'error_message': error_message})

        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file, delimiter=';')

        for row in reader:
            try:
                ref_tt = row[0]
                references = contrat.objects.filter(reference_contrat=ref_tt) 

                if references.exists():
                    existing_refs.append(references.first())
                else:
                    missing_refs.append(ref_tt)

            except IndexError:
                error_message = 'Le format du fichier CSV est incorrect'
                return render(request, 'modems/verifreference.html', {'error_message': error_message})

        success_message = 'Import effectué avec succès'
        # Sérialiser les références existantes au format JSON
        serialized_existing_refs = serialize('json', existing_refs)

        # Sauvegarder les références existantes dans la session
        request.session['existing_refs'] = serialized_existing_refs
    return render(request, 'modems/verifreference.html', {
        'error_message': error_message,
        'success_message': success_message,
        'existing_refs': existing_refs,
        'missing_refs': missing_refs
    })



@login_required(login_url='login')
def export_references_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="references.csv"'

    writer = csv.writer(response)
    writer.writerow(['Reference Contrat', 'Prénom Client', 'Nom Client', 'GSM Client'])

    serialized_existing_refs = request.session.get('existing_refs', '[]')
    existing_refs = list(deserialize('json', serialized_existing_refs))

    for reference in existing_refs:
        reference_obj = reference.object
        writer.writerow([
            reference_obj.reference_contrat,
            reference_obj.prenom_client,
            reference_obj.nom_client,
            reference_obj.gsm_client
        ])

    return response



@login_required(login_url='login')
def consulterreferenceaffecte(request):

    all_modems = stock_modemsn_gpon.objects.filter(statut__gte=3)  # Tous les modems avec statut=1

    if request.method == 'POST':
        form = SerialNumberStatut2Form(request.POST)
        if form.is_valid():
            selected_modem = form.cleaned_data['serialNumber']
            modems = all_modems.filter(serialNumber=selected_modem)
    else:
        form = SerialNumberStatut2Form()
        modems = all_modems  # Afficher tous les modems par défaut

    context = {'form': form, 'modems': modems}
    return render(request, 'modems/consulterreferenceaffecte.html', context)