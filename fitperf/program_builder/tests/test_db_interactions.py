from django.test import TestCase, TransactionTestCase
from django.contrib.auth.models import User
from ..models import Profile, Session, ExercisesPerSession, Program, Training, Exercise, MovementsPerExercise, Movement, MovementSettings, Equipment
from ..utils.db_interactions import DBInteractions

class TestDBSetInteractions(TestCase):
    """
    This class tests all the set_* methods
    from DBInteractions
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
        self.db = DBInteractions()

    def test_set_movement_settings_good_value(self):
        """
        This test checks if the method set_movement_setting
        registers well a new movement setting which is linked
        to the predetermined list
        """
        
        setting_value = 'Repetitions'
        founder = User.objects.get(username='admin_user')

        movement_setting = self.db.set_movement_setting(setting_value, founder)

        movement_setting_exists = MovementSettings.objects.filter(name=setting_value).exists()
        self.assertTrue(movement_setting_exists)

        movement_registered = MovementSettings.objects.get(name=setting_value)
        self.assertEqual(movement_registered.name, 'Repetitions') 

    def test_set_movement_settings_wrong_value(self):
        """
        This test checks if the method set_movement_setting
        don't registers a new movement's setting which is not linked
        to the predetermined list
        """

        setting_value = 'Wrong value'
        founder = User.objects.get(username='admin_user')

        movement_setting = self.db.set_movement_setting(setting_value, founder)

        movement_setting_exists = MovementSettings.objects.filter(name=setting_value).exists()
        self.assertFalse(movement_setting_exists)

    def test_set_movement_settings_not_unique(self):
        """
        This test checks if the method set_movement_settings returns
        the string "already_exists" when we try to register a setting
        which is already in the table
        """

        setting_value = 'Repetitions'
        founder = User.objects.get(username='admin_user')

        first_movement_setting = self.db.set_movement_setting(setting_value, founder)
        movement_setting_exists = MovementSettings.objects.filter(name=setting_value).exists()
        self.assertTrue(movement_setting_exists)

        second_movement_setting = self.db.set_movement_setting(setting_value, founder)
        self.assertEqual(second_movement_setting, "already_exists")

    def test_set_equipment_success(self):
        """
        This test checks if the method set_equipment registers well
        a new equipment
        """

        equipment_name = 'barre de traction'
        founder = User.objects.get(username='admin_user')

        new_equipment = self.db.set_equipment(equipment_name, founder)

        equipment_exists = Equipment.objects.filter(name=equipment_name).exists()
        self.assertTrue(equipment_exists)

        equipment_registered = Equipment.objects.get(name=equipment_name)
        self.assertEqual(equipment_registered.name, 'barre de traction')

    def test_set_equipment_not_unique(self):
        """
        This test checks if the method set_equipment returns
        the string "already_exists" when we try to register an equipment
        which is already in the table
        """

        equipment_name = 'barre de traction'
        founder = User.objects.get(username='admin_user')

        first_equipment = self.db.set_equipment(equipment_name, founder)
        equipment_exists = Equipment.objects.filter(name=equipment_name).exists()
        self.assertTrue(equipment_exists)

        second_equipment = self.db.set_equipment(equipment_name, founder)
        self.assertEqual(second_equipment, "already_exists")

    def test_set_movement_success(self):
        """
        This test checks if the method set_movement registers well
        a new movement
        """

        # avoir un nom, un createur, un équipement, un ou plusieurs settings
        # We add in the database, the different elements which are necessary
        # This method is dependant from previous ones
        movement_name = 'squat'
        founder = User.objects.get(username='admin_user')
        equipment = self.db.set_equipment("kettlebell", founder)
        first_setting = self.db.set_movement_setting("Repetitions", founder)
        second_setting = self.db.set_movement_setting("Poids", founder)


        new_movement = self.db.set_movement(movement_name, founder, equipment, first_setting, second_setting)
        print(new_movement.settings.all())

        movement_exists = Movement.objects.filter(name=movement_name).exists()
        self.assertTrue(movement_exists)

        movement_registered = Movement.objects.get(name=movement_name)
        self.assertEqual(movement_registered.name, 'squat')
        self.assertEqual(len(movement_registered.settings.all()), 2)

    # def test_set_movement_not_unique(self):
    #     """
    #     This test check if the method set_movement returns the string
    #     "already_exists" when we try to register a movement which is
    #     already in the table
    #     """

    #     movement_name = 'squat'
    #     founder = User.objects.get(username='admin_user')

    #     first_movement = self.db.set_movement(movement_name, founder)
    #     movement_exists = Movement.objects.filter(name=movement_name).exists()
    #     self.assertTrue(movement_exists)

    #     second_movement = self.db.set_movement(movement_name, founder)
    #     self.assertEqual(second_movement, "already_exists")