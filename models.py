from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Quiz(models.Model):
    title = models.CharField(max_length=60, blank=False, )

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"

    def __unicode__(self):
        return self.title


class Question(models.Model):
    quiz = models.ManyToManyField(Quiz, blank=True, )

    content = models.CharField(max_length=1000, blank=False,
                               help_text="Enter the question text that you want displayed", verbose_name='Question', )



    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        # ordering = ['category']

    def __unicode__(self):
        return self.content



class Response(models.Model):
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    question = models.ForeignKey(Question,on_delete=models.PROTECT)
    free_response = models.TextField(max_length=2000, blank=True)
    score = models.PositiveIntegerField(validators=[MaxValueValidator(10),MinValueValidator(0)],blank=True,null=True)
    def __unicode__(self):
            return self.free_response
