from django.contrib.auth.models import User
from django import forms
from .models import Transaction, Item


class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ['category_name','product_logo']


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ['product_name','quantity','rate','total_cost','date']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','email','password']