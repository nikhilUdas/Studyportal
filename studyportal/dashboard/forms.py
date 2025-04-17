from django import forms
from .models import Notes, Homework, Todo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Notes Form
class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# Homework Form
class HomeworkForm(forms.ModelForm):
    due = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        input_formats=['%Y-%m-%d'],
    )

    class Meta:
        model = Homework
        fields = ['subject', 'title', 'description', 'due']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# Dashboard Form (added based on your previous request)
class DashboardForm(forms.Form):
    text = forms.CharField(max_length=100, label="Enter your Search: ")

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'is_finished']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'is_finished': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']