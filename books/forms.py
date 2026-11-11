from django import forms
from django.contrib.auth.models import User
from .models import Book, Review

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'category', 'description', 'publication_year', 'pages', 'cover_image_url', 'preview_content', 'file_download_url', 'is_featured']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Designing Data-Intensive Applications'}),
            'author': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Martin Kleppmann'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4, 'placeholder': 'Book synopsis and core topics...'}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-input'}),
            'pages': forms.NumberInput(attrs={'class': 'form-input'}),
            'cover_image_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://...'}),
            'preview_content': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 6, 'placeholder': 'Sample text / Chapter 1 excerpt...'}),
            'file_download_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://...'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Write your thoughts on this book...'}),
        }

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Choose password'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Confirm password'}))

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email address'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match.")
        return cleaned_data
