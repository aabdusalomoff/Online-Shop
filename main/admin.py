from django.contrib import admin
from django.contrib.admin import TabularInline
from unfold.admin import ModelAdmin
from .models import Category, ProductCategory, Country, Product, ProductImage, Service


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['name', 'slug', 'color', 'is_active']
    list_filter = ['is_active', 'color']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductCategory)
class ProductCategoryAdmin(ModelAdmin):
    list_display = ['name', 'slug', 'category', 'is_active']
    list_filter = ['is_active', 'category']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Country)
class CountryAdmin(ModelAdmin):
    list_display = ['name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']


class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'is_active']


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ['title', 'price', 'product_category', 'country', 'quantity', 'star', 'verified', 'is_active']
    list_filter = ['is_active', 'verified', 'recommended', 'product_category', 'country', 'created_at']
    search_fields = ['title', 'desc', 'company', 'brand']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'update_at']
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'desc', 'main_image')
        }),
        ('Категория и страна', {
            'fields': ('product_category', 'country')
        }),
        ('Цена и количество', {
            'fields': ('price', 'quantity', 'dicount')
        }),
        ('Характеристики', {
            'fields': ('company', 'brand', 'size', 'color', 'condition', 'year')
        }),
        ('Рейтинг и отзывы', {
            'fields': ('star', 'review', 'delivery_time')
        }),
        ('Статусы', {
            'fields': ('verified', 'recommended', 'is_active')
        }),
        ('Даты', {
            'fields': ('created_at', 'update_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ProductImage)
class ProductImageAdmin(ModelAdmin):
    list_display = ['product', 'is_active']
    list_filter = ['is_active', 'product']
    search_fields = ['product__title']


@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = ['title', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'desc']