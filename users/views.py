from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.shortcuts import redirect

class UserListView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'

class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = _("User is successfully registered")

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserCreationForm
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