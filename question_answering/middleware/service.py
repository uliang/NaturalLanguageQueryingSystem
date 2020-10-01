import attr 
from collections import defaultdict
from functools import wraps 
from inspect import isfunction

from .states import states


@attr.s
class _ErrorHandling: 
    error_code = attr.ib()

    def __call__(self, f): 
        @wraps(f)
        def wrapper(obj, *args, **kwargs): 
            if not obj.in_state(self.error_code): 
                return f(obj, *args, **kwargs)
            else: 
                return obj
        return wrapper


@attr.s
class _Logging: 
    enable = attr.ib(default=True)
    def __call__(self, f): 
        @wraps(f)
        def wrapper(obj, *args, **kwargs): 
            input_ = obj.data
            result = f(obj, *args, **kwargs) 
            if self.enable: 
                if isinstance(result, obj.__class__):
                    output = result.data
                    print(f"{f.__name__} called: {input_} => {output} current state: {result.current_state}")
                else: 
                    print(f"{f.__name__} called: {result}")
            return result
        return wrapper 


class _ServiceMeta(type): 
    def __new__(cls, name, bases, namespace, logging_enabled=False, log_methods=None): 
        error_handling_decorator = _ErrorHandling(states.ERROR)
        logging_decorator = _Logging(logging_enabled) 

        decorated_methods = {}
        for name, method in namespace.items(): 
            if "_skip_if_error_" in namespace: 
                if name in namespace["_skip_if_error_"]: 
                    method = error_handling_decorator(method)
            if log_methods: 
                if name in log_methods: 
                    method = logging_decorator(method) 
            decorated_methods.update({name:method})

        namespace.update(decorated_methods)
        obj = super().__new__(cls, name, bases, namespace)
        return obj


@attr.s
class Service(metaclass=_ServiceMeta, 
              logging_enabled=True, 
              log_methods=["bind"]): 
   
    _skip_if_error_ = [
        'maybe', 'map_', 'filter_', 'assign',
        'bind'
    ]
    initial_state = attr.ib() 
    cache = attr.ib(init=False, factory=dict)
    data = attr.ib(init=False)

    def __attrs_post_init__(self):
        self.current_state = self.initial_state

    def handle_error(self, error_code):
        self.current_state = error_code 
        self.cache['error'] = self.current_state.error_message
        return self 

    def maybe(self, f, error_code): 
        try:
            return self.map_(f)
        except :
            return self.handle_error(error_code)

    def of_(self, data):
        self.data = data 
        return self

    def map_(self, f): 
        self.data = f(self.data) 
        return self 

    def filter_(self, cond, error_code): 
        if not cond(self.data): 
            self.handle_error(error_code)
        return self 

    def assign(self, fieldname): 
        self.cache.update({fieldname:self.data})
        return self 

    def bind(self, f, data_from): 
        value = self.cache[data_from]
        effect = f(value)
        self.data = effect(self.data)
        return self 

    def to_dict(self):         
        return defaultdict(lambda: None, **self.cache)

    def in_state(self, state): 
        this_state = self.current_state
        
        if this_state is state: 
            return True 

        while this_state.parent:
            if this_state.parent is state: 
                return True 
            this_state = state.parent
        return False  
