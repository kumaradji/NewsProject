from django import forms
from .models import Post


# Используется при новой публикации
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
