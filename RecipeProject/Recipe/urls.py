from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.recipes, name='recipes'),
    path('delete/<id>/', views.delete_recipe, name='delete_recipe'),
    path('update/<id>/', views.update_recipe, name='update_recipe'),
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register'),
    path('logout/', views.logout_page, name='logout_page'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
urlpatterns += staticfiles_urlpatterns()