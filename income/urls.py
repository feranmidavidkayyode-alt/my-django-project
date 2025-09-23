from django.urls import path
from . import views

urlpatterns = [
    path('', views.income_list, name='income-list'),
    path('add/', views.add_income, name='add-income'),
    path('edit/<int:id>/', views.edit_income, name='edit-income'),
    path('delete/<int:id>/', views.delete_income, name='delete-income'),
    path('summary/', views.income_summary_api, name='income-summary'),
]
