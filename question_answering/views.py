from django.template.response import TemplateResponse

from .forms import QuestionForm

# Create your views here.

def index(request) :
    form = QuestionForm()
    # print(request.context)
    data_service = request.context 

    template_context = data_service.to_dict()  
    template_context.update(form=form)

    return TemplateResponse(request, 'question_answering/index.html', 
                            context=template_context)