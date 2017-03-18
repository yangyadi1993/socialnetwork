from django import forms

from django.contrib.auth.models import User
from grumblr.models import *

class RegistrationForm(forms.Form):
    username = forms.EmailField()
    #first_name = forms.CharField(max_length = 200)
    password1 = forms.CharField(max_length = 200,
                                label = 'Password',
                                widget = forms.PasswordInput())
    password2 = forms.CharField(max_length = 200,
                                label = 'Confirm password',
                                widget = forms.PasswordInput())

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password did not match.")

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        return username

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('owner', )
        widget = {'picture' : forms.FileInput() }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('user', 'date', )
        widgets = {
            'text': forms.TextInput(
                attrs={'id': 'post-field', 'required': True}
            ),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('owner', 'user', 'date', )
        widgets = {
            'text': forms.TextInput(
                attrs={'id': 'comment-field', 'required': True}
            ),
        }
    def __init__(self, postid=None, *args, **kwargs):

        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['stream_id'] = postid


