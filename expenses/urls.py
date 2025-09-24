from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="expenses"),
    path("add/", views.add_expense, name="expense-add"),
    path("edit/<int:pk>/", views.edit_expense, name="expense-edit"),
    path("delete/<int:pk>/", views.delete_expense, name="expense-delete"),
    path("search/", views.search_expenses, name="expense-search"),
    path("summary/", views.summary_view, name="summary"),
    path("stats/", views.stats_view, name="stats"),
    path("category-summary/", views.expense_category_summary,
         name="expense-category-summary"),
    path("add-expense/", views.add_expense, name="add_expense"),

]
