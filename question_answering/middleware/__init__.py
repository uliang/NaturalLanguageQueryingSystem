import typing as typ
from string import Template

import attr

import spacy

import question_answering.models as models 

from ..forms import QuestionForm
from .monad import (State, ValidateForm, ExtractFormData, ApplyNlp, 
                    SetUnrecognizedMsg, SetAnswer, SetRecordNotFound, 
                    FindAnswer, States)


class NlpMiddleware: 

    nlp = spacy.load('en_hr_questions')

    def __init__(self, get_response) : 
        self.get_reponse = get_response 

    def __call__(self, request) : 
        request.context = State({ 'form': QuestionForm(request.GET) }) \
            | ValidateForm('form') \
            | ExtractFormData('form') \
            | ApplyNlp(self.nlp, 'q') \
            | FindAnswer(models) \
            | SetUnrecognizedMsg('Sorry, I do not understand this question. Please ask another question.') \
            | SetRecordNotFound('Unable to retrieve salary records.') \
            | SetAnswer(Template('$$$min_pay to $$$max_pay'), {'min_pay':'min_pay', 'max_pay':'max_pay'})

        return self.get_response(request)

    def process_template_response(self, request, response) : 
        if request.context.state is States.INVALID : 
            response.context_data.update(dict(form=request.context.get('form')))
        return response