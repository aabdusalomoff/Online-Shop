from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages

from .models import User


class UserLoginView(LoginView):
    """Страница входа"""
    template_name = 'accounts/page-user-login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('main:index')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Неверное имя пользователя или пароль')
        return super().form_invalid(form)


class UserRegisterView(CreateView):
    """Страница регистрации"""
    model = User
    template_name = 'accounts/page-user-register.html'
    fields = ['username', 'email', 'password', 'phone', 'address']
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        messages.success(self.request, 'Регистрация успешна! Теперь вы можете войти.')
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    """Выход из системы"""
    next_page = reverse_lazy('main:index')


class ProfileMainView(LoginRequiredMixin, TemplateView):
    """Главная страница профиля"""
    template_name = 'accounts/page-profile-main.html'
    login_url = reverse_lazy('accounts:login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        
        # Здесь будут заказы когда создадите модель Order
        context['orders_count'] = 0  # Замените на Order.objects.filter(user=user).count()
        context['wishlist_count'] = 0  # Замените на Wishlist.objects.filter(user=user).count()
        context['awaiting_delivery'] = 0
        context['delivered_items'] = 0
        context['recent_orders'] = []  # Замените на Order.objects.filter(user=user).order_by('-created_at')[:6]
        
        return context


class ProfileSettingView(LoginRequiredMixin, UpdateView):
    """Настройки профиля"""
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
    """Адреса доставки"""
    template_name = 'accounts/page-profile-address.html'
    login_url = reverse_lazy('accounts:login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class ProfileOrdersView(LoginRequiredMixin, TemplateView):
    """История заказов"""
    template_name = 'accounts/page-profile-orders.html'
    login_url = reverse_lazy('accounts:login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Здесь будут заказы когда создадите модель Order
        context['orders'] = []
        return context


class ProfileWishlistView(LoginRequiredMixin, TemplateView):
    """Список желаний"""
    template_name = 'accounts/page-profile-wishlist.html'
    login_url = reverse_lazy('accounts:login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Здесь будет wishlist когда создадите модель
        context['wishlist'] = []
        return context


class ProfileSellerView(LoginRequiredMixin, TemplateView):
    """Профиль продавца"""
    template_name = 'accounts/page-profile-seller.html'
    login_url = reverse_lazy('accounts:login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Проверяем что пользователь - продавец
        if user.status != 'seller':
            messages.warning(self.request, 'У вас нет прав продавца')
        
        # Здесь будут товары продавца когда добавите связь
        context['products'] = []
        return context