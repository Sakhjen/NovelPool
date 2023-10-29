from typing import Any

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound, HttpResponseForbidden
from .models import *
from .forms import NovelForm, ChapterForm, PageForm, SelectionForm, TransitionForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.core.exceptions import PermissionDenied

# Create your views here.



def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    
    form = UserRegistrationForm()
    context = {
        'form':form
    }
    return render(request, 'registration/register.html', context)


class IndexView(ListView):
    model = Novel
    template_name = 'novelpool/index.html'
    context_object_name = 'novels'

    # def get_queryset(self) -> QuerySet[Any]:
    #     return Novel.objects.filter(status=2)


def tutorial(request):
    return render(request, 'novelpool/tutorial.html')


def read(request, novel_id, page_id):
    novel = Novel.objects.get(id=novel_id)
    page = novel.page_set.filter(id=page_id).first()
    if(page):
        selections = page.selection_set.all()
        context = {
            'page':page, 
            'selections':selections
        }
        return render(request, 'novelpool/read.html', context=context)
    return HttpResponseNotFound()


class NovelView(DetailView):
    model = Novel
    template_name = 'novelpool/novel.html'
    context_object_name = 'novel'

    def get_object(self, queryset=None):
        return get_object_or_404(Novel, id=self.kwargs['novel_id'])


class NovelEditCreateView(FormView):
    form_class = NovelForm
    template_name = 'novelpool/create_novel.html'
    success_url = 'novel'
    
    def form_valid(self, form):
        form.cleaned_data['owner'] = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        novel = None
        context = super().get_context_data(**kwargs)
        if 'novel_id' in self.kwargs:
            novel = get_object_or_404(Novel, id=self.kwargs['novel_id'])
            context['form'].instance = novel
            if self.request.user != novel.getOwner():
                raise PermissionDenied()
        context['novel'] = novel
        return context
    



@login_required
def novel_edit_or_create(request, novel_id = None):
    novel = None
    if novel_id:
        novel = get_object_or_404(Novel, id=novel_id)
        if request.user != novel.getOwner():
            return HttpResponseForbidden()
    if request.method == 'POST':
        data = request.POST.copy()
        data['owner'] = request.user.id
        form = NovelForm(data, instance=novel)
        if form.is_valid():
            novel = form.save()
            return redirect('novel', novel_id=novel.id)
    form = NovelForm(instance=novel)

    context = {
        'form':form,
        'novel':novel
    }
    return render(request, 'novelpool/create_novel.html', context)

@login_required
def novel_delete(request, novel_id):
    novel = get_object_or_404(Novel, id=novel_id)
    if request.user != novel.getOwner():
        return HttpResponseForbidden()
    
    novel.delete()
    return redirect('index')


@login_required
def chapter_edit_or_create(request, novel_id, chapter_id=None):
    chapter = None
    novel = get_object_or_404(Novel, id=novel_id)
    if request.user != novel.getOwner():
            return HttpResponseForbidden()
    if chapter_id:
        chapter = get_object_or_404(Chapter, id=chapter_id)
        
    if request.method == 'POST':
        data = request.POST.copy()
        data['novel'] = Novel.objects.filter(id=novel_id).first()
        form = ChapterForm(data, instance=chapter)
        if form.is_valid():
            chapter = form.save()
            return redirect('chapter', novel_id=novel_id, chapter_id=chapter.id)
    form = ChapterForm(instance=chapter)
    context = {
        'form':form,
        'novel':novel,
        'chapter':chapter
    }
    return render(request, 'novelpool/create_chapter.html', context)
        

class ChapterView(DetailView):
    model=Chapter
    template_name = 'novelpool/chapter.html'
    context_object_name = 'chapter'

    def get_object(self):
        chapter = get_object_or_404(Chapter, novel__id = self.kwargs['novel_id'], id=self.kwargs['chapter_id'])
        if self.request.user != chapter.getOwner():
            raise PermissionDenied()
        return chapter
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['novel'] = context['chapter'].novel
        return context


