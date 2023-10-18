from .models import *
from django.forms import ModelForm, TextInput, Textarea, ModelChoiceField, BooleanField, Select

class NovelForm(ModelForm):
    class Meta:
        model = Novel
        fields = [
            'name',
            'description'
        ]
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название'
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание'
            })

        }


class ChapterForm(ModelForm):
    class Meta:
        model = Chapter
        fields = [
            'name',
            'novel'
        ]
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название'
            })
        }
    

class PageForm(ModelForm):
    class Meta:
        model = Page
        chapter = ModelChoiceField(queryset=Chapter.objects.all(), to_field_name="name")
        is_first = BooleanField(label='Первая страница')
        fields = [
            'name',
            'text',
            'chapter',
            'novel',
            'is_first'
        ]
        widgets = {
            'name': TextInput(attrs = {
                'class': 'form-control',
                'placeholder': 'Введите название'
            }),
            'text': Textarea(attrs = {
                'class': 'form-control',
                'placeholder': 'Введите текст'
            })
        }

class SelectionForm(ModelForm):
    class Meta:
        model = Selection
        fields = [
            'text',
            'page'
        ]
        widgets = {
            'text': TextInput(attrs = {
                'class': 'form-control',
                'placeholder': 'введите текст ответа'
            })
        }

class TransitionForm(ModelForm):
    class Meta:
        model = Transition
        fields = [
            'page_from',
            'page_to',
            'selection',
            'description'
        ]
        widgets = {
            'page_to': Select(attrs = {
                'class': 'form-control'
            }),
            'selection': Select(attrs = {
                'class': 'form-control'
            }),
            'description': TextInput(attrs = {
                'class': 'form-control',
                'placeholder': 'Введите описание перехода'
            })
        }