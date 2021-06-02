from django.contrib import admin
from .models import Order,Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display=("id","name","amount","available")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=("id","customer","item")
