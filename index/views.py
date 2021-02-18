from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages


# Create your views here.

def index(request):
    usergp = request.user.groups.all()
    grplist =[]
    for x in usergp:
        grplist.append(x)
    
    if request.user.is_authenticated:
        try:
            return redirect('dashboard:index', grplist[0])
        except:
            raise Http404('Plese contact your admin to assign you to a group')

    else:
        return render(request, 'index/landing.html')


def registerPage(request):
    usergp = request.user.groups.all()
    grplist =[]
    for x in usergp:
        grplist.append(x)
    
    if request.user.is_authenticated:
        return redirect('dashboard:index', grplist[0])
    else:
        form = CreateUserForm()
        ctx  = {'form' : form}
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()

                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')

                user = authenticate(request, username=username, password=password)
                login(request, user)

                return HttpResponseRedirect(reverse('index:index'))

        err = form.errors.values()
        err = list(err)
        ctx = {'form': form, 'err': err}

        return render(request, 'index/register.html', ctx)


def loginPage(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index:index'))
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                return redirect('index:index')
            else:
                messages.warning(request, 'Username or Password are incorrect')

        return render(request, 'index/login.html')

def logoutPage(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('index:index')
    else:
        messages.warning(request, "You need to login before you logout :/   ")
        return redirect('index:login')