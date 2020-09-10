from django.template.response import TemplateResponse

from .forms import QuestionForm


# Create your views here.

def index(request) :
    form = QuestionForm()
    context = { 
        'form': form, 
        'answer': request.context.get('message'), 
        'question': request.context.get('q')
    }

    return TemplateResponse(request, 'question_answering/index.html', context=context)