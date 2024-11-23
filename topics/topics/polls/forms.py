from django import forms
from django.contrib.auth.models import User
from .models import Topic, Comment
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    class LoginForm(AuthenticationForm):
        username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'autofocus': True}))
        password = forms.CharField(widget=forms.PasswordInput)

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'description']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']