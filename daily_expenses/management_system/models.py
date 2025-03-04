from django.db import models

# Create your models here.


class Expenses(models.Model):
    # Date, Description, Credit, Debit & Running Balance
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=False, null=False)
    credits = models.IntegerField(default=0, blank=True, null=True)
    debit = models.IntegerField(default=0, blank=True, null=True)
    balance = models.IntegerField(default=0, blank=True, null=True)
