from django import forms
from django.contrib.auth.models import User
from shop.models import Product, Category, Subject, Professor
from django.core.exceptions import ValidationError
import datetime, re
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}), label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}), label=("Email"))


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
    input_formats = ['%Y-%m-%d %H:%M:%S']
    price = forms.DecimalField(required=True, widget=forms.TextInput(attrs={"placeholder":'e.g.: 19.99'}))
    init_dateTime = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder":'YYYY-MM-DD HH-MM-SS'}))
    finish_dateTime = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder":'YYYY-MM-DD HH-MM-SS'}))
    class Meta:
        model = Product
        fields = ['category', 'professor', 'subject', 'name', 'slug', 'image', 'description', 'price', 'init_dateTime', 'finish_dateTime']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[str(field)].widget.attrs.update({'class':'form-control'})
        
    def clean(self):
        cleaned_data = super().clean()
        init_dateTime = cleaned_data.get("init_dateTime")
        finish_dateTime = cleaned_data.get("finish_dateTime")

        if init_dateTime and finish_dateTime and init_dateTime >= finish_dateTime:
            self.add_error('init_dateTime', "Initial DateTime must be before Finish DateTime.")
            
        try:
            if init_dateTime <= datetime.datetime.now() or finish_dateTime <= datetime.datetime.now():
                self.add_error('init_dateTime', "Initial DateTime and Finish DateTime can't be in the past.")
        except:
            pass
       
        return cleaned_data

    def clean_price(self):
        price = self.cleaned_data['price']
        # Check if the input matches the XX.XX format
        try:
            price_formatted = '{:.2f}'.format(price)
            if str(price_formatted) != str(price):
                raise forms.ValidationError("Price should be in XX.XX format.")
            if float(price_formatted) < 0:
                raise forms.ValidationError("Price can't be negative.")
        except ValueError:
            raise forms.ValidationError("Invalid price format. Use XX.XX format.")

        return price

    def clean_init_dateTime(self):
        init_dateTime = self.cleaned_data['init_dateTime']
        if len(str(init_dateTime)) != 19:
            raise forms.ValidationError("Invalid Date/Time format. Use YYYY-MM-DD HH-MM-SS format.")

        try:
            init_dateTime = datetime.datetime.strptime(init_dateTime, '%Y-%m-%d %H:%M:%S')
        except:
            raise forms.ValidationError("Invalid Date/Time format. Use YYYY-MM-DD HH-MM-SS format.")

        return init_dateTime

    def clean_finish_dateTime(self):
        finish_dateTime = self.cleaned_data['finish_dateTime']
        if len(str(finish_dateTime)) != 19:
            raise forms.ValidationError("Invalid Date/Time format. Use YYYY-MM-DD HH-MM-SS format.")

        try:
            finish_dateTime = datetime.datetime.strptime(finish_dateTime, '%Y-%m-%d %H:%M:%S')
        except:
            raise forms.ValidationError("Invalid Date/Time format. Use YYYY-MM-DD HH-MM-SS format.")

        return finish_dateTime

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields = ['name','slug']

class SubjetcForm(forms.ModelForm):
    class Meta:
        model=Subject
        fields = ['name','slug']

class ProfessorForm(forms.ModelForm):
    class Meta:
        model=Professor
        fields = ['name','surname','slug']
