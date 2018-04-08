from django.contrib.auth.models import Permission, User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.urlresolvers import reverse
from datetime import date


class Transaction(models.Model):
    user = models.ForeignKey(User, default=1)
    category_name = models.CharField(max_length=250)
    product_logo = models.FileField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.category_name


class Item(models.Model):
    user = models.ForeignKey(User, default=1)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=250)
    quantity = models.IntegerField(default="", validators=[MaxValueValidator(1000), MinValueValidator(1)])
    rate = models.IntegerField(default="", validators=[MaxValueValidator(1000), MinValueValidator(1)])
    total_cost = models.IntegerField(default="", validators=[MaxValueValidator(1000), MinValueValidator(1)])
    date = models.DateField(("Date"), default=date.today)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.product_name

    def __str__(self):
        return self.product_name


class Report(models.Model):
    generate = models.BooleanField(default=False)

    def __str__(self):
        return self.generate

