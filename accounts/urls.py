from django.urls import path
from .views import (
    UserLoginView,
    UserRegisterView,
    UserLogoutView,
    ProfileMainView,
    ProfileSettingView,
    ProfileAddressView,
    ProfileOrdersView,
    ProfileWishlistView,
    ProfileSellerView
)

app_name = 'accounts'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', ProfileMainView.as_view(), name='profile_main'),
    path('profile/settings/', ProfileSettingView.as_view(), name='profile_settings'),
    path('profile/address/', ProfileAddressView.as_view(), name='profile_address'),
    path('profile/orders/', ProfileOrdersView.as_view(), name='profile_orders'),
    path('profile/wishlist/', ProfileWishlistView.as_view(), name='profile_wishlist'),
    path('profile/seller/', ProfileSellerView.as_view(), name='profile_seller'),
]