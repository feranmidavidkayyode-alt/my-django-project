# userincome/forms.py
from django import forms
from .models import UserIncome
from django.utils import timezone
from decimal import Decimal, InvalidOperation


class UserIncomeForm(forms.ModelForm):
    class Meta:
        model = UserIncome
        fields = ['amount', 'date', 'description', 'source']
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"})
        }

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        if amount is None:
            raise forms.ValidationError("Amount is required.")
        try:
            # If using DecimalField, amount will already be Decimal
            val = Decimal(str(amount))
        except (InvalidOperation, TypeError):
            raise forms.ValidationError("Enter a valid number for amount.")
        if val <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return val

    def clean_date(self):
        date = self.cleaned_data.get("date")
        if date and date > timezone.now().date():
            raise forms.ValidationError("Date cannot be in the future.")
        return date
