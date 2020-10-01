from collections import namedtuple 
from unittest.mock import MagicMock


_fake_ext = namedtuple('_', ['qtype', 'kb_ident']) 

class FakeDoc:
    def __init__(self, text, qtype, kb_ident): 
        self._ = _fake_ext(qtype, kb_ident) 
        self.text = text 

    def __str__(self): 
        return f"<[MOCKED NLP]{self.text}>"
