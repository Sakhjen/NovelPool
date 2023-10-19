from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden
from .models import *
from.forms import NovelForm, ChapterForm, PageForm, SelectionForm, TransitionForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required

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


def index(request):
    novels = Novel.objects.all()
    context={
        'novels':novels,
        'user':request.user
    }
    return render(request, 'novelpool/index.html', context)


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


@login_required
def novel(request, novel_id):
    novel = Novel.objects.filter(id=novel_id).first()
    user = request.user
    isOwner = novel.getOwner() == user
    context = {
        'novel':novel,
        'isOwner':isOwner
    }
    return render(request, 'novelpool/novel.html', context=context)


@login_required
def create_novel(request):
    if request.method == 'POST':
        data = request.POST.copy()
        data['owner'] = request.user
        form = NovelForm(data)
        if form.is_valid():
            novel = form.save()
            return redirect('novel', novel_id=novel.id)

    form = NovelForm()
    context = {
        'form':form,
        'user':request.user
    }
    return render(request, 'novelpool/create_novel.html', context)


@login_required
def create_chapter(request, novel_id):
    novel = Novel.objects.filter(id=novel_id).first()
    if request.user != novel.getOwner():
        return HttpResponseForbidden()
    if request.method == 'POST':
        data = request.POST.copy()
        data['novel'] = Novel.objects.filter(id=novel_id).first()
        form = ChapterForm(data)
        if form.is_valid():
            chapter = form.save()
            return redirect('chapter', novel_id=novel_id, chapter_id=chapter.id)
    
    form = ChapterForm()
    context = {
        'form':form,
        'novel': novel
    }
    return render(request, 'novelpool/create_chapter.html', context)
        
    
@login_required
def chapter(request, novel_id, chapter_id):
    novel = Novel.objects.filter(id=novel_id).first()
    chapter = Chapter.objects.filter(id=chapter_id).first()
    if request.user != chapter.getOwner():
        return HttpResponseForbidden()
    context = {
        'novel':novel,
        'chapter':chapter
    }
    return render(request, 'novelpool/chapter.html', context)


@login_required
def create_page(request, novel_id, chapter_id=None):
    novel = Novel.objects.filter(id=novel_id).first()
    if request.user != novel.getOwner():
        return HttpResponseForbidden()
    if request.method == 'POST':
        data = request.POST.copy()
        data['novel'] = Novel.objects.filter(id=novel_id).first()
        form = PageForm(data)

        if form.is_valid():
            page = form.save()
            return redirect('page', novel_id=novel_id, page_id=page.id)
    chapter = None
    if(chapter_id):
        chapter = Chapter.objects.filter(id=chapter_id).first()
    form = PageForm()
    form.fields['chapter'].queryset = Chapter.getQuerySetByNovelId(novel_id)
    context = {
        'novel':novel,
        'chapter':chapter,
        'form':form
    }
    return render(request, 'novelpool/create_page.html', context)


@login_required
def page(request, novel_id, page_id):
    novel = Novel.objects.filter(id=novel_id).first()
    page = Page.objects.filter(id=page_id).first()
    if request.user != page.getOwner():
        return HttpResponseForbidden()
    context = {
        'novel': novel,
        'page': page
    }
    return render(request, 'novelpool/page.html', context)


@login_required
def create_selection(request, novel_id, page_id):
    page = Page.objects.filter(id=page_id).first()
    if request.user != page.getOwner():
        return HttpResponseForbidden()
    if request.method == 'POST':
        data = request.POST.copy()
        data['page'] = page
        form = SelectionForm(data)
        if form.is_valid():
            selection = form.save()
            return redirect('selection', novel_id=novel_id, page_id=page_id, selection_id=selection.id)
    form = SelectionForm()
    context = {
        'page': page,
        'form': form
    }
    return render(request, 'novelpool/create_selection.html', context)


@login_required
def selection(request, novel_id, page_id, selection_id):
    novel = Novel.objects.filter(id=novel_id).first()
    page = Page.objects.filter(id=page_id).first()
    selection = Selection.objects.filter(id=selection_id).first()
    if request.user != selection.getOwner():
        return HttpResponseForbidden()
    context = {
        'novel':novel,
        'page':page,
        'selection':selection
    }
    return render(request, 'novelpool/selection.html', context)


@login_required
def create_transition(request, novel_id, page_id, selection_id=None):
    page_from = Page.objects.filter(id=page_id).first()
    selection = None
    if request.user != page_from.getOwner():
        return HttpResponseForbidden()
    if selection_id:
        selection = Selection.objects.filter(id=selection_id).first()
    if request.method == 'POST':
        data = request.POST.copy()
        data['page_from'] = page_from
        if selection:
            data['selection'] = selection
        
        form = TransitionForm(data)
        if form.is_valid():
            transition = form.save()
            return redirect('transition', novel_id=novel_id, page_id=page_id, transition_id=transition.id)
    novel = Novel.objects.filter(id=novel_id).first()
    form = TransitionForm()
    form.fields['page_to'].queryset = Page.objects.filter(novel=novel).exclude(id=page_id).all()
    form.fields['selection'].queryset = Selection.objects.filter(page=page_from).all()
    context = {
        'novel':novel,
        'page':page_from,
        'selection':selection,
        'form':form
    }
    
    return render(request, 'novelpool/create_transition.html', context)


@login_required
def transition(request, novel_id, page_id, transition_id):
    novel = Novel.objects.filter(id=novel_id).first()
    page_from = Page.objects.filter(id=page_id).first()
    transition = Transition.objects.filter(id=transition_id).first()
    if request.user != transition.getOwner():
        return HttpResponseForbidden()
    page_to = Page.objects.filter(id=transition.page_to.id).first()
    context = {
        'novel':novel,
        'transition':transition,
        'page_from':page_from,
        'page_to':page_to,
        'selection':transition.selection
    }
    return render(request, 'novelpool/transition.html', context)


@login_required
def profile(request):
    user = request.user
    novels = Novel.objects.filter(owner=user).all()
    context = {
        'user':user,
        'novels':novels
    }
    return render(request, 'novelpool/profile.html', context)
