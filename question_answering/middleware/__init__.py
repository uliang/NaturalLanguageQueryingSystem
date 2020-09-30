import attr
from operator import itemgetter, methodcaller, attrgetter

from django.conf import settings

import spacy

from .service import Service
from .states import states
from .language_model import nlp
from .loaders import table_loader
from ..forms import QuestionForm


@attr.s
class NlpMiddleware: 
    get_response = attr.ib()
    
    def __call__(self, request) : 

        data_service = Service(initial_state=states.OK)
        (
            data_service.of_(request.GET)
                .filter_(lambda qd: 'q' in qd , error_code=states.NO_URL_PARAM) 
                .map_(QuestionForm)
                .assign(fieldname='form') 
                .filter_(methodcaller('is_valid'), 
                    error_code=states.INVALID_FORM) 
                .map_(attrgetter('cleaned_data')) 
                .map_(itemgetter('q')) 
                .assign(fieldname='question') 
                .maybe(nlp, error_code=states.NO_MODEL) 
                .assign(fieldname='document') 
                .map_(lambda doc: doc._.qtype) 
                .maybe(table_loader, error_code=states.UNRECOGNIZED) 
                .bind(lambda doc: methodcaller('find_answer', doc._.kb_ident),
                        data_from='document') 
                .maybe(lambda result: f"${result.min_pay} to ${result.max_pay}", 
                        error_code=states.NO_RECORDS_FOUND) 
                .assign(fieldname='answer') 
        )
        request.context = data_service 
        
        return self.get_response(request)

    def process_template_response(self, request, response) : 
        data_service = request.context
        
        if data_service.in_state(states.INVALID_FORM) : 
            response.context_data.update(**data_service.to_dict())
        
        return response
