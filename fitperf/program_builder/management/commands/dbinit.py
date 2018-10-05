#! /usr/bin/env python3
# coding: utf-8
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ...models import Training, Exercise, MovementsPerExercise, MovementSettingsPerMovementsPerExercise, Movement, MovementSettings, Equipment

class DBinit:
    """
    This class creates all the objects by default for the program
    """

    def clean_db(self):
        """
        This method clean all the db
        """
        settings = MovementSettings.objects.all()
        if settings:
            settings.delete()
        
        equipments = Equipment.objects.all()
        if equipments:
            equipments.delete()
        
        movements = Movement.objects.all()
        if movements:
            movements.delete()
        
        exercises = Exercise.objects.all()
        if exercises:
            exercises.delete()

        mvts_per_exos = MovementsPerExercise.objects.all()
        if mvts_per_exos:
            mvts_per_exos.delete()

        settings_per_mvt_per_exo = MovementSettingsPerMovementsPerExercise.objects.all()
        if settings_per_mvt_per_exo:
            settings_per_mvt_per_exo.delete()

        trainings = Training.objects.all()
        if trainings:
            trainings.delete()

    def start(self):
        """
        This method creates all the necessary settings
        """
        founder = User.objects.get(username="juliennuellas")

        # We create the necessary settings
        rep = MovementSettings.objects.create(name=MovementSettings.REPETITIONS, founder=founder)
        weight = MovementSettings.objects.create(name=MovementSettings.WEIGHT, founder=founder)
        dist = MovementSettings.objects.create(name=MovementSettings.DISTANCE, founder=founder)
        cal = MovementSettings.objects.create(name=MovementSettings.CALORIES, founder=founder)
        lest = MovementSettings.objects.create(name=MovementSettings.LEST, founder=founder)

        # We create the necessary equipments
        kb = Equipment.objects.create(name="kettlebell", founder=founder)
        anyone = Equipment.objects.create(name="aucun", founder=founder)
        ball = Equipment.objects.create(name="wallball", founder=founder)
        drawbar = Equipment.objects.create(name="barre de traction", founder=founder)
        dipbar = Equipment.objects.create(name="barre à dips", founder=founder)
        rope = Equipment.objects.create(name="corde à sauter", founder=founder)
        ring = Equipment.objects.create(name="anneaux", founder=founder)
        box = Equipment.objects.create(name="box", founder=founder)
        vest = Equipment.objects.create(name="veste lestée", founder=founder)

        # We create some movements
        squat = Movement.objects.create(name="squats", founder=founder, equipment=kb)
        squat.settings.add(rep, lest)

        pushup = Movement.objects.create(name="pushups", founder=founder, equipment=anyone)
        pushup.settings.add(rep, lest)
        
        wallball = Movement.objects.create(name="wallballs", founder=founder, equipment=ball)
        wallball.settings.add(rep, lest)
        
        pullup = Movement.objects.create(name="pullups", founder=founder, equipment=drawbar)
        wallball.settings.add(rep, lest)

        burpees = Movement.objects.create(name="burpees", founder=founder, equipment=anyone)
        burpees.settings.add(rep, lest)

        situp = Movement.objects.create(name="situps", founder=founder, equipment=anyone)
        burpees.settings.add(rep, lest)

        boxjumps = Movement.objects.create(name="box jumps", founder=founder, equipment=box)
        burpees.settings.add(rep, lest)

        run = Movement.objects.create(name="run", founder=founder, equipment=anyone)
        burpees.settings.add(dist, lest)

        # We create some Workouts

        # BENCHMARK GIRLS
        # 1. Chelsea
        chelsea = Exercise.objects.create(name="chelsea",
                                    exercise_type=Exercise.EMOM,
                                    description="""C'est un WOD Benchmark Girls. Il faut réaliser
                                                    un tour complet chaque minute pendant 30 minutes.
                                                    Si l'athlète n'arrive pas à réaliser un tour complet
                                                    pendant la minute, il est disqualifié.""",
                                    goal_type=Exercise.TIME,
                                    goal_value=30,
                                    is_default=True,
                                    founder=founder)
        chelsea_pullup = MovementsPerExercise.objects.create(exercise=chelsea,
                                                            movement=pullup,
                                                            movement_number=1)
        chelsea_pullup_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=chelsea_pullup,
                                                                                   setting=rep,
                                                                                   setting_value=5)
        chelsea_pullup_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=chelsea_pullup,
                                                                                   setting=lest,
                                                                                   setting_value=0)
        chelsea_pushup = MovementsPerExercise.objects.create(exercise=chelsea,
                                                            movement=pushup,
                                                            movement_number=2)
        chelsea_pushup_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=chelsea_pushup,
                                                                                   setting=rep,
                                                                                   setting_value=10)
        chelsea_pushup_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=chelsea_pushup,
                                                                                   setting=lest,
                                                                                   setting_value=0)
        chelsea_squat = MovementsPerExercise.objects.create(exercise=chelsea,
                                                            movement=squat,
                                                            movement_number=3)
        chelsea_squat_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=chelsea_squat,
                                                                                   setting=rep,
                                                                                   setting_value=15)
        chelsea_squat_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=chelsea_squat,
                                                                                   setting=lest,
                                                                                   setting_value=0)

        # 2. Angie

        angie = Exercise.objects.create(name="angie",
                                    exercise_type=Exercise.FORTIME,
                                    description="""C'est un WOD Benchmark Girls. Il challenge fortement votre endurance musculaire sur l'ensemble de votre corps. L'objectif est de réaliser l'ensemble des mouvements en un minimum de temps.""",
                                    goal_type=Exercise.ROUND,
                                    goal_value=1,
                                    is_default=True,
                                    founder=founder)
        angie_pullup = MovementsPerExercise.objects.create(exercise=angie,
                                                            movement=pullup,
                                                            movement_number=1)
        angie_pullup_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=angie_pullup,
                                                                                   setting=rep,
                                                                                   setting_value=100)
        angie_pullup_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=angie_pullup,
                                                                                    setting=lest,
                                                                                    setting_value=0)
        angie_pushup = MovementsPerExercise.objects.create(exercise=angie,
                                                            movement=pushup,
                                                            movement_number=2)
        angie_pushup_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=angie_pushup,
                                                                                   setting=rep,
                                                                                   setting_value=100)
        angie_pushup_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=angie_pushup,
                                                                                   setting=lest,
                                                                                   setting_value=0)
        angie_situp = MovementsPerExercise.objects.create(exercise=angie,
                                                            movement=situp,
                                                            movement_number=3)
        angie_situp_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=angie_situp,
                                                                                   setting=rep,
                                                                                   setting_value=100)
        angie_situp_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=angie_situp,
                                                                                   setting=lest,
                                                                                   setting_value=0)
        angie_squat = MovementsPerExercise.objects.create(exercise=angie,
                                                            movement=squat,
                                                            movement_number=4)
        angie_squat_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=angie_squat,
                                                                                   setting=rep,
                                                                                   setting_value=100)
        angie_squat_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=angie_squat,
                                                                                   setting=lest,
                                                                                   setting_value=0)

        # 3. Barbara
        barbara = Exercise.objects.create(name="barbara",
                                    exercise_type=Exercise.FORTIME,
                                    description="""C'est un WOD Benchmark Girls. Il travaille l'ensemble du corps et fait appel à votre endurance musculaire ainsi qu'à votre cardio. L'objectif est de réaliser l'ensemble des mouvements en un minimum de temps.""",
                                    goal_type=Exercise.ROUND,
                                    goal_value=5,
                                    is_default=True,
                                    founder=founder)
        barbara_pullup = MovementsPerExercise.objects.create(exercise=barbara,
                                                            movement=pullup,
                                                            movement_number=1)
        barbara_pullup_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=barbara_pullup,
                                                                                   setting=rep,
                                                                                   setting_value=20)
        barbara_pullup_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=barbara_pullup,
                                                                                    setting=lest,
                                                                                    setting_value=0)
        barbara_pushup = MovementsPerExercise.objects.create(exercise=barbara,
                                                            movement=pushup,
                                                            movement_number=2)
        barbara_pushup_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=barbara_pushup,
                                                                                   setting=rep,
                                                                                   setting_value=30)
        barbara_pushup_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=barbara_pushup,
                                                                                    setting=lest,
                                                                                    setting_value=0)
        barbara_situp = MovementsPerExercise.objects.create(exercise=barbara,
                                                            movement=situp,
                                                            movement_number=3)
        barbara_situp_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=barbara_situp,
                                                                                   setting=rep,
                                                                                   setting_value=40)
        barbara_situp_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=barbara_situp,
                                                                                   setting=lest,
                                                                                   setting_value=0) 
        barbara_squat = MovementsPerExercise.objects.create(exercise=barbara,
                                                            movement=squat,
                                                            movement_number=4)
        barbara_squat_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=barbara_squat,
                                                                                   setting=rep,
                                                                                   setting_value=50)
        barbara_squat_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=barbara_squat,
                                                                                   setting=lest,
                                                                                   setting_value=0)

        # 4. Cindy
        cindy = Exercise.objects.create(name="cindy",
                            exercise_type=Exercise.AMRAP,
                            description="""C'est un WOD Benchmark Girls. Il travaille l'ensemble du corps et sollicite fortement le cardio. L'objectif est de faire le maximum de tours en 20 minutes.""",
                            goal_type=Exercise.TIME,
                            goal_value=20,
                            is_default=True,
                            founder=founder)
        cindy_pullup = MovementsPerExercise.objects.create(exercise=cindy,
                                                            movement=pullup,
                                                            movement_number=1)
        cindy_pullup_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=cindy_pullup,
                                                                                   setting=rep,
                                                                                   setting_value=5)
        cindy_pullup_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=cindy_pullup,
                                                                                    setting=lest,
                                                                                    setting_value=0)
        cindy_pushup = MovementsPerExercise.objects.create(exercise=cindy,
                                                            movement=pushup,
                                                            movement_number=2)
        cindy_pushup_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=cindy_pushup,
                                                                                   setting=rep,
                                                                                   setting_value=10)
        cindy_pushup_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=cindy_pushup,
                                                                                    setting=lest,
                                                                                    setting_value=0)
        cindy_squat = MovementsPerExercise.objects.create(exercise=cindy,
                                                            movement=squat,
                                                            movement_number=3)
        cindy_squat_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=cindy_squat,
                                                                                   setting=rep,
                                                                                   setting_value=15)
        cindy_squat_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=cindy_squat,
                                                                                   setting=lest,
                                                                                   setting_value=0)

        # BENCHMARK HERO
        # 1. Murph
        murph = Exercise.objects.create(name="murph",
                            exercise_type=Exercise.FORTIME,
                            description="""C'est un WOD Benchmark Hero. Certainement l'un des wods benchmarks les plus dur. L'objectif est de réaliser le plus rapidement possible l'ensemble des mouvements le plus rapidement possible avec un gilet lesté de 9 kg.""",
                            goal_type=Exercise.ROUND,
                            goal_value=1,
                            is_default=True,
                            founder=founder)

        murph_run_1 = MovementsPerExercise.objects.create(exercise=murph,
                                                        movement=run,
                                                        movement_number=1)
        murph_run_1_dist = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=murph_run_1,
                                                                                   setting=dist,
                                                                                   setting_value=1600)
        murph_run_1_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=murph_run_1,
                                                                                   setting=lest,
                                                                                   setting_value=9)
        murph_pullup = MovementsPerExercise.objects.create(exercise=murph,
                                                            movement=pullup,
                                                            movement_number=2)
        murph_pullup_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=murph_pullup,
                                                                                   setting=rep,
                                                                                   setting_value=100)
        murph_pullup_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=murph_pullup,
                                                                                    setting=lest,
                                                                                    setting_value=9)
        murph_pushup = MovementsPerExercise.objects.create(exercise=murph,
                                                            movement=pushup,
                                                            movement_number=3)
        murph_pushup_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=murph_pushup,
                                                                                   setting=rep,
                                                                                   setting_value=200)
        murph_pushup_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=murph_pushup,
                                                                                    setting=lest,
                                                                                    setting_value=9)
        murph_squat = MovementsPerExercise.objects.create(exercise=murph,
                                                            movement=squat,
                                                            movement_number=4)
        murph_squat_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=murph_squat,
                                                                                   setting=rep,
                                                                                   setting_value=300)
        murph_squat_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=murph_squat,
                                                                                    setting=lest,
                                                                                    setting_value=9)
        murph_run_2 = MovementsPerExercise.objects.create(exercise=murph,
                                                        movement=run,
                                                        movement_number=5)
        murph_run_2_dist = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=murph_run_2,
                                                                                   setting=dist,
                                                                                   setting_value=1600)
        murph_run_2_lest = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=murph_run_2,
                                                                                   setting=lest,
                                                                                   setting_value=9)

class Command(BaseCommand):

    def handle(self, *args, **options):
        db_init = DBinit()
        db_init.clean_db()
        db_init.start()

        self.stdout.write("Base de données initialisée")