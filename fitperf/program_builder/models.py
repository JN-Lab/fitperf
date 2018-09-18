from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Profile(models.Model):
    """
    This class inherits from User model.
    It adds the different relations between the user and his programs, trainings
    and exercises.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
 
    def __str__(self):
        return self.user.username

class Session(models.Model):
    user = models.ForeignKey('Profile',
                             on_delete=models.CASCADE,
                             verbose_name="user who does the session")
    program = models.ForeignKey('Program', 
                                on_delete=models.CASCADE,
                                null=True,
                                verbose_name="program linked to the session if exists")
    training = models.ForeignKey('Training',
                                on_delete=models.CASCADE,
                                verbose_name="training associated to the session")
    date = models.DateTimeField(default=timezone.now)
    done = models.BooleanField(default=False)

    exercises = models.ManyToManyField('Exercise',
                                        through='ExercisesPerSession',
                                        related_name='sessions',
                                        verbose_name="list of exercises per session")
    
    def __str__(self):
        return self.training + "-"  + self.date

class ExercisesPerSession(models.Model):
    exercise = models.ForeignKey('Exercise',
                                 on_delete=models.CASCADE)
    session = models.ForeignKey('Session',
                                 on_delete=models.CASCADE)
    challenge = models.BooleanField(default=False)
    performance = models.DecimalField(max_digits=5, 
                                     decimal_places=1,
                                     null=True)

    def __str__(self):
        return self.session + "-" + self.exercise

class Program(models.Model):
    """
    This class represents the programs created.
    """
    name = models.CharField(max_length=200)
    description = models.TextField(null=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    founder = models.ForeignKey('Profile', 
                                on_delete=models.CASCADE,
                                 verbose_name="the program's creator")
    trainings = models.ManyToManyField('Training',
                                        related_name='programs',
                                        verbose_name='list of trainings per program')
    def __str__(self):
        return self.name

class Training(models.Model):
    """
    This class represents the trainings created
    """
    name = models.CharField(max_length=200)
    founder = models.ForeignKey('Profile', 
                                on_delete=models.CASCADE, 
                                verbose_name="the training's creator")
    exercises = models.ManyToManyField('Exercise',
                                        related_name='trainings',
                                        verbose_name='list of exercises per training')

    def __str__(self):
        return self.name

class Exercise(models.Model):
    """
    This class represents the exercises created
    """
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
    founder = models.ForeignKey('Profile', 
                                on_delete=models.CASCADE,
                                verbose_name="the execise's creator")
    movements = models.ManyToManyField('Movement',
                                      through='MovementsPerExercise', 
                                      related_name='exercises',
                                      verbose_name="list of movements per exercise")

    def __str__(self):
        return self.name

class MovementsPerExercise(models.Model):
    """
    This class represents the movements per exercise.
    This is an association table between exercises and movements
    where we add the setting value (number of repetitions, etc...)
    """
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

class Movement(models.Model):
    """
    This class represents the movements created
    """
    name = models.CharField(max_length=50, 
                            unique=True)
    equipment = models.ForeignKey('Equipment',
                                on_delete=models.CASCADE,
                                verbose_name="the movement's equipment")
    founder = models.ForeignKey('Profile',
                                on_delete=models.CASCADE,
                                verbose_name="the movement's creator")
    settings = models.ManyToManyField('MovementSettings',
                                     related_name='movements',
                                     verbose_name="list of settings")

    def __str__(self):
        return self.name

class MovementSettings(models.Model):
    """
    This class represents the different settings a movement can be
    associated with.
    """
    MOVEMENTS_SETTINGS = (
        ('REP', 'Repetitions'),
        ('WEIGTH', 'Poids'),
        ('DISTANCE', 'Distance'),
    )
    name = models.CharField(max_length=20,
                            choices=MOVEMENTS_SETTINGS,
                            unique=True)
    unity = models.CharField(max_length=5)

    def __str__(self):
        return self.name

class Equipment(models.Model):
    name = models.CharField(max_length=20,
                            unique=True)

    founder = models.ForeignKey('Profile',
                                on_delete=models.CASCADE,
                                verbose_name="the movement's creator")