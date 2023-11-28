from django import forms
from django.contrib.auth.models import User
from shop.models import Product

class LoginForm(forms.Form):
 username = forms.CharField()
 password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
    
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'professor', 'subject', 'name', 'slug', 'image', 'description', 'price', 'init_dateTime', 'finish_dateTime']

        input_formats = ['%Y-%m-%d %H:%M:%S']

        widgets = {
            'init_dateTime': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S',attrs={'class': 'datetime-input'}),
            'finish_dateTime': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S',attrs={'class': 'datetime-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        init_dateTime = cleaned_data.get("init_dateTime")
        finish_dateTime = cleaned_data.get("finish_dateTime")

        if init_dateTime and finish_dateTime and init_dateTime >= finish_dateTime:
            raise forms.ValidationError("La fecha de inicio debe ser anterior a la fecha de finalización.")

        return cleaned_data
