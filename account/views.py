from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import View, FormView
from .forms import LoginForm, SignUpForm, RegisterForm, ConfirmCodeForm, AddressForm, ContactUsForm
from user_personalization.models import User
from django.contrib.auth import login, authenticate, logout
from ghasedakpack import Ghasedak
from django.contrib import messages
from random import randint
from .models import Register
from uuid import uuid4
import time

SMS = Ghasedak("6a053b7aabc10ecb15f53dd0e6e7f6419de45d6c7d514065f4dcd3b1ed341b4a")


class LoginFormView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "account/login.html", {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['phone'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                form.add_error('phone', 'invalid')
        else:
            form.add_error('password', 'invalid')
        return render(request, "account/login.html", context={'form': form})


def userlogout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('home')


class PhoneRegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "account/register.html", {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            code = randint(1000, 9999)
            cd = form.cleaned_data
            SMS.verification({'receptor': cd['phone'], 'type': '1', 'template': 'kavianshop', 'param1': code})
            token = str(uuid4())
            Register.objects.create(phone=cd['phone'], code=code, token=token)
            print(code)
            return redirect(reverse_lazy("account:confirm_code") + f"?token={token}")

        return render(request, "account/register.html", {'form': form})


class ConfirmCodeView(View):
    def get(self, request):
        form = ConfirmCodeForm()
        return render(request, "account/confirm_code.html", {'form': form})

    def post(self, request):
        token = request.GET.get('token')
        form = ConfirmCodeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if Register.objects.filter(code=cd['code'], token=token).exists():
                user_phone = Register.objects.get(token=token)
                user = User.objects.create_user(phone=user_phone.phone, email=None)
                time.sleep(60)
                Register.objects.filter(token=token).delete()
                if cd['code']:
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect(reverse_lazy("account:signup"))

        return render(request, "account/confirm_code.html", {'form': form})


class SignUpView(View):
    def get(self, request):
        user = request.user
        form = SignUpForm(instance=user)
        return render(request, "account/signup.html", {'form': form})

    def post(self, request):
        user = request.user
        if request.user.is_authenticated:
            form = SignUpForm(request.POST, instance=user)
            if form.is_valid():
                password = form.cleaned_data.get('password')
                user.set_password(password)
                user.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect("home")

            return render(request, "account/signup.html", {'form': form})


class AddressView(View):
    def get(self, request):
        form = AddressForm()

        return render(request, "account/check_out.html", {'form': form})

    def post(self, request):
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)

            return redirect("account:address")
        return render(request, "account/check_out.html", {'form': form})


class ContactUsView(View):
    def get(self, request):
        form = ContactUsForm()
        return render(request, 'account/contact.html', {'form': form})

    def post(self, request):
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()

        return render(request, 'account/contact.html', {'form': form})

