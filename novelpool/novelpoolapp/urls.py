from django.urls import path, include
from novelpoolapp.views import *

urlpatterns = [
    path('', index, name='index'),
    path('tutorial/', tutorial, name='tutorial'),
    path('novel/<int:novel_id>/', novel, name='novel'),
    path('novel/<int:novel_id>/read/<int:page_id>/', read, name='read'),
    path('create/novel/', create_novel, name='create_novel'),
    path('create/<int:novel_id>/chapter/', create_chapter, name='create_chapter'),
    path('novel/<int:novel_id>/chapter/<int:chapter_id>', chapter, name='chapter'),
    path('create/<int:novel_id>/page/', create_page, name='create_page'),
    path('novel/<int:novel_id>/page/<int:page_id>/', page, name='page'),
    path('create/<int:novel_id>/page/<int:page_id>/selection/', create_selection, name='create_selection'),
    path('novel/<int:novel_id>/page/<int:page_id>/selection/<int:selection_id>/', selection, name='selection'),
    path(r'create/<int:novel_id>/page/<int:page_id>/transition/<int:selection_id>/', create_transition, name='create_transition_with_selection'),
    path(r'create/<int:novel_id>/page/<int:page_id>/transition/', create_transition, name='create_transition'),
    path('novel/<int:novel_id>/page/<int:page_id>/transition/<int:transition_id>/', transition, name='transition'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', profile, name='profile')
]