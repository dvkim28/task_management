from django import forms

from accounts.models import User


class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(
        label="Email address",
        max_length=100,
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            'placeholder': 'Enter email'
        }))
    first_name = forms.CharField(
        label="First Name",
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter first name"
        }))
    last_name = forms.CharField(
        label="Last Name",
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter last name"
        }))
    position = forms.CharField(
        label="position",
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter position"
        }))
    company = forms.CharField(
        label="company",
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter company"}))
    about_info = forms.CharField(
        label="About Info",
        widget=forms.Textarea(attrs={
            "class": "form-control", "placeholder": "Bio"
        }))

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "position",
            "company",
            "about_info"
        ]
