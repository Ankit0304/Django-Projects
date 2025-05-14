from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    TYPE_CHOICE = [('Income', 'Income'), ('Expense', 'Expense')]
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TYPE_CHOICE, default='Expense')

    def __str__(self):
        return self.name

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True)
    type = models.CharField(max_length=10, choices=[('Income', 'Income'), ('Expense', 'Expense')], default='Expense')
    
    def __str__(self):
        return f"{self.type} : {self.amount}"
    
    