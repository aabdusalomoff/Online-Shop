from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import User


class UserLoginView(LoginView):
    template_name = 'accounts/page-user-login.html'
    redirect_authenticated_user = True


class UserRegisterView(CreateView):
    model = User
    template_name = 'accounts/page-user-register.html'
    fields = ['username', 'email', 'password', 'phone', 'address']
    success_url = reverse_lazy('accounts:login')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('main:home')


class ProfileMainView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/page-profile-main.html'
    login_url = reverse_lazy('accounts:login')


class ProfileSettingView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'accounts/page-profile-setting.html'
    fields = ['username', 'email', 'phone', 'address', 'image']
    success_url = reverse_lazy('accounts:profile_main')


class ProfileAddressView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/page-profile-address.html'
    login_url = reverse_lazy('accounts:login')


class ProfileOrdersView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/page-profile-orders.html'
    login_url = reverse_lazy('accounts:login')
    

class ProfileWishlistView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/page-profile-wishlist.html'
    login_url = reverse_lazy('accounts:login')
    

class ProfileSellerView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/page-profile-seller.html'
    login_url = reverse_lazy('accounts:login')
