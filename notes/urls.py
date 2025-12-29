from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.index, name='notes_index'),
    path('tag/<str:tag_name>/', views.index, name='tagged_notes'),
    path('note/<int:note_id>/', views.note_detail, name='note_detail'),
    path('api/notes/<int:note_id>/', views.note_content_api, name='note_content_api'),

    path('new/', views.create_note, name='create_note'),
]