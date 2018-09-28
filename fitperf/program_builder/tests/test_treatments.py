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

        admin_user = User.objects.create_user(username='admin_user',password='admin_password')
        admin_profile = Profile(user=admin_user)
        admin_profile.save()

    def setUp(self):
        self.treatment = DataTreatment()
        self.db_mvt = DBMovement()

    def test_get_all_movements_in_dict(self):
        """
        This test checks if the method get_all_movements_in_dict
        returns an adequate dictionnary 
        """

        # We get the user
        founder = User.objects.get(username='admin_user')
        # We create some equipment
        kb = self.db_mvt.set_equipment("kettlebell", founder)
        anyone = self.db_mvt.set_equipment("aucun", founder)
        # We create some settings
        rep = self.db_mvt.set_movement_setting("Repetitions", founder)
        weight = self.db_mvt.set_movement_setting("Poids", founder)
           
        # We create a first movement
        movement_name = 'squat'
        first_movement = self.db_mvt.set_movement(movement_name, founder, kb)
        movement_settings = self.db_mvt.set_settings_to_movement(first_movement, rep, weight)
        
        # We create a second movement
        movement_name = 'push up'        
        second_movement = self.db_mvt.set_movement(movement_name, founder, anyone)
        movement_settings = self.db_mvt.set_settings_to_movement(first_movement, rep)

        # We apply the method
        mvts_list = self.treatment.get_all_movements_in_dict()
        
        # We test
        result = [
            {   
                "id": first_movement.pk,
                "name": first_movement.name,
                "equipement": first_movement.equipment.name,
                "settings": [setting.name for setting in first_movement.settings.all()]
            },
            {   
                "id": second_movement.pk,
                "name": second_movement.name,
                "equipement": second_movement.equipment.name,
                "settings": [setting.name for setting in second_movement.settings.all()]
            },
        ]

        self.assertEqual(mvts_list, result)