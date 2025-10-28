from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
                              
def home(request):
    return render(request, 'index.html')

def connect_accounts(request):
    # Redirect to login/signup instead of Plaid
    return redirect('login')         

def login_view(request):    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def logout(request):
    return render(request, 'index.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def explore_demo(request):
    return render(request, 'demo.html')

from django.contrib.auth.decorators import login_required
from .models import Expense
from .forms import ExpenseForm
from django.db.models import Sum
import json
from datetime import datetime, timedelta

@login_required
def dashboard(request):
    # Last 30 days expenses
    date_threshold = datetime.now() - timedelta(days=30)
    expenses = Expense.objects.filter(
        user=request.user,
        date__gte=date_threshold
    ).order_by('-date')
    
    # Calculate totals
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Category breakdown for chart
    categories = dict(Expense.CATEGORY_CHOICES)
    category_data = expenses.values('category').annotate(total=Sum('amount'))
    
    chart_data = {
        'labels': [categories[item['category']] for item in category_data],
        'datasets': [{
            'data': [float(item['total']) for item in category_data],
            'backgroundColor': [
                '#4F46E5', '#10B981', '#F59E0B', 
                '#EF4444', '#8B5CF6', '#EC4899'
            ]
        }]
    }
    
    context = {
        'expenses': expenses,
        'total_expenses': total_expenses,
        'chart_data': json.dumps(chart_data),
        'form': ExpenseForm()
    }
    return render(request, 'dashboard.html', context)

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('dashboard')
    return redirect('dashboard')
