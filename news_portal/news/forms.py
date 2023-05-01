from email.headerregistry import Group

from allauth.account.forms import SignupForm
from django import forms
from .models import *


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title',
                  'categoryType',
                  'category',
                  'text'
                  ]


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)


# class BasicSignupForm(SignupForm):
#
#     def save(self, request):
#         user = super(BasicSignupForm, self).save(request)
#         basic_group = Group.objects.get(name='newuser')
#         basic_group.user_set.add(user)
