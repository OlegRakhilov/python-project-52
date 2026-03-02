from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import ProtectedError
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.shortcuts import redirect
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from django.contrib.auth.views import LoginView, LogoutView


class UserListView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'

class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = _("User is successfully registered")

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = CustomUserUpdateForm 
    template_name = 'users/update.html'
    success_url = reverse_lazy('users')
    success_message = _("User is successfully updated")

    def test_func(self):
        return self.get_object() == self.request.user

    # Добавляем редирект вместо ошибки 403
    def handle_no_permission(self):
        messages.error(self.request, _("You do not have permission to edit another user."))
        return redirect('users')

class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users')
    success_message = _("User is successfully deleted")

    def test_func(self):
        return self.get_object() == self.request.user

    # Добавляем редирект вместо ошибки 403
    def handle_no_permission(self):
        messages.error(self.request, _("You do not have permission to delete another user."))
        return redirect('users')
    
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                self.request, 
                _("Cannot delete user because it is in use")
            )
            return redirect('users')
        
class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    success_message = _("You are logged in")

class UserLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _("You are logged out"))
        return super().dispatch(request, *args, **kwargs)