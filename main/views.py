from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView

from .models import Category, Product


class HomeView(TemplateView):
    template_name = 'main/index.html'
    


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'main/page-category.html'
    context_object_name = 'category'
    slug_url_kwarg = 'slug'
    


class ProductListView(ListView):
    model = Product
    template_name = 'main/page-listing-grid.html'
    context_object_name = 'products'
    paginate_by = 12
     


class ProductListLargeView(ProductListView):
    template_name = 'main/page-listing-large.html'
    paginate_by = 10



class ProductDetailView(DetailView):
    model = Product
    template_name = 'main/page-detail-product.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'
    


class ContentView(TemplateView):
    template_name = 'main/page-content.html'
    


class SearchView(ListView):
    model = Product
    template_name = 'main/page-listing-grid.html'
    context_object_name = 'products'
    paginate_by = 12
    