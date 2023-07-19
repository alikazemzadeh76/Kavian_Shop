from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class MyUserManager(BaseUserManager):

    def create_user(self, phone, email, password=None, full_name=None):
        if not phone:
            raise ValueError("شماره خود را وارد کنید")
        email = self.normalize_email(email)
        user = self.model(phone=phone, email=email, full_name=full_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, email=None):
        user = self.create_user(phone=phone, password=password, email=email)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    full_name = models.CharField(max_length=50, null=True, verbose_name="نام و نام خانوادگی")
    phone = models.CharField(null=True, max_length=50, unique=True, verbose_name='شماره تلفن')
    email = models.EmailField(null=True, blank=True, max_length=255, verbose_name="آدرس ایمیل")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    is_admin = models.BooleanField(default=False, verbose_name="ادمین")

    objects = MyUserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.phone:
            return self.phone
        else:
            return ''

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربر ها"
