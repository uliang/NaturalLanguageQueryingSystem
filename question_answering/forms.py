from django import forms
from django.core import validators
from django.core.exceptions import ValidationError



class QuestionForm(forms.Form) : 
    q = forms.CharField(label='Question', required=True, validators=[
        validators.MinLengthValidator(5), 
        validators.MaxLengthValidator(500),
    ])
    q.widget.attrs.update({ 
        'class': 'field', 
        'placeholder': 'Ask a salary scale related question ...',
        'required': False })