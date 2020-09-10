import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Question


# Create your views here.

def index(request) : 
    context = {'question_count': Question.count()}
    return render(request, "gather_questions/index.html", context)

def submit_question(request) : 
    try: 
        question_text = request.POST['question']
    except KeyError :
        return HttpResponseRedirect(reverse('gather_questions:index'))
    else:
        if len(question_text): 
            question = Question(question_text=question_text)
            question.save()
        return HttpResponseRedirect(reverse('gather_questions:index'))

def download(request) : 
    offset = request.GET.get('offset', 0)
        
    response = HttpResponse(content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="questions.jsonl"'
    Question.write_questions(response, offset)
    return response