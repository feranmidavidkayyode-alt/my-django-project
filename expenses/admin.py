from django.contrib import admin
from .models import Expense, Category

# 👤 Expense admin


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'amount', 'category', 'expense_date')
    list_filter = ('category', 'expense_date')
    search_fields = ('description', 'owner__username')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Category, CategoryAdmin)
