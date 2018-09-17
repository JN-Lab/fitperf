from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add some custom parameters linked to your need

    def __str__(self):
        return self.user.username

class Program(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    founder = models.ForeignKey(User, 
                                on_delete=models.CASCADE,
                                 verbose_name="the program's creator")

    def __str__(self):
        return self.name

class Training(models.Model):
    name = models.CharField(max_length=200)
    founder = models.ForeignKey(User, 
                                on_delete=models.CASCADE, 
                                verbose_name="the training's creator")

    def __str__(self):
        return self.name

class MovementSettings(models.Model):
    MOVEMENTS_SETTINGS = (
        ('REP', 'Repetitions'),
        ('WEIGTH', 'Poids'),
        ('DISTANCE', 'Distance'),
    )
    name = models.CharField(max_length=20,
                            choices=MOVEMENTS_SETTINGS)
    unity = models.CharField(max_length=5)

    def __str__(self):
        return self.name

class Movement(models.Model):
    name = models.CharField(max_length=50)
    equipment = models.CharField(max_length=20,
                                 null=True)
    founder = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                verbose_name="the movement's creator")
    settings = models.ManyToManyField('MovementSettings',
                                     related_name='movements',
                                     verbose_name="list of settings")

    def __str__(self):
        return self.name

class Exercise(models.Model):
    EXERCISE_TYPE = (
        ('RUN', 'RUNNING'),
        ('FORTIME', 'FORTIME'),
        ('AMRAP', 'AMRAP'),
        ('WARMUP', 'ECHAUFFEMENT'),
        ('STRENGTH', 'FORCE'),
        ('EMOM', 'EMOM'),
        ('CONDITIONNING', 'CONDITIONNEMENT'),
        ('MAX_REP', 'MAXIMUM DE REPETITION')
    )
    PERFORMANCE_TYPE = (
        ('TIME', 'Temps'),
        ('NB_ROUNDS', 'Nombre de tours'),
        ('NB_REP', 'Nombre de repetitions'),
    )
    name = models.CharField(max_length=200)
    exercise_type = models.CharField(max_length=20, 
                                     choices=EXERCISE_TYPE)
    performance_type = models.CharField(max_length=20, 
                                        null=True,
                                        choices=PERFORMANCE_TYPE)
    founder = models.ForeignKey(User, 
                                on_delete=models.CASCADE,
                                verbose_name="the execise's creator")
    movements = models.ManyToManyField('Movement',
                                      through='MovementsPerExercise', 
                                      related_name='exercises',
                                      verbose_name="list of movements per exercise")

    def __str__(self):
        return self.name

class MovementsPerExercise(models.Model):
    exercise = models.ForeignKey('Exercise',
                                 on_delete=models.CASCADE)
    movement = models.ForeignKey('Movement',
                                 on_delete=models.CASCADE)
    movement_setting = models.ForeignKey('MovementSettings',
                                         on_delete=models.CASCADE)
    setting_value = models.DecimalField(max_digits=5, 
                                        decimal_places=1)

    def __str__(self):
        return self.exercise + " / " + self.movement