from django.shortcuts import render
from .forms import *
from .models import *
from django.db.models import Sum
from datetime import date
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def dashboard(request):
    user = request.user
    
    income = Transaction.objects.filter(user=user, type='Income').aggregate(Sum('amount'))['amount__sum'] or 0
    expenses = Transaction.objects.filter(user=user, type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = income - expenses
    
    recent_transactions = Transaction.objects.filter(user=user).order_by('-date')[:5]
    
    category_data = (
        Transaction.objects.filter(user=user, type='Expense')
        .values('category__name')
        .annotate(total=Sum('amount'))
    )
    
    labels = [entry['category__name'] for entry in category_data]
    data = [entry['total'] for entry in category_data]
    
    context = {
        balance: balance,
        'income': income,
        'expenses': expenses,
        'recent_transactions': recent_transactions,
        'labels': labels,
        'data': data,
    }
    
    return render(request, 'dashboard.html', context)
  

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from .forms import RegisterForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password_confirm']

            if password != password_confirm:
                form.add_error('password_confirm', 'Passwords do not match')
            elif User.objects.filter(username=username).exists():
                form.add_error('username', 'Username already exists')
            elif User.objects.filter(email=email).exists():
                form.add_error('email', 'Email already exists')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                auth_login(request, user)  # Log the user in
                return redirect('dashboard')  # Redirect to dashboard after registration
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


from django.contrib.auth import authenticate, login as auth_login

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})



from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect

def logout(request):
    auth_logout(request)
    return redirect('login')

def transaction(request):
    return render(request, 'transaction.html')
