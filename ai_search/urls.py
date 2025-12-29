from django.urls import path
from . import views

app_name = 'ai_search'

urlpatterns = [
    path('', views.ai_search_view, name='search'),
]
