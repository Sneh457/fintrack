# myapp/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import dashboard, add_expense

urlpatterns = [
    path('', views.home, name='home'),
    path('demo/', views.explore_demo, name='explore_demo'),
    path('connect/', views.connect_accounts, name='connect_accounts'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('add-expense/', add_expense, name='add_expense'), 
]