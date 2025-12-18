from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages

from .models import User


class UserLoginView(LoginView):
    template_name = 'accounts/page-user-login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('main:home')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Неверное имя пользователя или пароль')
        return super().form_invalid(form)


class UserRegisterView(CreateView):
    model = User
    template_name = 'accounts/page-user-register.html'
    fields = ['username', 'email', 'password', 'phone', 'address']
    success_url = reverse_lazy('accounts:login')
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        if password != password2:
            messages.error(request, 'Passwords do not match!')
            return redirect('accounts:register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('accounts:register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect('accounts:register')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            phone=phone,
            address=address
        )
        
        messages.success(request, 'Registration successful! You can now login.')
        return redirect('accounts:login')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('main:home')


class ProfileMainView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/page-profile-main.html'
    login_url = reverse_lazy('accounts:login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        
        context['orders_count'] = 0  
        context['wishlist_count'] = 0  
        context['awaiting_delivery'] = 0
        context['delivered_items'] = 0
        context['recent_orders'] = []  
        
        return context


class ProfileSettingView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'accounts/page-profile-setting.html'
    fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'address', 'image']
    success_url = reverse_lazy('accounts:profile_settings')
    login_url = reverse_lazy('accounts:login')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Профиль успешно обновлен!')
        return super().form_valid(form)


class ProfileAddressView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/page-profile-address.html'
    login_url = reverse_lazy('accounts:login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class ProfileOrdersView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/page-profile-orders.html'
    login_url = reverse_lazy('accounts:login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = []
        return context


class ProfileWishlistView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/page-profile-wishlist.html'
    login_url = reverse_lazy('accounts:login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wishlist'] = []
        return context


class ProfileSellerView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/page-profile-seller.html'
    login_url = reverse_lazy('accounts:login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.status != 'seller':
            messages.warning(self.request, 'У вас нет прав продавца')
        
        context['products'] = []
        return context