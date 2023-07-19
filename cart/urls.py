from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path('cart_detail', views.CartView.as_view(), name="cart_detail"),
    path('cart_add/<int:pk>', views.CartAddView.as_view(), name="cart_add"),
    path('cart_remove/<str:id>', views.CartRemoveView.as_view(), name="cart_remove"),
    path('order_detail/<int:pk>', views.OrderDetailView.as_view(), name="order_detail"),
    path('orderadd', views.OrderCreationView.as_view(), name="order_add"),
    path('discount/<int:pk>', views.DiscountCodeView.as_view(), name="discount"),
]