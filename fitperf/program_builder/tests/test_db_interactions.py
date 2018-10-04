#! /usr/bin/env python3
# coding: utf-8
from django.test import TestCase, TransactionTestCase
from django.contrib.auth.models import User
from .helper_dbtestdata import TestDatabase
from ..models import Session, ExercisesPerSession, Program, Training, Exercise, MovementsPerExercise, Movement, MovementSettings, Equipment, MovementSettingsPerMovementsPerExercise
from ..utils.db_interactions import DBInteractions, DBMovement, DBExercise

from django.db.models import Q

class TestDBMovement(TestCase):
    """
    This class tests all the set_* methods
    from DBInteractions
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create a database for test with TestDatabase helper
        """
        TestDatabase.create()

    def setUp(self):
        self.db_mvt = DBMovement()
        self.db_exo = DBExercise()

    def test_set_settings_movement_one_setting_success(self):
        """
        This test check the method register well one setting
        """

        movement = Movement.objects.get(name="squat")
        cal = MovementSettings.objects.get(name="Calories")

        # Two are already associated in the database test
        self.assertEqual(movement.settings.all().count(), 2)
        movement_settings = self.db_mvt.set_settings_to_movement(movement, cal)
        self.assertEqual(movement.settings.all().count(), 3)

    def test_set_settings_movement_several_settings_success(self):
        """
        This test check the method register well several settings
        """

        movement = Movement.objects.get(name="squat")
        cal = MovementSettings.objects.get(name="Calories")
        dist = MovementSettings.objects.get(name="Distance")

        # Two are already associated in the database test
        self.assertEqual(movement.settings.all().count(), 2)
        movement_settings = self.db_mvt.set_settings_to_movement(movement, cal, dist)
        self.assertEqual(movement.settings.all().count(), 4)

    def test_set_settings_movement_setting_already_exists(self):
        """
        This test check the method register well several settings even if several of them
        are already associated
        """

        movement = Movement.objects.get(name="squat")
        cal = MovementSettings.objects.get(name="Calories")
        dist = MovementSettings.objects.get(name="Distance")
        rep = MovementSettings.objects.get(name="Repetitions")
        weight = MovementSettings.objects.get(name="Poids")

        # Two are already associated in the database test
        self.assertEqual(movement.settings.all().count(), 2)
        movement_settings = self.db_mvt.set_settings_to_movement(movement, cal, dist, rep, weight)
        self.assertEqual(movement.settings.all().count(), 4)


class TestDBExercise(TestCase):
    """
    This class tests all the set_* methods
    from DBInteractions
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create a database for test with TestDatabase helper
        """
        TestDatabase.create()

    def setUp(self):
        self.db_exo = DBExercise()

    def test_define_performance_type(self):
        """
        This test only checks if the method _define_performance_type associates correctly
        the exercise_type with the adequate performance_type
        """

        performance_type = self.db_exo._define_performance_type('MAXIMUM DE REPETITIONS')
        self.assertEqual(performance_type, 'repetitions')

        performance_type = self.db_exo._define_performance_type('AMRAP')
        self.assertEqual(performance_type, 'duree')

        performance_type = self.db_exo._define_performance_type('EMOM')
        self.assertEqual(performance_type, 'duree')

        performance_type = self.db_exo._define_performance_type('RUNNING')
        self.assertEqual(performance_type, 'distance')

        performance_type = self.db_exo._define_performance_type('FORTIME')
        self.assertEqual(performance_type, 'tours')

        performance_type = self.db_exo._define_performance_type('ECHAUFFEMENT')
        self.assertEqual(performance_type, 'tours')

        performance_type = self.db_exo._define_performance_type('FORCE')
        self.assertEqual(performance_type, 'tours')

        performance_type = self.db_exo._define_performance_type('CONDITIONNEMENT')
        self.assertEqual(performance_type, 'tours')

    def test_set_exercise_success(self):
        """
        This test checks if the method set_exercise registers well
        a new exercise
        """

        exercise_name = 'Angie'
        exercise_type = "RUNNING"
        description = "test exo"
        performance_type = "Distance"
        performance_value = "8000"
        founder = User.objects.get(username='admin_user')

        exercise = self.db_exo.set_exercise(exercise_name, exercise_type, description, performance_type, performance_value, founder)

        exercise_exists = Exercise.objects.filter(name=exercise_name).exists()
        self.assertTrue(exercise_exists)

        exercise_registered = Exercise.objects.get(name=exercise_name)
        self.assertEqual(exercise_registered.name, 'Angie')
        self.assertEqual(exercise_registered.exercise_type, 'RUNNING')
        self.assertEqual(exercise_registered.performance_type, 'distance')

    def test_set_movement_to_exercise_success(self):
        """
        This test checks if the method set_exercise registers well a new
        movement to an exercise
        """
        
        #We get the user
        founder = User.objects.get(username='admin_user')

        # We get an exercise
        connie = Exercise.objects.get(name="connie")

        # We get one movement
        pushup = Movement.objects.get(name="pushup")

        # Connie workout has two movements associated before new association
        self.assertEqual(connie.movements.all().count(), 2)
        # We associate the movement as a third movements for connie workout
        connie_pushup = self.db_exo.set_movement_to_exercise(connie, pushup, 3)

        # We test
        self.assertEqual(connie.movements.all().count(), 3)
        self.assertEqual(connie_pushup.movement_number, 3)

    def test_set_settings_value_to_movement_linked_to_exercise_success(self):

        #We get the user
        founder = User.objects.get(username='admin_user')

        # We get an exercise
        connie = Exercise.objects.get(name="connie")

        # We get a setting
        rep = MovementSettings.objects.get(name="Repetitions")

        # We get one movement
        pushup = Movement.objects.get(name="pushup")

        # We associate the movement as a third movements for connie workout
        connie_pushup = self.db_exo.set_movement_to_exercise(connie, pushup, 3)
        
        # We associate a number of repetitions of pushup for connie workout
        rep_value = self.db_exo.set_settings_value_to_movement_linked_to_exercise(connie_pushup, rep, 10)

        # We test
        self.assertEqual(rep_value.setting_value, 10)
        self.assertEqual(rep_value.setting, rep)
        self.assertEqual(rep_value.exercise_movement.exercise, connie)
        self.assertEqual(rep_value.exercise_movement.movement, pushup)