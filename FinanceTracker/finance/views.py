from django.shortcuts import render
from .forms import *
# Create your views here.


def dashboard(request):
    return render(request, 'dashboard.html')
    # return HttpResponse("Hello, world. You're at the finance index.")

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Save the user to the database
            pass
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Authenticate the user
            pass
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    return render(request, 'login.html')

