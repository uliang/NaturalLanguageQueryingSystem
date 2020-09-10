import enum 
import typing as typ 
from contextlib import suppress
from string import Template 

import attr 

# Type aliases
Environment = typ.Dict[str, typ.Any]

# Question categories 
UNRECOGNIZED            = 'Unrecognized'
SALARY                  = 'Salary'


class States(enum.Enum) : 
    NEW     = 1
    INVALID = 2
    FINAL   = 3


@attr.s(auto_attribs=True)
class State: 
    """
    Particular implementation of the state monad.
    """
    _environ: Environment
    _state: States = attr.ib(default=States.NEW, init=False)

    def bind(self, f) : 
        if any(self.state is st for st in [States.FINAL, States.INVALID]) : 
            return self 
        else :
            return f(self.environ)

    def get(self, key) : 
        return self._environ.get(key, None)

    @property
    def environ(self) -> Environment : 
        return self._environ

    @property 
    def state(self) -> States : 
        return self._state 

    def put(self, new_state) :
        if isinstance(new_state, States) : 
            self._state = new_state
            return self
        raise ValueError("Unknown state.")
    
    def __or__(self, f) : 
        return self.bind(f)


# Operations 


def modify(replacement:States) :
    def _modify(env:Environment) -> State : 
        return State(env).put(replacement)
    return _modify

def update(new_dict:typ.Dict) : 
    def _update(env:Environment) -> State : 
        new_env = dict(env)
        new_env.update(new_dict)
        return State(new_env)
    return _update

@attr.s(auto_attribs=True)
class ValidateForm: 
    form_field:str 

    def __call__(self, env:Environment) -> State : 
        form = env[self.form_field]
        if not form.is_valid() : 
            return State(env) | modify(States.INVALID)

        return State(env)

@attr.s(auto_attribs=True) 
class ExtractFormData: 
    form_field:str 

    def __call__(self, env:Environment) -> State : 
        return State(env) | update(env[self.form_field].cleaned_data)


@attr.s 
class ApplyNlp: 
    nlp = attr.ib() 
    data_field:str = attr.ib()

    def __call__(self, env:Environment) -> State : 
        with suppress(KeyError) : 
            doc = self.nlp(env[self.data_field])
            return State(env) | update({
                'qtype': doc._.qtype, 
                'kb_ident': doc._.kb_ident, 
            })
        return State(env) | modify(States.FINAL)

def SetUnrecognizedMsg(msg:str) : 
    def _setter(env:Environment) -> State : 
        if env['qtype'] == UNRECOGNIZED : 
            return State(env) | update({ 'message': msg }) | modify(States.FINAL)
        return State(env)
    return _setter

@attr.s
class FindAnswer: 
    models = attr.ib()

    def __call__(self, env:Environment) -> State : 
        with suppress(KeyError) : 
            return State(env) | update({ 
                'result' : self.models.__dict__[env['qtype']].find_answer(env['kb_ident']) 
            }) 
        return State(env)

@attr.s(auto_attribs=True)
class SetRecordNotFound: 
    msg:str

    def __call__(self, env:Environment) -> State : 
        if env['result'] is None : 
            return State(env) | update({ 'message' : self.msg }) | modify(States.FINAL)
        return State(env)  

@attr.s(auto_attribs=True) 
class SetAnswer:
    msg_template: Template
    substitution_schema: typ.Dict[str, str]

    def __call__(self, env:Environment) -> State : 
        if result := env['result'] :
            result_schema = { key: getattr(result, val) for key,val in self.substitution_schema.items() }
            return State(env) | update({ 
                'message': self.msg_template.substitute(**result_schema)
            }) | modify(States.FINAL)
        return State(env)
