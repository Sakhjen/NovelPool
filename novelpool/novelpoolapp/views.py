from typing import Any

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect
from .models import *
from .forms import NovelForm, ChapterForm, PageForm, SelectionForm, TransitionForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
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


class NovelCreateView(CreateView):
    form_class = NovelForm
    template_name = 'novelpool/create_novel.html'
    context_object_name = 'novel'
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    

class NovelEditView(UpdateView):
    form_class = NovelForm
    template_name = 'novelpool/create_novel.html'
    context_object_name = 'novel'

    def get_object(self, queryset=None):
        novel = get_object_or_404(Novel, id=self.kwargs['novel_id'])
        novel.validateUser(self.request.user)
        return novel


@login_required
def novel_delete(request, novel_id):
    novel = get_object_or_404(Novel, id=novel_id)
    novel.validateUser(request.user)
    
    novel.delete()
    return redirect('index')


class ChapterView(DetailView):
    model=Chapter
    template_name = 'novelpool/chapter.html'
    context_object_name = 'chapter'

    def get_object(self):
        chapter = get_object_or_404(Chapter, novel__id = self.kwargs['novel_id'], id=self.kwargs['chapter_id'])
        chapter.validateUser(self.request.user)
        return chapter
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['novel'] = context['chapter'].novel
        return context
    

class ChapterCreateView(CreateView):
    form_class = ChapterForm
    template_name = 'novelpool/create_chapter.html'
    context_object_name = 'chapter'
    novel = None

    def get(self, request, *args, **kwargs):
        self.novel = get_object_or_404(Novel, id=self.kwargs['novel_id'])
        self.novel.validateUser(self.request.user)
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.novel = get_object_or_404(Novel, id=self.kwargs['novel_id'])
        self.novel.validateUser(self.request.user)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.novel = self.novel
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['novel'] = self.novel
        return context
    

class ChapterEditView(UpdateView):
    form_class = ChapterForm
    template_name = 'novelpool/create_chapter.html'
    context_object_name = 'chapter'

    def get_object(self, queryset=None):
        chapter = get_object_or_404(Chapter, id=self.kwargs['chapter_id'], novel__id=self.kwargs['novel_id'])
        chapter.validateUser(self.request.user)
        return chapter
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['novel'] = get_object_or_404(Novel, id=self.kwargs['novel_id'])
        return context


