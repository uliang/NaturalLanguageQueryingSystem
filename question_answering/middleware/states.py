from enum import Enum 


class states(Enum): 
    OK =                            (1, None, None)
    ERROR =                         (0, None, None) 
    NO_URL_PARAM =                  (-1, None, 'ERROR') 
    INVALID_FORM =                  (-2, None, 'ERROR')
    NO_MODEL =                      (-3, 'No model loaded', 'ERROR')
    UNRECOGNIZED =                  (-4, 'Unrecognized question', 'ERROR')
    NO_RECORDS_FOUND =              (-5, 'Data not found', 'ERROR')
    
    def __init__(self, code, error_message, parent): 
        self.data = None
        self.code = code 
        self.error_message = error_message
        self.parent = None 
        
        cls = self.__class__
        if parent:  
            self.parent = cls[parent]