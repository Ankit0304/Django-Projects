from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('transactions/', views.transactions, name='transactions'),
    path("transaction/edit/<int:pk>/", views.edit_transaction, name="edit_transaction"),
    path("transaction/delete/<int:pk>/", views.delete_transaction, name="delete_transaction"),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    path("transaction/add/", views.add_transaction, name="add_transaction"),
    path("categories/", views.categories, name="categories"),
     # Budgets
    path("budget/add/", views.add_budget, name="add_budget"),
    path("budgets/", views.view_budgets, name="view_budgets"),
    path("budget/edit/<int:pk>/", views.edit_budget, name="edit_budget"),
    path("budget/delete/<int:pk>/", views.delete_budget, name="delete_budget"),

    # Reports
    path("reports/", views.reports, name="reports"),
    
    path('password_change/', 
         auth_views.PasswordChangeView.as_view(template_name='change_password.html'), 
         name='password_change'),
    path('password_change/done/', 
         auth_views.PasswordChangeDoneView.as_view(template_name='change_password_done.html'), 
         name='password_change_done'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)