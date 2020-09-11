try: 
    from .middleware import NlpMiddleware 
except: 
    
    def NlpMiddleware(get_response) :
        def _middleware(request): 
            context = {
                'q': None, 
                'message': 'NLP model\'s not loaded.'
            }
            request.context = context 
            return get_response(request)
        return _middleware