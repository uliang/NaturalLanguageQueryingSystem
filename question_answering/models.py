from django.db import models



# Create your models here.

class Salary(models.Model) :
    grade = models.CharField(max_length=20)
    min_pay = models.IntegerField("minimum salary") 
    max_pay = models.IntegerField("maximum salary")

    @classmethod 
    def find_answer(cls, kb_ident) : 
        qs = cls.objects.filter(grade__contains=kb_ident)
        answer = qs[0] if qs.count() else None
        return answer

    def __str__(self) :
        return "{}".format(self.grade)

