from django.db import models
from django.conf import settings

from django.contrib.auth.models import User

import random

# Create your models here.


class Person(models.Model):
    nome = models.CharField(max_length=25, verbose_name='Name')
    apelido = models.CharField(max_length=25, verbose_name='Surname')
    email = models.EmailField(verbose_name='Email')

    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'


class Contacto(models.Model):
    nome = models.CharField(max_length=25, verbose_name='Name')
    apelido = models.CharField(max_length=25, verbose_name='Surname')
    email = models.EmailField(verbose_name='Email')
    telefone = models.CharField(max_length=20, verbose_name='Telephono')
    data_de_nacimento = models.DateField(verbose_name='Birth Date')
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.nome} {self.apelido}'

    class Meta:
        verbose_name = 'contacto'
        verbose_name_plural = 'contactos'


class Pregunta(models.Model):

    possible_answer = 1
    text = models.TextField(verbose_name='Texto de la Pregunta')
    max_score = models.DecimalField(
        verbose_name='Maximo Puntaje', default=3, decimal_places=2, max_digits=6)

    def __str__(self):
        return self.text


class Respuesta(models.Model):

    answer_number = 4

    question = models.ForeignKey(
        Pregunta, related_name="options", on_delete=models.CASCADE)
    correct = models.BooleanField(
        verbose_name="Esta Pregunta es Correcta?", default=False, null=False)
    text = models.TextField(verbose_name="Texto de la Respuesta")

    def __str__(self):
        return self.text


class QuizUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score_obtained = models.DecimalField(
        verbose_name="Puntaje Total", default=0, decimal_places=2, max_digits=10)

    def create_attempts(self, question):
        attempt = PreguntasRespondidas(question=question, quiz_user=self)
        attempt.save()

    def get_new_questions(self):
        answered = PreguntasRespondidas.objects.filter(
            quiz_user=self).values_list('question__pk', flat=True)
        remaining_questions = Pregunta.objects.exclude(pk__in=answered)
        if not remaining_questions.exists():
            return None
        return random.choice(remaining_questions)

    def validate_attempt(self, questions_answered, selected_answer):
        if questions_answered.question_id != selected_answer.question_id:
            return False
        questions_answered.selected_answer = selected_answer.question_id
        if selected_answer.correct:
            questions_answered.correct = True
            questions_answered.score_obtained = selected_answer.question.max_score
            questions_answered.answer = selected_answer
        else:
            questions_answered.answer = selected_answer

        questions_answered.save()

    def update_score(self):
        updated_score = self.attempts.filter(correct=True).aggregate(
            models.Sum("score_obtained"))["score_obtained__sum"]
        self.score_obtained = updated_score
        self.save()

class PreguntasRespondidas(models.Model):
    quiz_user = models.ForeignKey(
        QuizUsuario, on_delete=models.CASCADE, related_name="attempts")
    question = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    answer = models.ForeignKey(Respuesta, on_delete=models.CASCADE, null=True)
    correct = models.BooleanField(
        verbose_name="Esta Pregunta es Correcta?", default=False, null=False)
    score_obtained = models.DecimalField(
        verbose_name="Puntaje Obtenido", default=0, decimal_places=2, max_digits=6)

    def __str__(self):
        return self.question



class Quiz(Person):
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'quiz'
        verbose_name_plural = 'quizzes'
