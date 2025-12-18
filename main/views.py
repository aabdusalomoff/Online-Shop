from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q

from .models import Category, ProductCategory, Country, Product, ProductImage, Service


class IndexView(TemplateView):
    template_name = 'main/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        context['services'] = Service.objects.filter(is_active=True)
        context['featured_products'] = Product.objects.filter(is_active=True, recommended=True)[:8]
        context['new_products'] = Product.objects.filter(is_active=True).order_by('-created_at')[:12]
        context['countries'] = Country.objects.filter(is_active=True)
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'main/page-category.html'
    context_object_name = 'category'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        context['products'] = Product.objects.filter(
            product_category__category=category,
            is_active=True
        )
        context['product_categories'] = category.product_categories.filter(is_active=True)
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'main/page-listing-grid.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(product_category__slug=category_slug)
        
        country_id = self.request.GET.get('country')
        if country_id:
            queryset = queryset.filter(country_id=country_id)
        
        condition = self.request.GET.get('condition')
        if condition:
            queryset = queryset.filter(condition=condition)
        
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        verified = self.request.GET.get('verified')
        if verified == 'true':
            queryset = queryset.filter(verified=True)
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(desc__icontains=search) |
                Q(brand__icontains=search) |
                Q(company__icontains=search)
            )
        
        sort = self.request.GET.get('sort', '-created_at')
        queryset = queryset.order_by(sort)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.filter(is_active=True)
        context['countries'] = Country.objects.filter(is_active=True)
        return context


class ProductListLargeView(ProductListView):
    template_name = 'main/page-listing-large.html'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        company = self.request.GET.get('company')
        if company:
            queryset = queryset.filter(company=company)
        
        size = self.request.GET.get('size')
        if size:
            queryset = queryset.filter(size=size)
        
        return queryset


class ProductDetailView(DetailView):
    model = Product
    template_name = 'main/page-detail-product.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        
        context['product_images'] = product.images.filter(is_active=True)
        
        context['related_products'] = Product.objects.filter(
            product_category=product.product_category,
            is_active=True
        ).exclude(id=product.id)[:4]
        
        return context


class ContentView(TemplateView):
    template_name = 'main/page-content.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.filter(is_active=True)
        return context


class CategoryListView(TemplateView):
    template_name = 'main/page-category.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True).prefetch_related('product_categories')
        return context


class SearchView(ListView):
    model = Product
    template_name = 'main/page-listing-grid.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Product.objects.filter(
                Q(title__icontains=query) | 
                Q(desc__icontains=query) |
                Q(brand__icontains=query) |
                Q(company__icontains=query),
                is_active=True
            )
        return Product.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['categories'] = ProductCategory.objects.filter(is_active=True)
        context['countries'] = Country.objects.filter(is_active=True)
        return context