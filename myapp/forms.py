from django import forms
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ImageUploadForm(forms.Form):
    image = forms.ImageField(label='Upload Image')
    direction = forms.ChoiceField(
        choices=[('A2B', 'A to B'), ('B2A', 'B to A')],
        label='Conversion Direction'
    )


class EmailUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]  # Set username as email
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)