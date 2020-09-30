from pydoc import locate


def table_loader(table_name): 
    model = locate(f'question_answering.models.{table_name}')
    if model:
        return model 
    raise ImportError("Unrecognized table name")