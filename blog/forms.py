from django import forms
from .models import Comment
from django.forms import ModelForm
from blog.models import Post


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']


class SearchForm(forms.Form):
    query = forms.CharField()


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'body']
