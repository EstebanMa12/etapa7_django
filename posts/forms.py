"""Post forms"""

from django import forms

from .models import Post

class PostForm(forms.ModelForm):
    """Form for creating a post"""
    class Meta:
        model = Post
        fields = ('title', 'content', 'read_permission', 'edit_permission')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'read_permission': forms.Select(attrs={'class': 'form-control'}),
            'edit_permission': forms.Select(attrs={'class': 'form-control'}),
        }