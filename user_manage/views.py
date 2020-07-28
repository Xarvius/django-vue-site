from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from django_server.settings import TEMPLATE_DIR
from user_manage.forms import UserForm, UserProfileForm


# Create your views here.

def home(request):
    return render(request, f'{TEMPLATE_DIR}/_homepage.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            # more?
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, f'{TEMPLATE_DIR}/pages/register.html',
                  {'user_form':user_form,
                   'profile_form':profile_form,
                   'registered':registered
                   })

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return  HttpResponse('Your account was inactive.')
        else:
            print('Failed login', f'on user:{username} pass:{password}')
            return HttpResponse('Invalid login')
    else:
        return render(request, f'{TEMPLATE_DIR}/pages/login.html')
