from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path('login', views.LoginFormView.as_view(), name='login'),
    path('logout', views.userlogout, name='logout'),
    path('signup', views.SignUpView.as_view(), name='signup'),
    path('register', views.PhoneRegisterView.as_view(), name='register'),
    path('confirm_code', views.ConfirmCodeView.as_view(), name='confirm_code'),
    path('address', views.AddressView.as_view(), name='address'),
    path('contact_us', views.ContactUsView.as_view(), name='contact_us'),
]