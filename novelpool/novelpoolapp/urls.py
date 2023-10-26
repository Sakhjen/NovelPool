from django.urls import path, include
from novelpoolapp.views import *

urlpatterns = [
    path('', index, name='index'),
    path('tutorial/', tutorial, name='tutorial'),
    path('novel/<int:novel_id>/read/<int:page_id>/', read, name='read'),
    #Novel
    path('novel/<int:novel_id>/', novel, name='novel'),
    path('create/novel/', novel_edit_or_create, name='create_novel'),
    path('edit/novel/<int:novel_id>/', novel_edit_or_create, name='edit_novel'),
    path('delete/novel/<int:novel_id>/', novel_delete, name='novel_delete'),
    #Chapter
    path('create/novel/<int:novel_id>/chapter/', chapter_edit_or_create, name='create_chapter'),
    path('edit/novel/<int:novel_id>/chapter/<int:chapter_id>/', chapter_edit_or_create, name='edit_chapter'),
    path('novel/<int:novel_id>/chapter/<int:chapter_id>/', chapter, name='chapter'),
    path('delete/chapter/<int:chapter_id>/', chapter_delete, name='delete_chapter'),
    #Page
    path('create/novel/<int:novel_id>/page/', page_edit_or_create, name='create_page'),
    path('edit/novel/<int:novel_id>/page/<int:page_id>/', page_edit_or_create, name='edit_page'),
    path('novel/<int:novel_id>/page/<int:page_id>/', page, name='page'),
    path('delete/page/<int:page_id>/', page_delete, name='delete_page'),
    #Selection
    path('create/novel/<int:novel_id>/page/<int:page_id>/selection/', selection_edit_or_create, name='create_selection'),
    path('edit/novel/<int:novel_id>/page/<int:page_id>/selection/<int:selection_id>/', selection_edit_or_create, name='edit_selection'),
    path('novel/<int:novel_id>/page/<int:page_id>/selection/<int:selection_id>/', selection, name='selection'),
    path('delete/selection/<int:selection_id>/', selection_delete, name='delete_selection'),
    #Transition
    path('create/novel/<int:novel_id>/page/<int:page_id>/selection/<int:selection_id>/transition/', transition_edit_or_create, name='create_transition_with_selection'),
    path('create/novel/<int:novel_id>/page/<int:page_id>/transition/', transition_edit_or_create, name='create_transition'),
    path('edit/novel/<int:novel_id>/page/<int:page_id>/transition/<int:transition_id>/', transition_edit_or_create, name='edit_transition'),
    path('novel/<int:novel_id>/page/<int:page_id>/transition/<int:transition_id>/', transition, name='transition'),
    path('delete/transition/<int:transition_id>/', transition_delete, name='delete_transition'),
    #Profiles
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', profile, name='profile'),
    path('register/', register, name='register')
]