@login_required
def chapter_delete(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    novel = chapter.novel
    chapter.validateUser(request.user)
    chapter.delete()
    return redirect('novel', novel_id=novel.id)


class PageView(DetailView):
    model=Page
    template_name = 'novelpool/page.html'
    context_object_name = 'page'

    def get_object(self):
        page = get_object_or_404(Page, novel__id = self.kwargs['novel_id'], id=self.kwargs['page_id'])
        page.validateUser(self.request.user)
        return page
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['novel'] = context['page'].novel
        return context
    

class PageCreateView(CreateView):
    form_class = PageForm
    template_name = 'novelpool/create_page.html'
    context_object_name = 'page'
    novel = None
    chapter = None

    def get(self, request, *args, **kwargs):
        self.novel = get_object_or_404(Novel, id=self.kwargs['novel_id'])
        self.novel.validateUser(self.request.user)
        if('chapter_id' in self.kwargs):
            self.chapter = get_object_or_404(Chapter, id=self.kwargs['chapter_id'], novel__id=self.novel.id)
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.novel = get_object_or_404(Novel, id=self.kwargs['novel_id'])
        self.novel.validateUser(self.request.user)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.novel = self.novel
        if not self.novel.hasFirstPage():
            self.object.is_first = True
        if self.object.is_first:
            first_page = Page.objects.filter(novel=self.kwargs['novel_id']).filter(is_first=True).first()
            if first_page:
                first_page.is_first = False
                first_page.save()
        if self.chapter:
            self.object.chapter = self.chapter
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['novel'] = self.novel
        context['form'].fields['chapter'].queryset = Chapter.getQuerySetByNovelId(self.kwargs['novel_id'])
        context['chapter'] = self.chapter
        if not self.novel.hasFirstPage():
            context['form'].fields['is_first'].disabled = True 
        return context
    
    def get_initial(self, *args, **kwargs):
        initial = super(PageCreateView, self).get_initial(**kwargs)
        if not self.novel.hasFirstPage():
            initial['is_first'] = True
        if self.chapter:
            initial['chapter'] = self.chapter
        return initial
    

class PageEditView(UpdateView):
    form_class = PageForm
    template_name = 'novelpool/create_page.html'
    context_object_name = 'page'

    def get_object(self, queryset=None):
        page = get_object_or_404(Page, id=self.kwargs['page_id'], novel__id=self.kwargs['novel_id'])
        page.validateUser(self.request.user)
        return page
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['novel'] = get_object_or_404(Novel, id=self.kwargs['novel_id'])
        if self.get_object().is_first:
            context['form'].fields['is_first'].disabled = True 
        return context
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.object.is_first:
            first_page = Page.objects.filter(novel=self.kwargs['novel_id']).filter(is_first=True).first()
            if first_page:
                first_page.is_first = False
                first_page.save()
        self.object.save()
        return super(PageEditView,self).form_valid(form)


@login_required
def page_delete(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    page.validateUser(request.user)
    page.delete()
    return redirect('chapter', novel_id=page.chapter.novel.id, chapter_id=page.chapter.id)


class SelectionCreateView(CreateView):
    form_class = SelectionForm
    template_name = 'novelpool/create_selection.html'
    context_object_name = 'selection'
    page = None
        
    def get(self, request, *args, **kwargs):
        self.page = get_object_or_404(Page, novel__id=self.kwargs['novel_id'], id=self.kwargs['page_id'])
        self.page.validateUser(self.request.user)
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.page = get_object_or_404(Page, novel__id=self.kwargs['novel_id'], id=self.kwargs['page_id'])
        self.page.validateUser(self.request.user)
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.page = self.page
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['novel'] = self.page.novel
        context['page'] = self.page
        return context
    

class SelectionEditView(UpdateView):
    form_class = SelectionForm
    template_name = 'novelpool/create_selection.html'
    context_object_name = 'selection'

    def get_object(self, queryset=None):
        selection = get_object_or_404(Selection, id=self.kwargs['selection_id'], page__novel__id=self.kwargs['novel_id'], page_id=self.kwargs['page_id'])
        selection.validateUser(self.request.user)
        return selection
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['novel'] = self.get_object().page.novel
        context['page'] = self.get_object().page
        return context


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


class TransitionCreateView(CreateView):
    form_class = TransitionForm
    template_name = 'novelpool/create_transition.html'
    context_object_name = 'transition'
    page_from = None
    selection = None
    
    def get(self, request, *args, **kwargs):
        self.page_from = get_object_or_404(Page, novel__id=self.kwargs['novel_id'], id=self.kwargs['page_id'])
        self.page_from.validateUser(self.request.user)
        if('selection_id' in self.kwargs):
            self.selection = get_object_or_404(Selection, id=self.kwargs['selection_id'], page__novel__id=self.page_from.novel.id, page=self.page_from)
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.page_from = get_object_or_404(Page, novel__id=self.kwargs['novel_id'], id=self.kwargs['page_id'])
        self.page_from.validateUser(self.request.user)
        if('selection_id' in self.kwargs):
            self.selection = get_object_or_404(Selection, id=self.kwargs['selection_id'], page__novel__id=self.page_from.novel.id, page=self.page_from)
            data = request.POST.copy()
            data['selection'] = self.selection
            request.POST = data.copy()
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.selection:
            self.object.selection = self.selection
        self.object.page_from = self.page_from
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['page_to'].queryset = Page.objects.filter(novel=self.page_from.novel).exclude(id=self.page_from.id).all()
        context['form'].fields['selection'].queryset = Selection.objects.filter(page=self.page_from).all()
        if self.selection:
            context['form'].fields['selection'].disabled = True 
            context['form'].fields['selection'].required = False
        return context
    
    def get_initial(self, *args, **kwargs):
        initial = super(TransitionCreateView, self).get_initial(**kwargs)
        if self.selection:
            initial['selection'] = self.selection
        return initial


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
