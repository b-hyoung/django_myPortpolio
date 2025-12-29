from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='notes_index'),
    path('note/<int:note_id>/', views.note_detail, name='note_detail'),
]

