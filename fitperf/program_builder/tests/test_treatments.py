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