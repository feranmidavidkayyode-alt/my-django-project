from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Expense(models.Model):
    # always use 'user' for consistency
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    expense_date = models.DateField(default=now)
