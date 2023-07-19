from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt

from user_personalization.models import User
from .session_cart import Cart
from .models import CartShop, CartItem, Diccount
import requests
from product.models import Product


class CartView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, "cart/cart.html", {'cart': cart})


class CartAddView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        size = request.POST.get('size')
        color = request.POST.get('color')
        quantity = request.POST.get('quantity')
        cart = Cart(request)
        cart.add(product, color, size, quantity)
        return redirect("cart:cart_detail")



class CartRemoveView(View):
    def post(self, request, id):
        cart = Cart(request)
        cart.remove(id)
        return JsonResponse({'status': 'ok'})


class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = get_object_or_404(CartShop, id=pk)
        return render(request, 'cart/order_detail.html', {'order': order})


class OrderCreationView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = CartShop.objects.create(user=request.user, total_price=cart.total())
        for item in cart:
            CartItem.objects.create(cart=order, product=item['product'], color=item['color'], size=item['size'],
                                    quantity=item['quantity'], price=item['price'])

        cart.delete_cart()
        return redirect('cart:order_detail', order.id)


class DiscountCodeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(CartShop, id=pk)
        code = request.POST.get('discount')
        discount_code = get_object_or_404(Diccount, name=code)
        if discount_code.quantity == 0:
            return redirect("cart:order_detail", order.id)
        order.total_price -= order.total_price * discount_code.discount / 100
        order.save()
        discount_code.quantity -= 1
        discount_code.save()
        return redirect("cart:order_detail", order.id)


