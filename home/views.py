from django.shortcuts import render
from django.views.generic import TemplateView
from product.models import Product, Category


class Home(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data()
        context['products'] = Product.objects.all()
        context['recent_products'] = Product.objects.all().order_by('-created')[:4]
        context['categories'] = Category.objects.all()
        context['discount'] = Product.objects.filter(discount__gt=0)[:2]

        return context