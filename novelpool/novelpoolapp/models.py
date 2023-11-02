from django.db import models
from enum import Enum
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import PermissionDenied


class NovelStatus(Enum):
    DRAFT = 1
    WORK = 2


class Novel(models.Model):
    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    status = models.IntegerField('Статус',default=1)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')

    def __str__(self):
        return self.name
    
    def getFirstPage(self):
        first_page = self.page_set.filter(is_first=True).first()
        return first_page
    
    def hasFirstPage(self):
        return not self.getFirstPage() is None
    
    class Meta:
        verbose_name = 'Новелла'
        verbose_name_plural = 'Новеллы'

    def getOwner(self):
        return self.owner
    
    def validateUser(self, user):
        if self.getOwner() != user:
            raise PermissionDenied()
    
    def get_absolute_url(self):
        return reverse('novel', kwargs={'novel_id':self.id})


class Chapter(models.Model):
    name = models.CharField('Название', max_length=20)
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, verbose_name='Новелла')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Глава'
        verbose_name_plural = 'Главы'

    def getQuerySetByNovelId(novel_id):
        novel = Novel.objects.filter(id=novel_id).first()
        return Chapter.objects.filter(novel=novel).all()
    
    def getOwner(self):
        return self.novel.getOwner()
    
    def validateUser(self, user):
        if self.getOwner() != user:
            raise PermissionDenied()
    
    def get_absolute_url(self):
        return reverse('chapter', kwargs={'novel_id':self.novel.id, 'chapter_id':self.id})


class Page(models.Model):
    name = models.CharField('Название', max_length=20)
    text = models.TextField('Текст')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, verbose_name='Глава')
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, verbose_name='Новелла')
    is_first = models.BooleanField('Является первой страницей', default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'

    def getOwner(self):
        return self.novel.getOwner()
    
    def validateUser(self, user):
        if self.getOwner() != user:
            raise PermissionDenied()
    
    def get_absolute_url(self):
        return reverse('page', kwargs={'novel_id':self.novel.id, 'page_id':self.id})


class Selection(models.Model):
    text = models.CharField('Ответ', max_length=500)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, verbose_name='Страница')

    def __str__(self):
        return f'(Ответ) {self.page.name} - {self.text[:10]}'
    
    def hasNoTransition(self):
        transitions = self.transition_set.all()
        return transitions.count() == 0
    
    def getOwner(self):
        return self.page.getOwner()
    
    def validateUser(self, user):
        if self.getOwner() != user:
            raise PermissionDenied()
    
    def get_absolute_url(self):
        return reverse('selection', kwargs={'novel_id':self.page.novel.id, 'page_id':self.page.id, 'selection_id':self.id})
    
    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'


class Transition(models.Model):
    page_from = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='outcoming_transitions', verbose_name='Страница отправления')
    page_to = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='incoming_transitions', verbose_name='Страница назначения')
    selection = models.ForeignKey(Selection, on_delete=models.CASCADE, verbose_name='Выбор')
    description = models.CharField(max_length=1000, verbose_name='Описание')

    def __str__(self):
        return self.description
    
    class Meta:
        verbose_name = 'Переход'
        verbose_name_plural = 'Переходы'

    def getOwner(self):
        return self.page_from.getOwner()
    
    def validateUser(self, user):
        if self.getOwner() != user:
            raise PermissionDenied()