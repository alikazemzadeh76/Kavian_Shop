from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView, TemplateView, ListView
from django.core.paginator import Paginator
from cart.models import CartShop
from cart.session_cart import Cart
from .models import Product, Category, Comment, Size, Like


class ProductDetailView(DetailView):
    model = Product
    template_name = "product/product_detail.html"
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.request.user.is_authenticated:
            if self.request.user.likes.filter(product__slug=self.object.slug, product_id=self.request.user.id).exists():
                context['is_like'] = True
            else:
                context['is_like'] = False
        return context

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        text = request.POST.get('text')
        email = request.POST.get('email')
        Comment.objects.create(user=request.user, product=product, text=text, email=email)


        return redirect('product:product_detail', slug=product.slug)


class CategoryPartialView(TemplateView):
    template_name = "includes/navbar.html"

    def get_context_data(self, **kwargs):
        context = super(CategoryPartialView, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['products'] = Product.objects.all()
        return context


class AllProductView(ListView):
    model = Product
    template_name = "product/all_product.html"
    context_object_name = 'product'
    paginate_by = 9

    def get(self, request, **kwargs):
        product = Product.objects.all()
        if request.GET.get('all_price'):
            products = product
        elif request.GET.get('price1'):
            products = product.filter(price__lte=500000)
        elif request.GET.get('price2'):
            products = product.filter(price__gt=500000, price__lte=1000000)
        elif request.GET.get('price3'):
            products = product.filter(price__gt=1000000, price__lte=5000000)
        elif request.GET.get('price4'):
            products = product.filter(price__gt=5000000, price__lte=10000000)
        elif request.GET.get('price5'):
            products = product.filter(price__gt=10000000, price__lte=20000000)
        elif request.GET.get('price6'):
            products = product.filter(price__gt=20000000)
        else:
            products = product

        self.object_list = products
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_object_name] = self.object_list
        return context


class CategoryQueryView(ListView):
    model = Product
    template_name = "product/all_product.html"
    context_object_name = 'categories'
    paginate_by = 6

    def get_queryset(self):
        slug = self.kwargs['slug']
        category = get_object_or_404(Category, slug=slug)
        product = Product.objects.filter(category=category)
        return product

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        context['category'] = get_object_or_404(Category, slug=slug)
        paginator = Paginator(context['categories'], self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['product'] = page_obj

        return context


class SearchView(ListView):
    model = Product
    template_name = 'product/all_product.html'
    context_object_name = 'product'
    paginate_by = 6

    def get_queryset(self):
        query = self.request.GET.get('q')
        return self.model.objects.filter(name__icontains=query)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchView, self).get_context_data()
        paginator = Paginator(context['product'], self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['product'] = page_obj

        return context

def like(request, slug, pk):
    try:
        like = Like.objects.get(product__slug=slug, user_id=request.user.id)
        like.delete()
        return JsonResponse({'response': 'unliked'})
    except:
        Like.objects.create(product_id=pk, user_id=request.user.id)
        return JsonResponse({'response': 'liked'})

    # return redirect("product:product_detail", slug)
