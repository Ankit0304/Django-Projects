from django.shortcuts import render, redirect
from django.http import HttpResponse 
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.
def recipes(request):
    if request.method == 'POST':
        data = request.POST
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')
        recipe_image = request.FILES.get('recipe_image')
        # print(f"Recipe Name: {recipe_name} and Description: {recipe_description}")
        # print(f"Recipe Image: {recipe_image}")
        Recipe.objects.create(
            recipe_name=recipe_name,
            recipe_description=recipe_description,
            recipe_image=recipe_image
        )
        
        return redirect('recipes')
    
    queryset = Recipe.objects.all()
    
    if request.GET.get('search'):
        queryset = queryset.filter(recipe_name__icontains=request.GET.get('search'))
        
    context = {
        'recipes': queryset
    }
    
    return render(request, 'recipes.html', context)

def delete_recipe(request, id):
    queryset = Recipe.objects.filter(id=id)
    queryset.delete()
    # return HttpResponse(f"Delete recipe with id: {id}")
    return redirect('recipes')

def update_recipe(request, id):
    queryset = Recipe.objects.get(id=id)
    if request.method == 'POST':
        data = request.POST
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')
        recipe_image = request.FILES.get('recipe_image')
        
        queryset.recipe_name = recipe_name
        queryset.recipe_description = recipe_description
        
        if recipe_image:
            queryset.recipe_image = recipe_image
        queryset.save()
        return redirect('recipes')
         
    context = {'recipe': queryset}
    
    return render(request, 'update_recipe.html', context)
    

def login_page(request):
    return render(request, 'login.html')

def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')
        
        if password != confirm_password:
            return render(request, 'register.html', {'error': "Passwords do not match."})

        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': "Email already in use."})

        user = User.objects.create_user(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save()
        messages.success(request, "Account created successfully! Please log in.")
        return redirect('/login/')
        
    return render(request, 'register.html')
