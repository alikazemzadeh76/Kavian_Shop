from slugify import slugify
from jdatetime import datetime as jdatetime
from django.db import models
from django.utils.html import format_html

from django.urls import reverse
from user_personalization.models import User


class Information(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True, related_name="informations", verbose_name="محصول")
    text = models.CharField(max_length=150, verbose_name="عنوان")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name="عنوان")
    image = models.ImageField(upload_to="category_images", null=True, verbose_name="تصویر")
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='sub', verbose_name='زیر مجموعه')
    slug = models.SlugField(null=True, blank=True, unique=True, verbose_name="عنوان صفحه")
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    def __str__(self):
        return self.title
    def shamsidate(self):
        gdate = self.created.date()
        jdate = jdatetime.fromgregorian(date=gdate)
        return jdate.strftime('%Y/%m/%d')

    shamsidate.short_description = "تاریخ ایجاد"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

class Color(models.Model):
    color = models.CharField(max_length=20, verbose_name="رنگ")

    def __str__(self):
        return self.color

    class Meta:
        verbose_name = "رنگ"
        verbose_name_plural = "رنگ ها"

class Size(models.Model):
    size = models.CharField(max_length=15, verbose_name="سایز")

    def __str__(self):
        return self.size

    class Meta:
        verbose_name = "سایز"
        verbose_name_plural = "سایز ها"

class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name="نام محصول")
    image = models.ImageField(upload_to="product_images", verbose_name="تصویر")
    price = models.SmallIntegerField(verbose_name="قیمت")
    discount = models.SmallIntegerField(verbose_name="درصد تخفیف")
    description = models.TextField(verbose_name="توضیحات محصول")
    color = models.ManyToManyField(Color, blank=True, related_name="product", verbose_name="رنگ")
    size = models.ManyToManyField(Size, blank=True, related_name="product", verbose_name="سایز")
    category = models.ManyToManyField(Category, related_name='categories', verbose_name="دسته بندی")
    slug = models.SlugField(unique=True, verbose_name="عنوان صفحه")
    created = models.DateTimeField(auto_now=True, verbose_name="تاریخ ایجاد")

    def shamsidate(self):
        gdate = self.created.date()
        jdate = jdatetime.fromgregorian(date=gdate)
        return jdate.strftime('%Y/%m/%d')

    shamsidate.short_description = "تاریخ ایجاد"

    def show_image(self):
        if self.image:
            return format_html(f'<img src="{self.image.url}" width="60px" height="50px">')
        return ('<h2 style="container: revert">این محصول تصویر ندارد</h2>')

    show_image.short_description = 'تصویر'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name="محصول")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name="کاربر")
    text = models.CharField( max_length=100, verbose_name="کامنت")
    email = models.EmailField(verbose_name="ایمیل")
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    status = models.BooleanField(default=False, verbose_name="تایید کامنت")

    def shamsidate(self):
        date = self.created.date()
        persiantime = jdatetime.fromgregorian(date=date)
        return persiantime.strftime('%Y/%m/%d')

    shamsidate.short_description = 'تاریخ ایجاد'


    class Meta:
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت ها"

    def __str__(self):
        return self.user.full_name

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes", verbose_name="کاربر")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="likes", verbose_name="محصول")

    def __str__(self):
        return f'{self.user} - {self.product}'

    class Meta:
        verbose_name = "لایک"
        verbose_name_plural = "لایک ها"
