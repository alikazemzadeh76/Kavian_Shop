from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('product/<slug:slug>', views.ProductDetailView.as_view(), name='product_detail'),
    path('categories', views.CategoryPartialView.as_view(), name='categories'),
    path('all_product', views.AllProductView.as_view(), name='all_product'),
    path('search', views.SearchView.as_view(), name='search'),
    path('like/<slug:slug>/<int:pk>', views.like, name='like'),
    path('categoryquery/<slug:slug>', views.CategoryQueryView.as_view(), name='categoryquery'),

]