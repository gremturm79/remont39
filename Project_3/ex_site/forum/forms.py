from django import forms
from .models import Category, Thread, Reply
from django.forms import ModelForm


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {'name': 'Название'}


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'content', 'category']  # , 'author'
        labels = {'title': 'Название', 'content': 'Текст', 'category': 'Категория'}  # ,'author': 'Автор'


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content', 'thread']  # , 'author'
        labels = {'content': 'Текст', 'thread': 'Тема'}  # , 'author': 'Автор'




