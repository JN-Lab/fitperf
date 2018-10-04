#! /usr/bin/env python3
# coding: utf-8
from django.contrib.auth.models import User
from ..models import Session, ExercisesPerSession, Program, Training, Exercise, MovementsPerExercise, Movement, MovementSettings, Equipment, MovementSettingsPerMovementsPerExercise

class TestDatabase:
    
    @staticmethod
    def create():
        # We create a users
        admin_user = User.objects.create_user(username='admin_user', password='admin_password')
        ordinary_user = User.objects.create_user(username='ordinary_user', password='ordinary_user')
        new_user = User.objects.create_user(username='new_user', password='new_user')

        # We create some settings
        rep = MovementSettings.objects.create(name=MovementSettings.REPETITIONS, founder=admin_user)
        weight = MovementSettings.objects.create(name=MovementSettings.WEIGHT, founder=admin_user)
        dist = MovementSettings.objects.create(name=MovementSettings.DISTANCE, founder=admin_user)
        cal = MovementSettings.objects.create(name=MovementSettings.CALORIES, founder=admin_user)

        # We create some equipments
        kb = Equipment.objects.create(name="kettlebell", founder=admin_user)
        anyone = Equipment.objects.create(name="aucun", founder=admin_user)
        ball = Equipment.objects.create(name="balle", founder=admin_user)
        drawbar = Equipment.objects.create(name="barre de traction", founder=admin_user)

        # We create some movements
        squat = Movement.objects.create(name="squat", founder=admin_user, equipment=kb)
        squat.settings.add(rep, weight)
        push_up = Movement.objects.create(name="pushup", founder=admin_user, equipment=anyone)
        push_up.settings.add(rep)
        wallball = Movement.objects.create(name="wallball", founder=admin_user, equipment=ball)
        wallball.settings.add(rep, weight)
        pullup = Movement.objects.create(name="pullup", founder=admin_user, equipment=drawbar)
        wallball.settings.add(rep)

        # We create some workouts

        # 1. Chelsea Workout created by ordinary_user
        o_chelsea = Exercise.objects.create(name="chelsea",
                                         exercise_type=Exercise.EMOM,
                                         description="test chelsea",
                                         performance_type=Exercise.TIME,
                                         performance_value=30,
                                         founder=ordinary_user)
        o_chelsea_pullup = MovementsPerExercise.objects.create(exercise=o_chelsea,
                                                            movement=pullup,
                                                            movement_number=1)
        o_chelsea_pullup_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=o_chelsea_pullup,
                                                                                   setting=rep,
                                                                                   setting_value=10)
        o_chelsea_pushup = MovementsPerExercise.objects.create(exercise=o_chelsea,
                                                            movement=push_up,
                                                            movement_number=2)
        o_chelsea_pushup_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=o_chelsea_pushup,
                                                                                   setting=rep,
                                                                                   setting_value=20)
        o_chelsea_squat = MovementsPerExercise.objects.create(exercise=o_chelsea,
                                                            movement=squat,
                                                            movement_number=3)
        o_chelsea_squat_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=o_chelsea_squat,
                                                                                   setting=rep,
                                                                                   setting_value=30)
        o_chelsea_squat_weight = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=o_chelsea_squat,
                                                                                   setting=weight,
                                                                                   setting_value=10)                                                    

        # 2. Chelsea Workout created by admin_user
        a_chelsea = Exercise.objects.create(name="chelsea",
                                         exercise_type=Exercise.EMOM,
                                         description="test chelsea",
                                         performance_type=Exercise.TIME,
                                         performance_value=30,
                                         founder=admin_user)
        a_chelsea_pullup = MovementsPerExercise.objects.create(exercise=a_chelsea,
                                                            movement=pullup,
                                                            movement_number=1)
        a_chelsea_pullup_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=a_chelsea_pullup,
                                                                                   setting=rep,
                                                                                   setting_value=5)
        a_chelsea_pushup = MovementsPerExercise.objects.create(exercise=a_chelsea,
                                                            movement=push_up,
                                                            movement_number=2)
        a_chelsea_pushup_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=a_chelsea_pushup,
                                                                                   setting=rep,
                                                                                   setting_value=10)
        a_chelsea_squat = MovementsPerExercise.objects.create(exercise=a_chelsea,
                                                            movement=squat,
                                                            movement_number=3)
        a_chelsea_squat_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=a_chelsea_squat,
                                                                                   setting=rep,
                                                                                   setting_value=15)
        a_chelsea_squat_weight = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=a_chelsea_squat,
                                                                                   setting=weight,
                                                                                   setting_value=0)                                                    

        # 3. Connie Workout created by new_user
        connie = Exercise.objects.create(name="connie",
                                    exercise_type=Exercise.FORTIME,
                                    description="test connie",
                                    performance_type=Exercise.ROUND,
                                    performance_value=5,
                                    founder=new_user)
        connie_pullup = MovementsPerExercise.objects.create(exercise=connie,
                                                            movement=pullup,
                                                            movement_number=1)
        connie_pullup_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=connie_pullup,
                                                                                   setting=rep,
                                                                                   setting_value=25)
        connie_wallball = MovementsPerExercise.objects.create(exercise=connie,
                                                            movement=wallball,
                                                            movement_number=2)
        connie_wallball_rep = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=connie_wallball,
                                                                                   setting=rep,
                                                                                   setting_value=50)
        connie_wallball_weight = MovementSettingsPerMovementsPerExercise.objects.create(exercise_movement=connie_wallball,
                                                                                   setting=weight,
                                                                                   setting_value=20) 