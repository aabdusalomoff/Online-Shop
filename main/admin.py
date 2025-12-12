from django.contrib import admin
from .models import Category, ProductCategory, Country, Product, ProductImage, Service


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color', 'is_active']
    list_filter = ['is_active', 'color']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'is_active']
    list_filter = ['is_active', 'category']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    fields = ['image', 'is_active']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'product_category', 'country', 'quantity', 'star', 'verified', 'is_active']
    list_filter = ['is_active', 'product_category', 'country', 'created_at']
    search_fields = ['title', 'company', 'brand']
    prepopulated_fields = {'slug': ('title',)}
    

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'is_active']
    list_filter = ['is_active', 'product']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'description']