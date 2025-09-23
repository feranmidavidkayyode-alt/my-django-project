# userincome/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpRequest, HttpResponse
from decimal import Decimal
import json

from .models import Source, UserIncome
from .forms import UserIncomeForm
from userpreferences.models import UserPreference

# for chart aggregation
from django.db.models.functions import TruncMonth
from django.db.models import Sum


@login_required(login_url='/authentication/login/')
def index(request: HttpRequest) -> HttpResponse:
    """
    List incomes, show paginated table and Chart.js data.
    """
    incomes_qs = UserIncome.objects.filter(
        owner=request.user).order_by('-date')
    paginator = Paginator(incomes_qs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user_pref, _ = UserPreference.objects.get_or_create(
        user=request.user, defaults={'currency': 'USD'}
    )

    # monthly aggregation for Chart.js
    monthly = (
        incomes_qs
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )
    labels = [entry['month'].strftime("%b %Y") for entry in monthly]
    data = [float(entry['total']) for entry in monthly]

    context = {
        'incomes': incomes_qs,
        'page_obj': page_obj,
        'currency': user_pref.currency,
        'chart_labels': labels,
        'chart_data': data,
    }
    return render(request, 'income/index.html', context)


@login_required(login_url='/authentication/login/')
def add_income(request: HttpRequest) -> HttpResponse:
    """
    Add a new income entry using UserIncomeForm.
    """
    if request.method == "POST":
        form = UserIncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.owner = request.user
            income.save()
            messages.success(request, "Record saved successfully")
            return redirect('income')
    else:
        form = UserIncomeForm()

    return render(request, 'income/add_income.html', {'form': form})


@login_required(login_url='/authentication/login/')
def income_edit(request: HttpRequest, id: int) -> HttpResponse:
    """
    Edit an existing income entry.
    """
    income = get_object_or_404(UserIncome, pk=id, owner=request.user)
    if request.method == "POST":
        form = UserIncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            messages.success(request, "Record updated successfully")
            return redirect('income')
    else:
        form = UserIncomeForm(instance=income)

    return render(request, 'income/edit_income.html', {'form': form, 'income': income})


@login_required(login_url='/authentication/login/')
def delete_income(request: HttpRequest, id: int) -> HttpResponse:
    income = get_object_or_404(UserIncome, pk=id, owner=request.user)
    income.delete()
    messages.success(request, "Record removed")
    return redirect('income')


@login_required(login_url='/authentication/login/')
def search_income(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText', '')
        qs = (
            UserIncome.objects.filter(amount__istartswith=search_str, owner=request.user) |
            UserIncome.objects.filter(date__istartswith=search_str, owner=request.user) |
            UserIncome.objects.filter(description__icontains=search_str, owner=request.user) |
            UserIncome.objects.filter(
                source__icontains=search_str, owner=request.user)
        )
        return JsonResponse(list(qs.values()), safe=False)
    return JsonResponse({'error': 'invalid method'}, status=400)
