from django.template.response import TemplateResponse

from .forms import QuestionForm


# Create your views here.

def index(request) :
    form = QuestionForm()
    # print(request.context)
    payload, state = request.context 
    context = { 
        'form': form, 
        'answer': payload, 
        'question': state.get('q', None)
    }

    return TemplateResponse(request, 'question_answering/index.html', context=context)