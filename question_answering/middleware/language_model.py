import spacy 
from django.conf import settings


# Initialize language model 
try: 
    nlp = spacy.load(settings.LANG_MODEL)
except(ImportError, OSError) : 
    nlp = None
