from django.urls import path, include
from novelpoolapp.views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('tutorial/', tutorial, name='tutorial'),
    path('novel/<int:novel_id>/read/<int:page_id>/', read, name='read'),
    #Novel
    path('novel/<int:novel_id>/', login_required(NovelView.as_view()), name='novel'),
    path('create/novel/', login_required(NovelCreateView.as_view()), name='create_novel'),
    path('edit/novel/<int:novel_id>/', login_required(NovelEditView.as_view()), name='edit_novel'),
    path('delete/novel/<int:novel_id>/', novel_delete, name='novel_delete'),
    #Chapter
    path('create/novel/<int:novel_id>/chapter/', login_required(ChapterCreateView.as_view()), name='create_chapter'),
    path('edit/novel/<int:novel_id>/chapter/<int:chapter_id>/', login_required(ChapterEditView.as_view()), name='edit_chapter'),
    path('novel/<int:novel_id>/chapter/<int:chapter_id>/', login_required(ChapterView.as_view()), name='chapter'),
    path('delete/chapter/<int:chapter_id>/', chapter_delete, name='delete_chapter'),
    #Page
    path('create/novel/<int:novel_id>/page/', login_required(PageCreateView.as_view()), name='create_page'),
    path('create/novel/<int:novel_id>/chapter/<int:chapter_id>/page/', login_required(PageCreateView.as_view()), name='create_page_with_chapter'),
    path('edit/novel/<int:novel_id>/page/<int:page_id>/', login_required(PageEditView.as_view()), name='edit_page'),
    path('novel/<int:novel_id>/page/<int:page_id>/', login_required(PageView.as_view()), name='page'),
    path('delete/page/<int:page_id>/', page_delete, name='delete_page'),
    #Selection
    path('create/novel/<int:novel_id>/page/<int:page_id>/selection/', login_required(SelectionCreateView.as_view()), name='create_selection'),
    path('edit/novel/<int:novel_id>/page/<int:page_id>/selection/<int:selection_id>/', login_required(SelectionEditView.as_view()), name='edit_selection'),
    path('novel/<int:novel_id>/page/<int:page_id>/selection/<int:selection_id>/', login_required(SelectionView.as_view()), name='selection'),
    path('delete/selection/<int:selection_id>/', selection_delete, name='delete_selection'),
    #Transition
    path('create/novel/<int:novel_id>/page/<int:page_id>/selection/<int:selection_id>/transition/', login_required(TransitionCreateView.as_view()), name='create_transition_with_selection'),
    path('create/novel/<int:novel_id>/page/<int:page_id>/transition/', login_required(TransitionCreateView.as_view()), name='create_transition'),
    path('edit/novel/<int:novel_id>/page/<int:page_id>/transition/<int:transition_id>/', transition_edit_or_create, name='edit_transition'),
    path('novel/<int:novel_id>/page/<int:page_id>/transition/<int:transition_id>/', login_required(TransitionView.as_view()), name='transition'),
    path('delete/transition/<int:transition_id>/', transition_delete, name='delete_transition'),
    #Profiles
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', login_required(ProfileView.as_view()), name='profile'),
    path('register/', register, name='register')
]