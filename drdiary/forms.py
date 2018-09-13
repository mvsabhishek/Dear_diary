from django import forms
from django.forms import ModelForm, widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from drdiary.models import Diary
from django.utils.text import slugify
from django.core.exceptions import ValidationError



class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('An account with this username already exists.')
        return username

    def clean_email(self):
        email1 = self.cleaned_data['email']
        if User.objects.filter(email=email1).exists():
            raise ValidationError('An account with this email already exists.')
        return email1


class EntriesForm(ModelForm):
    title = forms.CharField(label="", max_length = 200,required=True, widget=forms.TextInput(attrs={'placeholder':'Enter title', 'class':'form-control'}))
    body = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder':'Tell me about your day...', 'rows': 15, 'cols': 100, 'class':'form-control' }),max_length = 10000,required=True )
    class Meta:
        model = Diary
        fields = ('title', 'body')

