import spacy 
from django.conf import settings


# Initialize language model 
try: 
    if settings.LANG_MODEL != 'none':   
        nlp = spacy.load(settings.LANG_MODEL)
    else:
        raise ImportError
except(ImportError, OSError) : 
    def nlp(text):
        raise NotImplementedError
