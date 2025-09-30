from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.db.models import Sum
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
import json
from .models import Transaction
from django.db.models import Sum, F
from .models import Budget

@login_required
def dashboard(request):
    # Total Income/Expense
    income = Transaction.objects.filter(user=request.user, category__type='income').aggregate(total=Sum('amount'))['total'] or 0
    expense = Transaction.objects.filter(user=request.user, category__type='expense').aggregate(total=Sum('amount'))['total'] or 0
    balance = float(income) - float(expense)

    # Recent transactions
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')[:5]

    # Budgets
    budgets_qs = Budget.objects.filter(user=request.user)
    budgets = []
    for b in budgets_qs:
        spent = Transaction.objects.filter(user=request.user, category=b.category).aggregate(total=Sum('amount'))['total'] or 0
        remaining = float(b.amount) - float(spent)
        budgets.append({'budget': b, 'spent': spent, 'remaining': remaining})

    # Expense by Category
    expense_by_cat = Transaction.objects.filter(user=request.user, category__type='expense') \
        .values('category__name') \
        .annotate(total=Sum('amount'))

    expense_by_cat_list = [
        {"category__name": item['category__name'], "total": float(item['total'])}
        for item in expense_by_cat
    ]
    expense_by_cat_json = json.dumps(expense_by_cat_list)

    return render(request, "dashboard.html", {
        'income': float(income),
        'expense': float(expense),
        'balance': balance,
        'transactions': transactions,
        'budgets': budgets,
        'expense_by_cat': expense_by_cat_json
    })


@login_required
def add_transaction(request):
    if request.method == "POST":
        category_id = request.POST.get("category")
        amount = request.POST.get("amount")
        description = request.POST.get("description")

        if not category_id or not amount:
            messages.error(request, "Please fill all required fields")
            return redirect("add_transaction")

        category = Category.objects.get(id=category_id, user=request.user)
        Transaction.objects.create(
            user=request.user,
            category=category,
            amount=amount,
            description=description
        )
        messages.success(request, "Transaction added successfully!")
        return redirect("dashboard")

    categories = Category.objects.filter(user=request.user)
    return render(request, "add_transaction.html", {"categories": categories})


@login_required
def categories(request):
    if request.method == "POST":
        name = request.POST.get("name")
        type = request.POST.get("type")
        Category.objects.create(user=request.user, name=name, type=type)
        messages.success(request, "Category created!")
        return redirect("categories")

    cats = Category.objects.filter(user=request.user)
    return render(request, "categories.html", {"categories": cats})

from django.utils.timezone import now
from django.db.models import Sum
import datetime

@login_required
def add_budget(request):
    if request.method == "POST":
        category_id = request.POST.get("category")
        amount = request.POST.get("amount")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        category = Category.objects.get(id=category_id)
        Budget.objects.create(
            user=request.user,
            category=category,
            amount=amount,
            start_date=start_date,
            end_date=end_date
        )
        messages.success(request, "Budget added successfully!")
        return redirect("view_budgets")

    categories = Category.objects.filter(user=request.user, type="expense")
    return render(request, "add_budget.html", {"categories": categories})


@login_required
def view_budgets(request):
    budgets = Budget.objects.filter(user=request.user)
    data = []
    for b in budgets:
        spent = Transaction.objects.filter(
            user=request.user,
            category=b.category,
            date__range=[b.start_date, b.end_date]
        ).aggregate(total=Sum("amount"))["total"] or 0
        remaining = b.amount - spent
        data.append({"budget": b, "spent": spent, "remaining": remaining})
    return render(request, "view_budgets.html", {"data": data})


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
import json
from .models import Transaction

from django.db.models.functions import ExtractMonth, ExtractYear
from datetime import date

from datetime import date
from django.db.models.functions import ExtractMonth, ExtractYear

