import attr
from tidbits.monads import State

from .decls import chain, Status

@attr.s
class NlpMiddleware: 
    
    get_response = attr.ib()
        
    def __call__(self, request) : 

        context = State.unit(None).pipe(*chain).run_state({ 
                'status': Status.NEW, 
                'url_param': request.GET })
        
        request.context = context            
        
        return self.get_response(request)

   
    def process_template_response(self, request, response) : 
        payload, state = request.context
        if state['status'] is Status.INVALID : 
            response.context_data.update(dict(form=payload))
        return response