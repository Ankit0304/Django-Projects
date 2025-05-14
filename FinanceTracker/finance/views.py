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

def transaction(request):
    return render(request, 'transaction.html')
