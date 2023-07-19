from django.contrib import admin
from . import models


class OrderItemAdmin(admin.TabularInline):
    model = models.CartItem


@admin.register(models.CartShop)
class OrderRegisterAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'is_paid')
    inlines = (OrderItemAdmin,)
    list_filter = ('is_paid',)


@admin.register(models.Diccount)
class DiscountRegisterAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount', 'quantity')

