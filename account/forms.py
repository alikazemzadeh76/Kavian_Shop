from django import forms
from django.forms import ValidationError
from user_personalization.models import User
from django.contrib.auth import authenticate
from .models import Register, Address, ContactUs


class LoginForm(forms.Form):
    phone = forms.CharField(max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره تلفن یا ایمیل'}))
    password = forms.CharField(max_length=20,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور'}))

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        valid_numbers = str(list(range(900, 999)))

        if phone[1:4] not in valid_numbers:
            raise ValidationError("شماره وارد شده نامعتبر است", code="invalid")

        if len(phone) != 11:
            raise ValidationError(
                f"شماره تلفن وارد شده نباید کمتر یا بیشتر از 11 کاراکتر باشد.شما {len(phone)} کاراکتر وارد کردید.",
                code="invalid_phone")

        # بررسی اینکه تمامی کاراکترهای ورودی، اعدادی هستند
        if not all(char.isdigit() for char in phone):
            raise forms.ValidationError('شماره تلفن باید شامل اعداد باشد.')

        # بررسی اینکه شماره تلفن، یازده رقمی باشد
        if len(phone) != 11:
            raise forms.ValidationError('شماره تلفن باید یازده رقمی باشد.')

        # بررسی اینکه شماره تلفن با صفر آغاز می‌شود
        if phone[0] != '0':
            raise forms.ValidationError('شماره تلفن باید با صفر آغاز شود.')

        return phone

    def clean_password(self):
        password = self.cleaned_data.get('password')
        phone = self.cleaned_data.get('phone')
        user = authenticate(username=phone, password=password)
        if user is None:
             raise ValidationError("رمز عبور اشتباه است", code="invalid_password")

        return password


class SignUpForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': 'تکرار رمز عبور'}))
    class Meta:
        model = User
        fields = ('phone', 'full_name', 'email', 'password')
        widgets = {
            'full_name': forms.TextInput(attrs={'class': "form-control", 'placeholder': 'نام و نام خانوادگی'}),
            'email': forms.EmailInput(attrs={'class': "form-control", 'placeholder': 'ایمیل'}),
            'password': forms.PasswordInput(attrs={'class': "form-control", 'placeholder': 'رمز عبور'})
        }


    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if len(password) < 8:
            raise ValidationError("رمز عبور نباید کمتر از 8 کاراکتر باشد", code="invalid_password")


        return password2


class RegisterForm(forms.Form):
    phone = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره تلفن'}))

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        valid_numbers = str(list(range(900, 999)))

        if User.objects.filter(phone=phone).exists():
            raise ValidationError("شماره تلفن تکراری است", code="phone_invalid")

        if phone[1:4] not in valid_numbers:
            raise ValidationError("شماره وارد شده نامعتبر است", code="invalid")

        if len(phone) != 11:
            raise ValidationError(
                f"شماره تلفن وارد شده نباید کمتر یا بیشتر از 11 کاراکتر باشد.شما {len(phone)} کاراکتر وارد کردید.",
                code="invalid_phone")

        # بررسی اینکه تمامی کاراکترهای ورودی، اعدادی هستند
        if not all(char.isdigit() for char in phone):
            raise forms.ValidationError('شماره تلفن باید شامل اعداد باشد.')

        # بررسی اینکه شماره تلفن، یازده رقمی باشد
        if len(phone) != 11:
            raise forms.ValidationError('شماره تلفن باید یازده رقمی باشد.')

        # بررسی اینکه شماره تلفن با صفر آغاز می‌شود
        if phone[0] != '0':
            raise forms.ValidationError('شماره تلفن باید با صفر آغاز شود.')

        return phone

class ConfirmCodeForm(forms.Form):
    code = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کد تایید'}))

    def clean_code(self):
        code = self.cleaned_data.get('code')
        queryset = Register.objects.filter(code=code)
        if not queryset.exists():
            raise ValidationError("کد وارد شده صحیح نمی‌باشد")
        return code

class AddressForm(forms.ModelForm):
    user = forms.IntegerField(required=False)
    class Meta:
        model = Address
        fields = "__all__"
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام و نام خانوادگی'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره تلفن'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'آدرس کامل'}),
        }


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = "__all__"
        widgets = {
            "full_name": forms.TextInput(attrs={'id': 'full_name', 'class': 'form-control', 'placeholder': 'نام و نام خانوادگی'}),
            "email": forms.EmailInput(attrs={'id': 'email', 'class': 'form-control', 'placeholder': 'آدرس ایمیل'}),
            "subject": forms.TextInput(attrs={'id': 'subject', 'class': 'form-control', 'placeholder': 'عنوان'}),
            "text": forms.Textarea(attrs={'id': 'text', 'class': 'form-control', 'placeholder': 'متن پیام'}),
        }