@login_required
def chapter_delete(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    novel = chapter.novel
    if request.user != chapter.getOwner():
        return HttpResponseForbidden()
    chapter.delete()
    return redirect('novel', novel_id=novel.id)


@login_required
def page_edit_or_create(request, novel_id, chapter_id=None, page_id=None):
    page = None
    novel = get_object_or_404(Novel, id=novel_id)
    if page_id:
        page = get_object_or_404(Page, id=page_id)
    if request.user != novel.getOwner():
        return HttpResponseForbidden()
    if request.method == 'POST':
        data = request.POST.copy()
        data['novel'] = Novel.objects.filter(id=novel_id).first()
        if not novel.hasFirstPage() or (not page is None and page.is_first):
            data['is_first'] = True
        if data['is_first']:
            first_page = Page.objects.filter(novel=novel_id).filter(is_first=True).first()
            if first_page:
                first_page.is_first = False
                first_page.save()
        form = PageForm(data, instance=page)
        if form.is_valid():
            page = form.save()
            return redirect('page', novel_id=novel_id, page_id=page.id)
    chapter = None
    if(chapter_id):
        chapter = Chapter.objects.filter(id=chapter_id).first()
    if not novel.hasFirstPage() or (not page is None and page.is_first):
        form = PageForm(initial={'is_first':True}, instance=page)
        form.fields['is_first'].disabled = True 
    else:
        form = PageForm(instance=page)
    form.fields['chapter'].queryset = Chapter.getQuerySetByNovelId(novel_id)
    
    context = {
        'novel':novel,
        'chapter':chapter,
        'page':page,
        'form':form
    }
    return render(request, 'novelpool/create_page.html', context)


class PageView(DetailView):
    model=Page
    template_name = 'novelpool/page.html'
    context_object_name = 'page'

    def get_object(self):
        page = get_object_or_404(Page, novel__id = self.kwargs['novel_id'], id=self.kwargs['page_id'])
        if self.request.user != page.getOwner():
            raise PermissionDenied()
        return page
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['novel'] = context['page'].novel
        return context


@login_required
def page_delete(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    if request.user != page.getOwner():
        return HttpResponseForbidden()
    page.delete()
    return redirect('chapter', novel_id=page.chapter.novel.id, chapter_id=page.chapter.id)


@login_required
def selection_edit_or_create(request, novel_id, page_id, selection_id=None):
    selection = None
    novel = get_object_or_404(Novel, id=novel_id)
    if selection_id:
        selection = get_object_or_404(Selection, id=selection_id)
    page = get_object_or_404(Page, id=page_id)
    if request.user != page.getOwner():
        return HttpResponseForbidden()
    if request.method == 'POST':
        data = request.POST.copy()
        data['page'] = page
        form = SelectionForm(data, instance=selection)
        if form.is_valid():
            selection = form.save()
            return redirect('selection', novel_id=novel_id, page_id=page_id, selection_id=selection.id)
    form = SelectionForm(instance=selection)
    context = {
        'novel': novel,
        'page': page,
        'selection':selection,
        'form': form
    }
    return render(request, 'novelpool/create_selection.html', context)


class SelectionView(DetailView):
    model=Selection
    template_name = 'novelpool/selection.html'
    context_object_name = 'selection'

    def get_object(self):
        selection = get_object_or_404(Selection, page__novel__id = self.kwargs['novel_id'], page__id=self.kwargs['page_id'], id=self.kwargs['selection_id'])
        if self.request.user != selection.getOwner():
            raise PermissionDenied()
        return selection
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['novel'] = context['selection'].page.novel
        context['page'] = context['selection'].page
        return context


@login_required
def selection_delete(request, selection_id):
    selection = get_object_or_404(Selection, id=selection_id)
    if request.user != selection.getOwner():
        return HttpResponseForbidden()
    selection.delete()
    return redirect('page', novel_id=selection.page.chapter.novel.id, page_id=selection.page.id)


@login_required
def transition_edit_or_create(request, novel_id, page_id, selection_id=None, transition_id=None):
    transition = None
    if transition_id:
        transition = get_object_or_404(Transition, id=transition_id)
    page_from = get_object_or_404(Page, id=page_id)
    selection = None
    if request.user != page_from.getOwner():
        return HttpResponseForbidden()
    if selection_id:
        selection = get_object_or_404(Selection, id=selection_id)
    if request.method == 'POST':
        data = request.POST.copy()
        data['page_from'] = page_from
        if selection:
            data['selection'] = selection
        form = TransitionForm(data, instance=transition)
        if form.is_valid():
            transition = form.save()
            return redirect('transition', novel_id=novel_id, page_id=page_id, transition_id=transition.id)
    novel = get_object_or_404(Novel, id=novel_id)
    form = TransitionForm(instance=transition)
    form.fields['page_to'].queryset = Page.objects.filter(novel=novel).exclude(id=page_id).all()
    form.fields['selection'].queryset = Selection.objects.filter(page=page_from).all()
    context = {
        'novel':novel,
        'page':page_from,
        'selection':selection,
        'transition':transition,
        'form':form
    }
    
    return render(request, 'novelpool/create_transition.html', context)


class TransitionView(DetailView):
    model=Transition
    template_name = 'novelpool/transition.html'
    context_object_name = 'transition'

    def get_object(self):
        transition = get_object_or_404(Transition, page_from__novel__id = self.kwargs['novel_id'], page_from__id=self.kwargs['page_id'], id=self.kwargs['transition_id'])
        if self.request.user != transition.getOwner():
            raise PermissionDenied()
        return transition
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['novel'] = context['transition'].page_from.novel
        context['page_from'] = context['transition'].page_from
        context['page_to'] = context['transition'].page_to
        context['selection'] = context['transition'].selection
        return context


@login_required
def transition_delete(request, transition_id):
    transition = get_object_or_404(Transition, id=transition_id)
    if request.user != transition.getOwner():
        return HttpResponseForbidden()
    transition.delete()
    return redirect('selection', novel_id=transition.selection.page.chapter.novel.id, page_id=transition.selection.page.id, selection_id=transition.selection.id)


class ProfileView(DetailView):
    model=User
    template_name = 'novelpool/profile.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['novels'] = Novel.objects.filter(owner=self.request.user).all()
        return context
