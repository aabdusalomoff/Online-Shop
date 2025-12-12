from django.urls import path
from .views import (
    HomeView,
    CategoryDetailView,
    ProductListView,
    ProductListLargeView,
    ProductDetailView,
    ContentView,
    SearchView
)

app_name = 'main'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/large/', ProductListLargeView.as_view(), name='product_list_large'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('search/', SearchView.as_view(), name='search'),
    path('content/', ContentView.as_view(), name='content'),
]