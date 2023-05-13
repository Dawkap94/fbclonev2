from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import CustomUser, Post, Comment, Messages


class NewUserForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password', 'name': 'password1', 'placeholder': 'Password'}),
        label='Enter your password')
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password', 'name': 'password2', 'placeholder': 'Password Confirmation'}),
        label='Confirm your password')

    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", "email")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Enter your username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control',
                                             'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control',
                                                 'placeholder': 'Enter your last name'}),
            'email': forms.TextInput(attrs={'class': 'form-control',
                                                 'placeholder': 'Enter your email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control',
                                                     'placeholder': 'Enter your password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control',
                                                     'placeholder': 'Enter your password again'}),

        }
    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class DateInput(forms.DateInput):
    input_type = 'date'


class AvatarForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['avatar', 'birth_date', 'user_about']
        labels = {
            "birth_date": "Your date of birth:",
            "content": ""
        }
        widgets = {
            'birth_date': DateInput(),
            'user_about': forms.Textarea(attrs={'class': 'form-control',
                                             'placeholder': "Write somthing about yourself"}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        labels = {
            "title": "",
            "content": ""
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Your post title'}),
            'content': forms.Textarea(attrs={'class': 'form-control',
                                             'placeholder': "What's on your mind?"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {'content': ""}
        widgets = {'content': forms.TextInput(attrs={'class': 'form-control',
                                         'placeholder': 'Add your comment'})}


class EditUserInfoForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'
        widgets = {
        'Name': forms.TextInput(attrs={'class': 'form-control',
                                       'placeholder': f'Tutaj imie'}),
        'Last_Name': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': f'Tutaj nazwisko'}),
    }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ['content']
        labels = {'content': ''}
        widgets = {'content': forms.TextInput(attrs={'class': 'form-control',
                                                     'placeholder': 'Type your message'})}
