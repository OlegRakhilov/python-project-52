from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label=_("First Name"), max_length=150, required=True)
    last_name = forms.CharField(label=_("Last Name"), max_length=150, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name')


class CustomUserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label=_("First name"), max_length=150, required=True)
    last_name = forms.CharField(label=_("Last name"), max_length=150, required=True)
    password = forms.CharField(
        label=_("Password"), 
        widget=forms.PasswordInput, 
        required=False
    )
    password_confirm = forms.CharField(
        label=_("Password confirmation"), 
        widget=forms.PasswordInput, 
        required=False
    )


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')