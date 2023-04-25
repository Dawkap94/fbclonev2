from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser, Post, Comment, Messages


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Enter your username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control',
                                             'placeholder': 'Enter your first name'}),
        }

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class AvatarForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['avatar']


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
        fields = '__all__'  # or ['phone_number', 'Birthday', 'city', 'only_fields_you_want_to_edit']
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