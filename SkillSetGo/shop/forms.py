from .models import *
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body','reclamation']

class ChangeStateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['state']