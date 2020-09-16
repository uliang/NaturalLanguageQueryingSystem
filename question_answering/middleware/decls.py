import enum
import typing as typ
from string import Template
from contextlib import suppress

import attr
import spacy

from tidbits.monads import State, DoWhen

import question_answering.models as models 
from ..forms import QuestionForm

# Model name 
MODEL_NAME = 'en_hr_questions' 

# Question categories 
UNRECOGNIZED            = 'Unrecognized'
SALARY                  = 'Salary'

#Pipeline states
class Status(enum.Enum) : 
    NEW         = 1
    INVALID     = 2
    FINAL       = 3
    PROCESSING   = 5
    NO_MODEL    = 6
    NO_RESULT   = 7

# Initialize language model 
try: 
    model = spacy.load(MODEL_NAME)
except(ImportError, OSError) : 
    model = lambda _: None 

# Pipeline 
processing = lambda s: s['status'] is Status.PROCESSING

chain = [
    DoWhen(lambda s: 'q' in s['url_param'])
        (lambda t, s: (QuestionForm(s['url_param']), 
            { **s, 'status': Status.PROCESSING })) ,  

    DoWhen(processing)(lambda t, s: (t, { **s, 
            'status': Status.PROCESSING if t.is_valid() else Status.INVALID, 
            'form': t 
        })), 
    
    DoWhen(processing)(lambda t, s: (model(t.cleaned_data['q']), {
            **s, 
            'q': t.cleaned_data['q']
        })), 
    
    DoWhen(processing) (lambda t, s: (t, { **s, 
            'status': Status.PROCESSING if t else Status.NO_MODEL
        })), 

    DoWhen(lambda s: s['status'] is Status.NO_MODEL) (
        lambda t, s: ("No model present. Please install spacy model", s)),

    DoWhen(processing) (lambda t, s: (t, { **s, 
        'qtype': t._.qtype, 
        'kb_ident': t._.kb_ident
    })), 

    DoWhen(processing, lambda s: s['qtype'] == UNRECOGNIZED) (
        lambda t, s: ("Sorry, I do not understand this question. Please ask another question.", 
            { **s, 'status': Status.FINAL })), 

    DoWhen(processing, lambda s: s['qtype'] != UNRECOGNIZED) (
        lambda t, s: (models.__dict__[s['qtype']], s)),

    DoWhen(processing) (lambda t, s: (t.find_answer(s['kb_ident']), s)), 

    DoWhen(processing) (lambda t, s: (t, {**s, 
        'status': Status.PROCESSING if t else Status.NO_RESULT })), 

    DoWhen(lambda s: s['status'] is Status.NO_RESULT) (
        lambda t, s: ('Unable to retrieve salary records.', s)), 

    DoWhen(processing) (lambda t, s: ( f"${t.min_pay} to ${t.max_pay}", 
        { **s, 'status': Status.FINAL }))
]
