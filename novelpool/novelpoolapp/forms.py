from .models import *
from django.forms import ModelForm, TextInput, Textarea, ModelChoiceField, BooleanField, Select, CharField, PasswordInput,ValidationError
#trying to push to dev branch

class UserRegistrationForm(ModelForm):
    password = CharField(label='Пароль', widget=PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Пароль'
            }))
    password2 = CharField(label='Повторите пароль', widget=PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Повторите пароль'
            }))


    class Meta:
        model = User
        fields = [
            'username', 
            'first_name', 
            'last_name',
            'email',
        ]
        widgets = {
            'username':TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Логин'
            }),
            'first_name':TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя'
            }),
            'last_name':TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия'
            }),
            'email':TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Адрес электронной почты'
            }),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError('Пароли не совпадают.')
        return cd['password2']


class NovelForm(ModelForm):
    class Meta:
        model = Novel
        fields = [
            'name',
            'description',
            'owner'
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