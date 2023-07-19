from django.db import models

from user_personalization.models import User


class Register(models.Model):
    token = models.CharField(max_length=100, null=True, verbose_name="توکن")
    phone = models.CharField(max_length=11, verbose_name="شماره تلفن")
    code = models.IntegerField(verbose_name="کد دریافتی")
    expirtion_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = "رجیستر"
        verbose_name_plural = "رجیستر ها"


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='address', verbose_name="کاربر")
    fullname = models.CharField(max_length=50, verbose_name="نام و نام خانوادگی")
    phone = models.CharField(max_length=12, verbose_name="شماره تلفن")
    address = models.TextField(verbose_name="آدرس کامل")

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس ها"


class ContactUs(models.Model):
    full_name = models.CharField(max_length=30, verbose_name="نام و نام خانوادگی")
    email = models.EmailField(verbose_name="آدرس ایمیل")
    subject = models.CharField(max_length=50, verbose_name="عنوان")
    text = models.TextField(verbose_name="متن پیام")

    class Meta:
        verbose_name = "پیام دریافتی"
        verbose_name_plural = "پیام های دریافتی"

    def __str__(self):
        return self.subject

