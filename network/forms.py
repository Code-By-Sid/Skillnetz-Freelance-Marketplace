# forms.py
from django import forms
from .models import posts

class PostForm(forms.ModelForm):
    class Meta:
        model = posts
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': "What's on your mind? Share an update, a win, or a question..."}),
        }
        labels = {
            'body': 'Write a post',
        }
