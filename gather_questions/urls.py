from django.urls import path 

from . import views 

app_name = 'gather_questions'
urlpatterns = [
    path("", views.index, name='index'), 
    path("submit", views.submit_question, name='submit'), 
    path("download", views.download, name='download')
]