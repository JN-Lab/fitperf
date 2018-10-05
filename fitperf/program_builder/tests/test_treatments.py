#! /usr/bin/env python3
# coding: utf-8
from django.test import TestCase
from django.contrib.auth.models import User
from .helper_dbtestdata import TestDatabase
from ..models import Session, ExercisesPerSession, Program, Training, Exercise, MovementsPerExercise, MovementSettingsPerMovementsPerExercise, Movement, MovementSettings, Equipment
from ..utils.treatments import DataTreatment
from ..utils.db_interactions import DBMovement


class TestDataTreatment(TestCase):
    """
    This class tests all the methods from DataTreatment class
    """
    maxDiff = None
    @classmethod
    def setUpTestData(cls):
        """
        Create a database for test with TestDatabase helper
        """
        TestDatabase.create()

    def setUp(self):
        
        self.treatment = DataTreatment()

    def test_get_all_movements_in_dict(self):
        """
        This test checks if the method get_all_movements_in_dict
        returns an adequate dictionnary 
        """

        # We get the movements
        squat = Movement.objects.get(name="squat")
        pushup = Movement.objects.get(name="pushup")
        wallball = Movement.objects.get(name="wallball")
        pullup = Movement.objects.get(name="pullup")

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
            {   
                "id": pullup.pk,
                "name": pullup.name,
                "equipement": pullup.equipment.name,
                "settings": [setting.name for setting in pullup.settings.all()]
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
        rep = MovementSettings.objects.get(name=MovementSettings.REPETITIONS)
        weight = MovementSettings.objects.get(name=MovementSettings.WEIGHT)

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
                            "name": "repetitions",
                            "value": 10,
                        },
                        {
                            "name": "poids",
                            "value": 5,
                        }

                    ]
                },
                {
                    "name": pushup.name,
                    "order": 2,
                    "settings": [
                        {
                            "name": "repetitions",
                            "value": 15,
                        },
                    ]
                },
                {
                    "name": wallball.name,
                    "order": 3,
                    "settings": [
                        {
                            "name": "repetitions",
                            "value": 20,
                        },
                        {
                            "name": "poids",
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
        self.assertEqual(exercise.exercise_type, "FORTIME")
        self.assertEqual(exercise.performance_value, 5)
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

    def test_register_exercise_from_dict_success_running_exercise(self):
        
        # We get the user
        founder = User.objects.get(username="admin_user")

        # We set up some exercise features
        name = "run 7.5"
        exercise_type = "RUNNING"
        description = "running test"
        perf_type = "Distance"
        perf_value = 7.5


        # We create the dict
        exercise_dict = {
            "name": name,
            "exerciseType": exercise_type,
            "description": description,
            "performanceType": perf_type,
            "performanceValue": perf_value,
            "movements" : []
        }

        # We apply the method
        exercise = self.treatment.register_exercise_from_dict(exercise_dict, founder)

        # We Test
        self.assertEqual(exercise.name, "run 7.5")
        self.assertEqual(exercise.exercise_type, "RUNNING")
        self.assertEqual(exercise.performance_value, 7500)
        self.assertEqual(exercise.movements.all().count(), 0)

    def test_get_all_exercises_in_dict(self):
        
        # We get the user
        admin_founder = User.objects.get(username="admin_user")
        ordinary_founder = User.objects.get(username="ordinary_user")
        new_user = User.objects.get(username="new_user")
        
        # We get the movements
        pullup = Movement.objects.get(name="pullup")
        pushup = Movement.objects.get(name="pushup")
        squat = Movement.objects.get(name="squat")
        wallball = Movement.objects.get(name="wallball")

        # We get the settings 
        rep = MovementSettings.objects.get(name=MovementSettings.REPETITIONS)
        weight = MovementSettings.objects.get(name=MovementSettings.WEIGHT)
        dist = MovementSettings.objects.get(name=MovementSettings.DISTANCE)
        cal = MovementSettings.objects.get(name=MovementSettings.CALORIES)

        # We get the workouts
        
        # 1. o_chelsea

        o_chelsea = Exercise.objects.get(name="chelsea", founder=ordinary_founder)
        o_chelsea_pullup = MovementsPerExercise.objects.get(exercise=o_chelsea, movement=pullup)
        o_chelsea_pullup_rep = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=o_chelsea_pullup, setting=rep)
        o_chelsea_pushup = MovementsPerExercise.objects.get(exercise=o_chelsea, movement=pushup)
        o_chelsea_pushup_rep = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=o_chelsea_pushup, setting=rep)
        o_chelsea_squat = MovementsPerExercise.objects.get(exercise=o_chelsea, movement=squat)
        o_chelsea_squat_rep = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=o_chelsea_squat, setting=rep)
        o_chelsea_squat_weight = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=o_chelsea_squat, setting=weight)

        # 2. a_chelsea
        a_chelsea = Exercise.objects.get(name="chelsea", founder=admin_founder)
        a_chelsea_pullup = MovementsPerExercise.objects.get(exercise=a_chelsea, movement=pullup)
        a_chelsea_pullup_rep = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=a_chelsea_pullup, setting=rep)
        a_chelsea_pushup = MovementsPerExercise.objects.get(exercise=a_chelsea, movement=pushup)
        a_chelsea_pushup_rep = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=a_chelsea_pushup, setting=rep)
        a_chelsea_squat = MovementsPerExercise.objects.get(exercise=a_chelsea, movement=squat)
        a_chelsea_squat_rep = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=a_chelsea_squat, setting=rep)
        a_chelsea_squat_weight = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=a_chelsea_squat, setting=weight)

        # 3. connie
        connie = Exercise.objects.get(name="connie", founder=new_user)
        connie_pullup = MovementsPerExercise.objects.get(exercise=connie, movement=pullup)
        connie_pullup_rep = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=connie_pullup, setting=rep)
        connie_wallball = MovementsPerExercise.objects.get(exercise=connie, movement=wallball)
        connie_wallball_rep = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=connie_wallball, setting=rep)
        connie_wallball_weight = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=connie_wallball, setting=weight)

        # Result expected
        result = [
            {
                "id": o_chelsea.pk,
                "name": o_chelsea.name,
                "exerciseType": o_chelsea.exercise_type,
                "description": o_chelsea.description,
                "performanceType": o_chelsea.performance_type,
                "performanceValue": o_chelsea.performance_value,
                "is_default": o_chelsea.is_default,
                "movements": [
                    {
                        "id": o_chelsea_pullup.movement.pk,
                        "name": o_chelsea_pullup.movement.name,
                        "order": o_chelsea_pullup.movement_number,
                        "settings": [
                            {
                                "name": o_chelsea_pullup_rep.setting.name,
                                "value": o_chelsea_pullup_rep.setting_value,
                            },
                        ]
                    },
                    {
                        "id": o_chelsea_pushup.movement.pk,
                        "name": o_chelsea_pushup.movement.name,
                        "order": o_chelsea_pushup.movement_number,
                        "settings": [
                            {
                                "name": o_chelsea_pushup_rep.setting.name,
                                "value": o_chelsea_pushup_rep.setting_value,
                            },
                        ]
                    },
                    {
                        "id": o_chelsea_squat.movement.pk,
                        "name": o_chelsea_squat.movement.name,
                        "order": o_chelsea_squat.movement_number,
                        "settings": [
                            {
                                "name": o_chelsea_squat_rep.setting.name,
                                "value": o_chelsea_squat_rep.setting_value,
                            },
                            {
                                "name": o_chelsea_squat_weight.setting.name,
                                "value": o_chelsea_squat_weight.setting_value,
                            },
                        ]
                    },
                ],
            },
            {
                "id": a_chelsea.pk,
                "name": a_chelsea.name,
                "exerciseType": a_chelsea.exercise_type,
                "description": a_chelsea.description,
                "performanceType": a_chelsea.performance_type,
                "performanceValue": a_chelsea.performance_value,
                "is_default": a_chelsea.is_default,
                "movements": [
                    {
                        "id": a_chelsea_pullup.movement.pk,
                        "name": a_chelsea_pullup.movement.name,
                        "order": a_chelsea_pullup.movement_number,
                        "settings": [
                            {
                                "name": a_chelsea_pullup_rep.setting.name,
                                "value": a_chelsea_pullup_rep.setting_value,
                            },
                        ]
                    },
                    {
                        "id": a_chelsea_pushup.movement.pk,
                        "name": a_chelsea_pushup.movement.name,
                        "order": a_chelsea_pushup.movement_number,
                        "settings": [
                            {
                                "name": a_chelsea_pushup_rep.setting.name,
                                "value": a_chelsea_pushup_rep.setting_value,
                            },
                        ]
                    },
                    {
                        "id": a_chelsea_squat.movement.pk,
                        "name": a_chelsea_squat.movement.name,
                        "order": a_chelsea_squat.movement_number,
                        "settings": [
                            {
                                "name": a_chelsea_squat_rep.setting.name,
                                "value": a_chelsea_squat_rep.setting_value,
                            },
                            {
                                "name": a_chelsea_squat_weight.setting.name,
                                "value": a_chelsea_squat_weight.setting_value,
                            },
                        ]
                    },
                ],
            },
            {
                "id": connie.pk,
                "name": connie.name,
                "exerciseType": connie.exercise_type,
                "description": connie.description,
                "performanceType": connie.performance_type,
                "performanceValue": connie.performance_value,
                "is_default": connie.is_default,
                "movements": [
                    {
                        "id": connie_pullup.movement.pk,
                        "name": connie_pullup.movement.name,
                        "order": connie_pullup.movement_number,
                        "settings": [
                            {
                                "name": connie_pullup_rep.setting.name,
                                "value": connie_pullup_rep.setting_value,
                            },
                        ]
                    },
                    {
                        "id": connie_wallball.movement.pk,
                        "name": connie_wallball.movement.name,
                        "order": connie_wallball.movement_number,
                        "settings": [
                            {
                                "name": connie_wallball_rep.setting.name,
                                "value": connie_wallball_rep.setting_value,
                            },
                            {
                                "name": connie_wallball_weight.setting.name,
                                "value": connie_wallball_weight.setting_value,
                            },
                        ]
                    },
                ],
            },
        ]

        # We apply the method
        all_exercises = self.treatment.get_all_exercises_in_dict()

        # We test
        self.assertEqual(all_exercises, result)

    def test_all_exercises_in_dict_for_user(self):
        
        # We get the user
        admin_founder = User.objects.get(username="admin_user")
        ordinary_founder = User.objects.get(username="ordinary_user")
        new_user = User.objects.get(username="new_user")
        
        # We get the movements
        pullup = Movement.objects.get(name="pullup")
        pushup = Movement.objects.get(name="pushup")
        squat = Movement.objects.get(name="squat")
        wallball = Movement.objects.get(name="wallball")

        # We get the settings 
        rep = MovementSettings.objects.get(name=MovementSettings.REPETITIONS)
        weight = MovementSettings.objects.get(name=MovementSettings.WEIGHT)
        dist = MovementSettings.objects.get(name=MovementSettings.DISTANCE)
        cal = MovementSettings.objects.get(name=MovementSettings.CALORIES)

        # We get the workouts
        
        # 1. o_chelsea

        o_chelsea = Exercise.objects.get(name="chelsea", founder=ordinary_founder)
        o_chelsea_pullup = MovementsPerExercise.objects.get(exercise=o_chelsea, movement=pullup)
        o_chelsea_pullup_rep = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=o_chelsea_pullup, setting=rep)
        o_chelsea_pushup = MovementsPerExercise.objects.get(exercise=o_chelsea, movement=pushup)
        o_chelsea_pushup_rep = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=o_chelsea_pushup, setting=rep)
        o_chelsea_squat = MovementsPerExercise.objects.get(exercise=o_chelsea, movement=squat)
        o_chelsea_squat_rep = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=o_chelsea_squat, setting=rep)
        o_chelsea_squat_weight = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=o_chelsea_squat, setting=weight)

        # 2. a_chelsea
        a_chelsea = Exercise.objects.get(name="chelsea", founder=admin_founder)
        a_chelsea_pullup = MovementsPerExercise.objects.get(exercise=a_chelsea, movement=pullup)
        a_chelsea_pullup_rep = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=a_chelsea_pullup, setting=rep)
        a_chelsea_pushup = MovementsPerExercise.objects.get(exercise=a_chelsea, movement=pushup)
        a_chelsea_pushup_rep = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=a_chelsea_pushup, setting=rep)
        a_chelsea_squat = MovementsPerExercise.objects.get(exercise=a_chelsea, movement=squat)
        a_chelsea_squat_rep = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=a_chelsea_squat, setting=rep)
        a_chelsea_squat_weight = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=a_chelsea_squat, setting=weight)

        # 3. connie
        connie = Exercise.objects.get(name="connie", founder=new_user)
        connie_pullup = MovementsPerExercise.objects.get(exercise=connie, movement=pullup)
        connie_pullup_rep = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=connie_pullup, setting=rep)
        connie_wallball = MovementsPerExercise.objects.get(exercise=connie, movement=wallball)
        connie_wallball_rep = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=connie_wallball, setting=rep)
        connie_wallball_weight = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=connie_wallball, setting=weight)

        # Result expected
        ordinary_user_result = [
            {
                "id": o_chelsea.pk,
                "name": o_chelsea.name,
                "exerciseType": o_chelsea.exercise_type,
                "description": o_chelsea.description,
                "performanceType": o_chelsea.performance_type,
                "performanceValue": o_chelsea.performance_value,
                "is_default": o_chelsea.is_default,
                "movements": [
                    {
                        "id": o_chelsea_pullup.movement.pk,
                        "name": o_chelsea_pullup.movement.name,
                        "order": o_chelsea_pullup.movement_number,
                        "settings": [
                            {
                                "name": o_chelsea_pullup_rep.setting.name,
                                "value": o_chelsea_pullup_rep.setting_value,
                            },
                        ]
                    },
                    {
                        "id": o_chelsea_pushup.movement.pk,
                        "name": o_chelsea_pushup.movement.name,
                        "order": o_chelsea_pushup.movement_number,
                        "settings": [
                            {
                                "name": o_chelsea_pushup_rep.setting.name,
                                "value": o_chelsea_pushup_rep.setting_value,
                            },
                        ]
                    },
                    {
                        "id": o_chelsea_squat.movement.pk,
                        "name": o_chelsea_squat.movement.name,
                        "order": o_chelsea_squat.movement_number,
                        "settings": [
                            {
                                "name": o_chelsea_squat_rep.setting.name,
                                "value": o_chelsea_squat_rep.setting_value,
                            },
                            {
                                "name": o_chelsea_squat_weight.setting.name,
                                "value": o_chelsea_squat_weight.setting_value,
                            },
                        ]
                    },
                ],
            },
            {
                "id": a_chelsea.pk,
                "name": a_chelsea.name,
                "exerciseType": a_chelsea.exercise_type,
                "description": a_chelsea.description,
                "performanceType": a_chelsea.performance_type,
                "performanceValue": a_chelsea.performance_value,
                "is_default": a_chelsea.is_default,
                "movements": [
                    {
                        "id": a_chelsea_pullup.movement.pk,
                        "name": a_chelsea_pullup.movement.name,
                        "order": a_chelsea_pullup.movement_number,
                        "settings": [
                            {
                                "name": a_chelsea_pullup_rep.setting.name,
                                "value": a_chelsea_pullup_rep.setting_value,
                            },
                        ]
                    },
                    {
                        "id": a_chelsea_pushup.movement.pk,
                        "name": a_chelsea_pushup.movement.name,
                        "order": a_chelsea_pushup.movement_number,
                        "settings": [
                            {
                                "name": a_chelsea_pushup_rep.setting.name,
                                "value": a_chelsea_pushup_rep.setting_value,
                            },
                        ]
                    },
                    {
                        "id": a_chelsea_squat.movement.pk,
                        "name": a_chelsea_squat.movement.name,
                        "order": a_chelsea_squat.movement_number,
                        "settings": [
                            {
                                "name": a_chelsea_squat_rep.setting.name,
                                "value": a_chelsea_squat_rep.setting_value,
                            },
                            {
                                "name": a_chelsea_squat_weight.setting.name,
                                "value": a_chelsea_squat_weight.setting_value,
                            },
                        ]
                    },
                ],
            },
        ]

        # Result expected
        new_user_result = [
            {
                "id": a_chelsea.pk,
                "name": a_chelsea.name,
                "exerciseType": a_chelsea.exercise_type,
                "description": a_chelsea.description,
                "performanceType": a_chelsea.performance_type,
                "performanceValue": a_chelsea.performance_value,
                "is_default": a_chelsea.is_default,
                "movements": [
                    {
                        "id": a_chelsea_pullup.movement.pk,
                        "name": a_chelsea_pullup.movement.name,
                        "order": a_chelsea_pullup.movement_number,
                        "settings": [
                            {
                                "name": a_chelsea_pullup_rep.setting.name,
                                "value": a_chelsea_pullup_rep.setting_value,
                            },
                        ]
                    },
                    {
                        "id": a_chelsea_pushup.movement.pk,
                        "name": a_chelsea_pushup.movement.name,
                        "order": a_chelsea_pushup.movement_number,
                        "settings": [
                            {
                                "name": a_chelsea_pushup_rep.setting.name,
                                "value": a_chelsea_pushup_rep.setting_value,
                            },
                        ]
                    },
                    {
                        "id": a_chelsea_squat.movement.pk,
                        "name": a_chelsea_squat.movement.name,
                        "order": a_chelsea_squat.movement_number,
                        "settings": [
                            {
                                "name": a_chelsea_squat_rep.setting.name,
                                "value": a_chelsea_squat_rep.setting_value,
                            },
                            {
                                "name": a_chelsea_squat_weight.setting.name,
                                "value": a_chelsea_squat_weight.setting_value,
                            },
                        ]
                    },
                ],
            },
            {
                "id": connie.pk,
                "name": connie.name,
                "exerciseType": connie.exercise_type,
                "description": connie.description,
                "performanceType": connie.performance_type,
                "performanceValue": connie.performance_value,
                "is_default": connie.is_default,
                "movements": [
                    {
                        "id": connie_pullup.movement.pk,
                        "name": connie_pullup.movement.name,
                        "order": connie_pullup.movement_number,
                        "settings": [
                            {
                                "name": connie_pullup_rep.setting.name,
                                "value": connie_pullup_rep.setting_value,
                            },
                        ]
                    },
                    {
                        "id": connie_wallball.movement.pk,
                        "name": connie_wallball.movement.name,
                        "order": connie_wallball.movement_number,
                        "settings": [
                            {
                                "name": connie_wallball_rep.setting.name,
                                "value": connie_wallball_rep.setting_value,
                            },
                            {
                                "name": connie_wallball_weight.setting.name,
                                "value": connie_wallball_weight.setting_value,
                            },
                        ]
                    },
                ],
            },
        ]

        # We apply the method
        ordinary_user_exercise = self.treatment.get_all_exercises_in_dict_for_user(ordinary_founder)
        self.assertEqual(ordinary_user_exercise, ordinary_user_result)

        new_user_exercise = self.treatment.get_all_exercises_in_dict_for_user(new_user)
        self.assertEqual(new_user_exercise, new_user_result)

    def test_get_one_exercise_in_dict(self):
        # We get the user
        ordinary_founder = User.objects.get(username="ordinary_user")
        
        # We get the movements
        pullup = Movement.objects.get(name="pullup")
        pushup = Movement.objects.get(name="pushup")
        squat = Movement.objects.get(name="squat")

        # We get the settings 
        rep = MovementSettings.objects.get(name=MovementSettings.REPETITIONS)
        weight = MovementSettings.objects.get(name=MovementSettings.WEIGHT)

        # We get one movement

        o_chelsea = Exercise.objects.get(name="chelsea", founder=ordinary_founder)
        o_chelsea_pullup = MovementsPerExercise.objects.get(exercise=o_chelsea, movement=pullup)
        o_chelsea_pullup_rep = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=o_chelsea_pullup, setting=rep)
        o_chelsea_pushup = MovementsPerExercise.objects.get(exercise=o_chelsea, movement=pushup)
        o_chelsea_pushup_rep = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=o_chelsea_pushup, setting=rep)
        o_chelsea_squat = MovementsPerExercise.objects.get(exercise=o_chelsea, movement=squat)
        o_chelsea_squat_rep = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=o_chelsea_squat, setting=rep)
        o_chelsea_squat_weight = MovementSettingsPerMovementsPerExercise.objects.get(exercise_movement=o_chelsea_squat, setting=weight)

        # Result
        result = {
            "id": o_chelsea.pk,
            "name": o_chelsea.name,
            "exerciseType": o_chelsea.exercise_type,
            "description": o_chelsea.description,
            "performanceType": o_chelsea.performance_type,
            "performanceValue": o_chelsea.performance_value,
            "is_default": o_chelsea.is_default,
            "movements": [
                {
                    "id": o_chelsea_pullup.movement.pk,
                    "name": o_chelsea_pullup.movement.name,
                    "order": o_chelsea_pullup.movement_number,
                    "settings": [
                        {
                            "name": o_chelsea_pullup_rep.setting.name,
                            "value": o_chelsea_pullup_rep.setting_value,
                        },
                    ]
                },
                {
                    "id": o_chelsea_pushup.movement.pk,
                    "name": o_chelsea_pushup.movement.name,
                    "order": o_chelsea_pushup.movement_number,
                    "settings": [
                        {
                            "name": o_chelsea_pushup_rep.setting.name,
                            "value": o_chelsea_pushup_rep.setting_value,
                        },
                    ]
                },
                {
                    "id": o_chelsea_squat.movement.pk,
                    "name": o_chelsea_squat.movement.name,
                    "order": o_chelsea_squat.movement_number,
                    "settings": [
                        {
                            "name": o_chelsea_squat_rep.setting.name,
                            "value": o_chelsea_squat_rep.setting_value,
                        },
                        {
                            "name": o_chelsea_squat_weight.setting.name,
                            "value": o_chelsea_squat_weight.setting_value,
                        },
                    ]
                },
            ],
        }

        # We test
        o_chelsea_dict = self.treatment.get_one_exercise_in_dict(o_chelsea.pk)
        self.assertEqual(o_chelsea_dict, result)