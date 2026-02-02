"""
User authentication views: register, login, logout.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import UserRegisterForm


class RegisterView(CreateView):
    """User registration view."""
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('rooms:room_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


class CustomLoginView(LoginView):
    """Custom login view with our template."""
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('rooms:room_list')


class CustomLogoutView(LogoutView):
    """Custom logout view."""
    next_page = reverse_lazy('rooms:home')
