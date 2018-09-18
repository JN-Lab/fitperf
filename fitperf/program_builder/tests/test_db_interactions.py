from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Profile, Session, ExercisesPerSession, Program, Training, Exercise, MovementsPerExercise, Movement, MovementSettings
from ..utils.db_interactions import DBInteractions

class TestDBSetInteractions(TestCase):
    """
    This class tests all the set_* methods
    from DBInteractions
    """

    def setUp(self):
        self.db = DBInteractions()

    def test_set_movement_settings_good_value(self):
        """
        This test checks if the method set_movement_setting
        registers well a new movement setting which is linked
        to the predetermined list
        """
        
        setting_value = 'Repetitions'
        movement_setting = self.db.set_movement_setting(setting_value)

        movement_setting_exists = MovementSettings.objects.filter(name=setting_value).exists()
        self.assertTrue(movement_setting_exists)

    def test_set_movement_settings_wrong_value(self):
        """
        This test checks if the method set_movement_setting
        don't registers a new movement's setting which is not linked
        to the predetermined list
        """

        setting_value = 'Wrong value'
        movement_setting = self.db.set_movement_setting(setting_value)

        movement_setting_exists = MovementSettings.objects.filter(name=setting_value).exists()
        self.assertFalse(movement_setting_exists)

    def test_set_movement_settings_not_unique(self):
        """
        This test checks if the method set_movement_settings returns
        the string "already_exists" when we try to register a setting
        which is already in the table
        """

        setting_value = 'Repetitions'
        first_movement_setting = self.db.set_movement_setting(setting_value)

        movement_setting_exists = MovementSettings.objects.filter(name=setting_value).exists()
        self.assertTrue(movement_setting_exists)

        second_movement_setting = self.db.set_movement_setting(setting_value)
        self.assertEqual(second_movement_setting, "already_exists")