@login_required
def reports(request):
    today = date.today()
    month = int(request.GET.get('month', today.month))
    year = int(request.GET.get('year', today.year))

    # Transactions filtered by selected month/year
    transactions = Transaction.objects.filter(
        user=request.user,
        date__month=month,
        date__year=year
    )

    # Totals
    income = transactions.filter(category__type='income').aggregate(total=Sum('amount'))['total'] or 0
    expense = transactions.filter(category__type='expense').aggregate(total=Sum('amount'))['total'] or 0

    # Expense by Category
    expense_by_cat = transactions.filter(category__type='expense') \
        .values('category__name') \
        .annotate(total=Sum('amount'))

    expense_by_cat_list = [
        {"category__name": item['category__name'], "total": float(item['total'])}
        for item in expense_by_cat
    ]
    expense_by_cat_json = json.dumps(expense_by_cat_list)

    # Generate list of years from user transactions
    years = Transaction.objects.filter(user=request.user) \
        .annotate(y=ExtractYear('date')).values_list('y', flat=True).distinct().order_by('-y')

    # Month list for dropdown
    months = [
        {'num': 1, 'name': 'January'}, {'num': 2, 'name': 'February'},
        {'num': 3, 'name': 'March'}, {'num': 4, 'name': 'April'},
        {'num': 5, 'name': 'May'}, {'num': 6, 'name': 'June'},
        {'num': 7, 'name': 'July'}, {'num': 8, 'name': 'August'},
        {'num': 9, 'name': 'September'}, {'num': 10, 'name': 'October'},
        {'num': 11, 'name': 'November'}, {'num': 12, 'name': 'December'}
    ]

    return render(request, "reports.html", {
        'income': float(income),
        'expense': float(expense),
        'expense_by_cat': expense_by_cat_json,
        'selected_month': month,
        'selected_year': year,
        'years': years,
        'months': months
    })

@login_required
def edit_budget(request, pk):
    budget = Budget.objects.get(id=pk, user=request.user)

    if request.method == "POST":
        budget.amount = request.POST.get("amount")
        budget.start_date = request.POST.get("start_date")
        budget.end_date = request.POST.get("end_date")
        budget.save()
        messages.success(request, "Budget updated successfully!")
        return redirect("view_budgets")

    return render(request, "edit_budget.html", {"budget": budget})

@login_required
def delete_budget(request, pk):
    budget = Budget.objects.get(id=pk, user=request.user)
    budget.delete()
    messages.success(request, "Budget deleted successfully!")
    return redirect("view_budgets")

@login_required
def transactions(request):
    user_transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, "transactions.html", {"transactions": user_transactions})

@login_required
def edit_transaction(request, pk):
    transaction = Transaction.objects.get(id=pk, user=request.user)
    categories = Category.objects.filter(user=request.user)

    if request.method == "POST":
        category_id = request.POST.get("category")
        amount = request.POST.get("amount")
        description = request.POST.get("description")

        transaction.category = Category.objects.get(id=category_id, user=request.user)
        transaction.amount = amount
        transaction.description = description
        transaction.save()

        messages.success(request, "Transaction updated successfully!")
        return redirect("transactions")

    return render(request, "edit_transaction.html", {"transaction": transaction, "categories": categories})

@login_required
def delete_transaction(request, pk):
    transaction = Transaction.objects.get(id=pk, user=request.user)
    transaction.delete()
    messages.success(request, "Transaction deleted successfully!")
    return redirect("transactions")


from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm

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

def logout(request):
    auth_logout(request)
    return redirect('login')


from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

@login_required
def profile(request):
    user = request.user

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        # Update user details
        if username and email:
            user.username = username
            user.email = email
            user.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')

    # Optionally: fetch account stats
    income = Transaction.objects.filter(user=user, category__type='income').aggregate(total=Sum('amount'))['total'] or 0
    expense = Transaction.objects.filter(user=user, category__type='expense').aggregate(total=Sum('amount'))['total'] or 0
    balance = float(income) - float(expense)

    return render(request, 'profile.html', {
        'user': user,
        'income': income,
        'expense': expense,
        'balance': balance
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = Profile(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = Profile(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})
