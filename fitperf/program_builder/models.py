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
    programs = models.ManyToManyField('Program',
                                       through='Session',
                                       related_name='profiles',
                                       verbose_name="list of programs per user")
    trainings = models.ManyToManyField('Training',
                                        through='Session',
                                        related_name='profiles',
                                        verbose_name="list of trainings per user")
    exercises = models.ManyToManyField('Exercise',
                                        through='Session',
                                        verbose_name="list of exercises per user")
 
    def __str__(self):
        return self.user.username

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
                                        through='Session',
                                        related_name='programs',
                                        verbose_name='list of trainings per program')
    exercises = models.ManyToManyField('Exercise',
                                        through='Session',
                                        related_name='programs',
                                        verbose_name='list of exercises per program')

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
                                        through='Session',
                                        related_name='trainings',
                                        verbose_name='list of exercises per training')

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
                            choices=MOVEMENTS_SETTINGS)
    unity = models.CharField(max_length=5)

    def __str__(self):
        return self.name

class Movement(models.Model):
    """
    This class represents the movements created
    """
    name = models.CharField(max_length=50)
    equipment = models.CharField(max_length=20,
                                 null=True)
    founder = models.ForeignKey('Profile',
                                on_delete=models.CASCADE,
                                verbose_name="the movement's creator")
    settings = models.ManyToManyField('MovementSettings',
                                     related_name='movements',
                                     verbose_name="list of settings")

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

class Session(models.Model):
    """
    This class linked all the different elements to create a unique activity.
    The idea is to get an exercise which is linked to a training, also linked
    to a program and which is realized by a specific user.
    """
    user = models.ForeignKey('Profile',
                             on_delete=models.CASCADE)
    program = models.ForeignKey('Program',
                                on_delete=models.CASCADE)
    training = models.ForeignKey('Training',
                                 on_delete=models.CASCADE)
    exercise = models.ForeignKey('Exercise',
                                on_delete=models.CASCADE)
    date = models.DateTimeField()
    challenge = models.BooleanField(default=False)
    done = models.BooleanField(default=False)
    performance = models.DecimalField(max_digits=5, 
                                     decimal_places=1,
                                     null=True)