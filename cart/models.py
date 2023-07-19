from django.db import models

from account.models import Address
from product.models import Product
from user_personalization.models import User


class CartShop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_cart", verbose_name="کاربر")
    name = models.CharField(max_length=50, verbose_name="نام و نام خانوادگی")
    total_price = models.IntegerField(verbose_name="مبلغ کل")
    is_paid = models.BooleanField(default=False, verbose_name="وضعیت پرداخت")

    def __str__(self):
        return self.user.full_name

    def get_total_items(self):
        return sum(items.quantity for items in self.item.all())

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"


class CartItem(models.Model):
    cart = models.ForeignKey(CartShop, on_delete=models.CASCADE, related_name="item", verbose_name="سفارش")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="item", verbose_name="محصول")
    color = models.CharField(null=True, blank=True, max_length=20, verbose_name="رنگ")
    size = models.CharField(null=True, blank=True, max_length=5, verbose_name="سایز")
    price = models.PositiveIntegerField(verbose_name="مبلغ")
    quantity = models.PositiveIntegerField(verbose_name="تعداد")

    def __str__(self):
        return self.cart.name

    class Meta:
        verbose_name = "محصول ثبت شده"
        verbose_name_plural = "محصولات ثبت شده"


class Diccount(models.Model):
    name = models.CharField(max_length=20)
    discount = models.SmallIntegerField(default=0)
    quantity = models.SmallIntegerField(default=1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "کد تخفیف"
        verbose_name_plural = "کد های تخفیف"