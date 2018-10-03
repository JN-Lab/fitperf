#! /usr/bin/env python3
# coding: utf-8
from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Profile, Session, ExercisesPerSession, Program, Training, Exercise, MovementsPerExercise, MovementSettingsPerMovementsPerExercise, Movement, MovementSettings, Equipment
from ..utils.treatments import DataTreatment
from ..utils.db_interactions import DBMovement


class TestDataTreatment(TestCase):
    """
    This class tests all the methods from DataTreatment class
    """

    @classmethod
    def setUpTestData(cls):
        """
        We need to create a user
        """

        # We create a user
        admin_user = User.objects.create_user(username='admin_user',password='admin_password')

        # We create some settings
        rep = MovementSettings.objects.create(name="Repetitions", founder=admin_user)
        weight = MovementSettings.objects.create(name="Poids", founder=admin_user)
        dist = MovementSettings.objects.create(name="Distance", founder=admin_user)
        cal = MovementSettings.objects.create(name="Calories", founder=admin_user)

        # We create some equipments
        kb = Equipment.objects.create(name="kettlebell", founder=admin_user)
        anyone = Equipment.objects.create(name="aucun", founder=admin_user)
        ball = Equipment.objects.create(name="balle", founder=admin_user)

        # We create some movements
        squat = Movement.objects.create(name="squat", founder=admin_user, equipment=kb)
        squat.settings.add(rep, weight)
        push_up = Movement.objects.create(name="pushup", founder=admin_user, equipment=anyone)
        push_up.settings.add(rep)
        wallball = Movement.objects.create(name="wallball", founder=admin_user, equipment=ball)
        wallball.settings.add(rep, weight)

    def setUp(self):
        
        self.treatment = DataTreatment()
        self.db_mvt = DBMovement()

    def test_get_all_movements_in_dict(self):
        """
        This test checks if the method get_all_movements_in_dict
        returns an adequate dictionnary 
        """

        # We get the movements
        squat = Movement.objects.get(name="squat")
        pushup = Movement.objects.get(name="pushup")
        wallball = Movement.objects.get(name="wallball")

        # We apply the method
        mvts_list = self.treatment.get_all_movements_in_dict()

        # We test
        result = [
            {   
                "id": squat.pk,
                "name": squat.name,
                "equipement": squat.equipment.name,
                "settings": [setting.name for setting in squat.settings.all()]
            },
            {   
                "id": pushup.pk,
                "name": pushup.name,
                "equipement": pushup.equipment.name,
                "settings": [setting.name for setting in pushup.settings.all()]
            },
            {   
                "id": wallball.pk,
                "name": wallball.name,
                "equipement": wallball.equipment.name,
                "settings": [setting.name for setting in wallball.settings.all()]
            },
        ]

        self.assertEqual(mvts_list, result)

    def test_register_exercise_from_dict_success(self):
        """
        This test checks if the method register_exercise_from_dict
        registers well the exercise in the database withh all its
        associations.
        """

        # We get the user
        founder = User.objects.get(username="admin_user")

        # We set up some exercise features
        name = "angie"
        exercise_type = "FORTIME"
        description = "workout de test"
        perf_type = "Nombre de tours"
        perf_value = 5
        
        # We get the movements
        squat = Movement.objects.get(name="squat")
        pushup = Movement.objects.get(name="pushup")
        wallball = Movement.objects.get(name="wallball")

        # We get the settings implicated in the test
        rep = MovementSettings.objects.get(name="Repetitions")
        weight = MovementSettings.objects.get(name="Poids")

        # We create the dict
        exercise_dict = {
            "name": name,
            "exerciseType": exercise_type,
            "description": description,
            "performanceType": perf_type,
            "performanceValue": perf_value,
            "movements" : [
                {
                    "name": squat.name,
                    "order": 1,
                    "settings": [
                        {
                            "name": "Repetitions",
                            "value": 10,
                        },
                        {
                            "name": "Poids",
                            "value": 5,
                        }

                    ]
                },
                {
                    "name": pushup.name,
                    "order": 2,
                    "settings": [
                        {
                            "name": "Repetitions",
                            "value": 15,
                        },
                    ]
                },
                {
                    "name": wallball.name,
                    "order": 3,
                    "settings": [
                        {
                            "name": "Repetitions",
                            "value": 20,
                        },
                        {
                            "name": "Poids",
                            "value": 18,
                        },
                    ]
                },
            ]
        }

        # We apply the method
        exercise = self.treatment.register_exercise_from_dict(exercise_dict, founder)

        # We test
        self.assertEqual(exercise.name, "angie")
        self.assertEqual(exercise.movements.all().count(), 3)

        angie_squat = MovementsPerExercise.objects.get(exercise=exercise, movement=squat)
        self.assertEqual(angie_squat.movement_number, 1)
        self.assertEqual(angie_squat.movement_settings.all().count(), 2)

        angie_squat_settings = MovementSettingsPerMovementsPerExercise.objects.filter(exercise_movement=angie_squat)
        self.assertEqual(angie_squat_settings.count(), 2)
        angie_squat_rep = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=angie_squat, setting=rep)
        self.assertEqual(angie_squat_rep.setting_value, 10)
        angie_squat_weight = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=angie_squat, setting=weight)
        self.assertEqual(angie_squat_weight.setting_value, 5)
        
        angie_pushup = MovementsPerExercise.objects.get(exercise=exercise, movement=pushup)
        self.assertEqual(angie_pushup.movement_number, 2)
        self.assertEqual(angie_pushup.movement_settings.all().count(), 1)
        angie_pushup_settings = MovementSettingsPerMovementsPerExercise.objects.filter(exercise_movement=angie_pushup)
        self.assertEqual(angie_pushup_settings.count(), 1)
        angie_pushup_rep = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=angie_pushup, setting=rep)
        self.assertEqual(angie_pushup_rep.setting_value, 15)

        angie_wallball = MovementsPerExercise.objects.get(exercise=exercise, movement=wallball)
        self.assertEqual(angie_wallball.movement_number, 3)
        self.assertEqual(angie_wallball.movement_settings.all().count(), 2)

        angie_wallball_settings = MovementSettingsPerMovementsPerExercise.objects.filter(exercise_movement=angie_wallball)
        self.assertEqual(angie_wallball_settings.count(), 2)
        angie_wallball_rep = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=angie_wallball, setting=rep)
        self.assertEqual(angie_wallball_rep.setting_value, 20)
        angie_wallball_weight = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=angie_wallball, setting=weight)
        self.assertEqual(angie_wallball_weight.setting_value, 18)


    def test_register_exercise_from_dict_fail_already_exist(self):
        pass

    def test_register_exercise_from_dict_fail_data_type_problem(self):
        pass