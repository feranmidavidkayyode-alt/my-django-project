from django.db import models
from django.contrib.auth.models import User


class Income(models.Model):
    CATEGORY_CHOICES = [
        ('SALARY', 'Salary'),
        ('BUSINESS', 'Business'),
        ('INVESTMENT', 'Investment'),
        ('SIDE_HUSTLE', 'Side Hustle'),
        ('OTHER', 'Other'),
    ]

    amount = models.FloatField()
    date = models.DateField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.category}: {self.amount}"
