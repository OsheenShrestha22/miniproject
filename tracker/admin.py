from django.contrib import admin
from .models import Transaction,Item, Report
from django.contrib.auth.models import Group
from django.contrib.auth.models import User


class ItemModelAdmin(admin.ModelAdmin):
    list_display = ["product_name","date"]

    class Meta:
        model = Item


admin.site.register(Item,ItemModelAdmin)
admin.site.register(Report)
admin.site.unregister(Group)
admin.site.unregister(User)
