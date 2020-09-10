import json 

from django.db import models
from django.db.models import Count 

# Create your models here.


class Question(models.Model) : 
    question_text = models.CharField(max_length=500) 
    date_asked = models.DateTimeField('date asked', auto_now_add=True)
    
    @classmethod
    def count(cls) : 
        return cls.objects.count()

    @classmethod 
    def write_questions(cls, filelike, offset=0) :
        offset = int(offset)
        for q in cls.objects.all()[offset:] :
            line = {"text": q.question_text}
            filelike.write(json.dumps(line)+ "\n")

    def __str__(self) : 
        return self.question_text