from django.urls import path 

from . import views 

app_name = 'question_answering' 
urlpatterns = [
    path("", views.index, name='index')
]