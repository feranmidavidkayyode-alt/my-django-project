from datetime import datetime, date, timedelta
import json
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import Category, Expense
from income.models import Income
from userpreferences.models import UserPreference


# 🔎 AJAX: Search Expenses
def search_expenses(request: HttpRequest) -> JsonResponse:
    """Search expenses by amount, date, description, or category."""
    if request.method == "POST":
        search_str = json.loads(request.body).get("searchText", "")
        expenses = (
            Expense.objects.filter(amount__startswith=search_str, user=request.user) |
            Expense.objects.filter(expense_date__startswith=search_str, user=request.user) |
            Expense.objects.filter(description__icontains=search_str, user=request.user) |
            Expense.objects.filter(
                category__name__icontains=search_str, user=request.user)
        )
        return JsonResponse(list(expenses.values()), safe=False)
    return JsonResponse([], safe=False)


# 🏠 Dashboard / Index
@login_required(login_url="/authentication/login")
def index(request: HttpRequest) -> HttpResponse:
    expenses = Expense.objects.filter(
        user=request.user).order_by("-expense_date")

    paginator = Paginator(expenses, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    user_preference, _ = UserPreference.objects.get_or_create(
        user=request.user, defaults={"currency": "USD"}
    )

    context = {
        "expenses": expenses,
        "page_obj": page_obj,
        "currency": user_preference.currency,
    }
    return render(request, "expenses/index.html", context)


# ➕ Add Expense
@login_required(login_url="/authentication/login")
def add_expense(request: HttpRequest) -> HttpResponse:
    categories = Category.objects.all()
    if request.method == "POST":
        amount_str = request.POST.get("amount") or ""
        description = request.POST.get("description") or ""
        date_str = request.POST.get("date") or ""
        category_name = request.POST.get("category") or ""

        try:
            amount_value = Decimal(amount_str)
        except Exception:
            messages.error(request, "Invalid amount")
            return render(request, "expenses/add_expense.html", {"categories": categories})

        if not description.strip():
            messages.error(request, "Description is required")
            return render(request, "expenses/add_expense.html", {"categories": categories})

        try:
            expense_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Invalid date format")
            return render(request, "expenses/add_expense.html", {"categories": categories})

        # Get Category instance
        try:
            category_obj = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            messages.error(request, "Selected category does not exist")
            return render(request, "expenses/add_expense.html", {"categories": categories})

        Expense.objects.create(
            user=request.user,
            amount=amount_value,
            description=description,
            expense_date=expense_date,
            category=category_obj,
        )

        messages.success(request, "Expense saved successfully")
        return redirect("expenses")

    return render(request, "expenses/add_expense.html", {"categories": categories})


# ✏️ Edit Expense
@login_required(login_url="/authentication/login")
def edit_expense(request: HttpRequest, pk: int) -> HttpResponse:
    expense = get_object_or_404(Expense, id=pk, user=request.user)
    categories = Category.objects.all()

    if request.method == "POST":
        amount_str = request.POST.get("amount") or ""
        description = request.POST.get("description") or ""
        date_str = request.POST.get("date") or ""
        category_name = request.POST.get("category") or ""

        try:
            expense.amount = Decimal(amount_str)
        except Exception:
            messages.error(request, "Invalid amount")
            return render(request, "expenses/edit_expense.html", {"expense": expense, "categories": categories})

        if not description.strip():
            messages.error(request, "Description is required")
            return render(request, "expenses/edit_expense.html", {"expense": expense, "categories": categories})
        expense.description = description

        try:
            expense.expense_date = datetime.strptime(
                date_str, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Invalid date format")
            return render(request, "expenses/edit_expense.html", {"expense": expense, "categories": categories})

        if category_name:
            try:
                category_obj = Category.objects.get(name=category_name)
                expense.category = category_obj
            except Category.DoesNotExist:
                messages.error(request, "Selected category does not exist")
                return render(request, "expenses/edit_expense.html", {"expense": expense, "categories": categories})

        expense.save()
        messages.success(request, "Expense updated successfully")
        return redirect("expenses")

    return render(request, "expenses/edit_expense.html", {"expense": expense, "categories": categories})


# ❌ Delete Expense
@login_required(login_url="/authentication/login")
def delete_expense(request: HttpRequest, pk: int) -> HttpResponse:
    expense = get_object_or_404(Expense, id=pk, user=request.user)
    expense.delete()
    messages.success(request, "Expense removed successfully")
    return redirect("expenses")


# 📊 Expense Category Summary (JSON for charts)
@login_required(login_url="/authentication/login")
def expense_category_summary(request: HttpRequest) -> JsonResponse:
    today = date.today()
    six_months_ago = today - timedelta(days=30 * 6)

    expenses = Expense.objects.filter(
        user=request.user, expense_date__gte=six_months_ago, expense_date__lte=today)

    summary = {}
    for category in Category.objects.all():
        total = expenses.filter(category=category).aggregate(
            total=Sum("amount"))["total"] or 0
        if total > 0:
            summary[category.name] = float(total)

    return JsonResponse({"expense_category_data": summary}, safe=False)


# 📈 Stats View
@login_required(login_url="/authentication/login")
def stats_view(request: HttpRequest) -> HttpResponse:
    return render(request, "expenses/stats.html")


# 📊 Summary View
@login_required(login_url="/authentication/login")
def summary_view(request: HttpRequest) -> HttpResponse:
    expenses = Expense.objects.filter(user=request.user)
    incomes = Income.objects.filter(user=request.user)

    total_expenses = expenses.aggregate(total=Sum("amount"))[
        "total"] or Decimal("0.00")
    total_income = incomes.aggregate(total=Sum("amount"))[
        "total"] or Decimal("0.00")
    balance = total_income - total_expenses

    category_summary = expenses.values(
        "category__name").annotate(total=Sum("amount"))

    categories = [item["category__name"] for item in category_summary]
    amounts = [float(item["total"]) for item in category_summary]

    context = {
        "total_expenses": float(total_expenses),
        "total_income": float(total_income),
        "balance": float(balance),
        "categories_json": json.dumps(categories),
        "amounts_json": json.dumps(amounts),
    }
    return render(request, "expenses/summary.html", context)
