from django import forms
from django.contrib.auth.models import User
from shop.models import Product, Category, Subject, Professor
from django.core.exceptions import ValidationError
import datetime

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

        '''
        input_formats = ['%Y-%m-%d %H:%M:%S']

        widgets = {
            'init_dateTime': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S',attrs={'class': 'datetime-input'}),
            'finish_dateTime': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S',attrs={'class': 'datetime-input'}),
        }
        '''
    
    def clean_init_dateTime(self):
        init_dateTime = self.cleaned_data['init_dateTime']
        expected_format = '%Y-%m-%d %H:%M:%S'

        try:
            init_dateTime = datetime.datetime.strptime(init_dateTime, expected_format)
        except ValueError:
            raise ValidationError(f'Incorrect format. Initial date should be in {expected_format} format.')

        return init_dateTime

    def clean_finish_dateTime(self):
        finish_dateTime = self.cleaned_data['finish_dateTime']
        expected_format = '%Y-%m-%d %H:%M:%S'

        try:
            finish_dateTime = datetime.datetime.strptime(finish_dateTime, expected_format)
        except ValueError:
            raise ValidationError(f'Incorrect format. Finish date should be in {expected_format} format.')

        return finish_dateTime
'''
    def clean(self):
        cleaned_data = super().clean()
        init_dateTime = cleaned_data.get("init_dateTime")
        finish_dateTime = cleaned_data.get("finish_dateTime")

        if init_dateTime and finish_dateTime and init_dateTime >= finish_dateTime:
            raise forms.ValidationError("La fecha de inicio debe ser anterior a la fecha de finalización.")

        return cleaned_data
    '''
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
