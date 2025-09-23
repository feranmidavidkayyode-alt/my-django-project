from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import datetime, date, timedelta
import json

from .models import Income


@login_required(login_url='/authentication/login')
def income_list(request):
    incomes = Income.objects.filter(owner=request.user)
    paginator = Paginator(incomes, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'income/index.html', {'page_obj': page_obj})


@login_required(login_url='/authentication/login')
def add_income(request):
    if request.method == 'GET':
        return render(request, 'income/add_income.html')

    amount = request.POST.get('amount')
    date_str = request.POST.get('income_date')
    category = request.POST.get('category')
    description = request.POST.get('description')

    if not amount:
        messages.error(request, 'Amount is required')
        return render(request, 'income/add_income.html')
    if not date_str:
        messages.error(request, 'Date is required')
        return render(request, 'income/add_income.html')

    try:
        amount_value = float(amount)
        income_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        messages.error(request, 'Invalid amount or date format')
        return render(request, 'income/add_income.html')

    Income.objects.create(
        owner=request.user,
        amount=amount_value,
        date=income_date,
        category=category,
        description=description
    )
    messages.success(request, 'Income added successfully')
    return redirect('income-list')


@login_required(login_url='/authentication/login')
def edit_income(request, id):
    income = get_object_or_404(Income, pk=id)

    if request.method == 'GET':
        return render(request, 'income/edit_income.html', {'income': income})

    amount = request.POST.get('amount')
    date_str = request.POST.get('income_date')
    category = request.POST.get('category')
    description = request.POST.get('description')

    income.amount = float(amount)
    income.date = datetime.strptime(date_str, "%Y-%m-%d").date()
    income.category = category
    income.description = description
    income.save()

    messages.success(request, 'Income updated successfully')
    return redirect('income-list')


@login_required(login_url='/authentication/login')
def delete_income(request, id):
    income = get_object_or_404(Income, pk=id)
    income.delete()
    messages.success(request, 'Income deleted successfully')
    return redirect('income-list')


@login_required(login_url='/authentication/login')
def income_summary_api(request):
    """Return income summary by category for chart.js"""
    six_months_ago = date.today() - timedelta(days=30 * 6)
    incomes = Income.objects.filter(
        owner=request.user, date__gte=six_months_ago)

    summary = {}
    for income in incomes:
        summary[income.category] = summary.get(
            income.category, 0) + income.amount

    return JsonResponse(summary, safe=False)
