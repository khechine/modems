from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard1')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard1')
            else:
                messages.info(request, 'username or password incorrect')
        context = {}
        return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')    
