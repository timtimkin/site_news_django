from django.forms import ModelForm
from .models import Post, Subscriber, Category
from django import forms


class PostForm(forms.ModelForm):
    postCategory = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Post
        fields = ['author', 'postType', 'title', 'text', 'postCategory']


class SubscriberForm(forms.ModelForm):
    subscribed_categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Subscriber
        fields = ['email', 'subscribed_categories']
