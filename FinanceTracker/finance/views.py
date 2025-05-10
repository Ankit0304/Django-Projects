from django.shortcuts import render
from .forms import RegisterForm
# Create your views here.


def home(request):
    return render(request, 'base.html')
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