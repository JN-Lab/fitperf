from django.test import TestCase, TransactionTestCase
from django.contrib.auth.models import User
from ..models import Profile, Session, ExercisesPerSession, Program, Training, Exercise, MovementsPerExercise, Movement, MovementSettings, Equipment, MovementSettingsPerMovementsPerExercise
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
        We need to create a user
        """

        admin_user = User.objects.create_user(username='admin_user',password='admin_password')
        admin_profile = Profile(user=admin_user)
        admin_profile.save()

    def setUp(self):
        self.db_mvt = DBMovement()
        self.db_exo = DBExercise()

    def test_set_movement_settings_success(self):
        """
        This test checks if the method set_movement_setting
        registers well a new movement setting which is linked
        to the predetermined list
        """
        
        setting_value = 'Repetitions'
        founder = User.objects.get(username='admin_user')

        movement_setting = self.db_mvt.set_movement_setting(setting_value, founder)

        movement_setting_exists = MovementSettings.objects.filter(name='repetitions').exists()
        self.assertTrue(movement_setting_exists)

        movement_registered = MovementSettings.objects.get(name=setting_value.lower())
        self.assertEqual(movement_registered.name, 'repetitions') 

    def test_set_movement_settings_not_unique(self):
        """
        This test checks if the method set_movement_settings returns
        the string "already_exists" when we try to register a setting
        which is already in the table
        """

        setting_value = 'Repetitions'
        founder = User.objects.get(username='admin_user')

        first_movement_setting = self.db_mvt.set_movement_setting(setting_value, founder)
        movement_setting_exists = MovementSettings.objects.filter(name='repetitions').exists()
        self.assertTrue(movement_setting_exists)

        second_movement_setting = self.db_mvt.set_movement_setting(setting_value, founder)
        self.assertEqual(second_movement_setting, "already_exists")

    def test_set_equipment_success(self):
        """
        This test checks if the method set_equipment registers well
        a new equipment
        """

        equipment_name = 'Barre de traction'
        founder = User.objects.get(username='admin_user')

        new_equipment = self.db_mvt.set_equipment(equipment_name, founder)

        equipment_exists = Equipment.objects.filter(name='barre de traction').exists()
        self.assertTrue(equipment_exists)

        equipment_registered = Equipment.objects.get(name=equipment_name.lower())
        self.assertEqual(equipment_registered.name, 'barre de traction')

    def test_set_equipment_not_unique(self):
        """
        This test checks if the method set_equipment returns
        the string "already_exists" when we try to register an equipment
        which is already in the table
        """

        equipment_name = 'barre de traction'
        founder = User.objects.get(username='admin_user')

        first_equipment = self.db_mvt.set_equipment(equipment_name, founder)
        equipment_exists = Equipment.objects.filter(name='barre de traction').exists()
        self.assertTrue(equipment_exists)

        second_equipment = self.db_mvt.set_equipment(equipment_name, founder)
        self.assertEqual(second_equipment, "already_exists")

    def test_set_movement_success(self):
        """
        This test checks if the method set_movement registers well
        a new movement
        """

        movement_name = 'SQUAT'
        founder = User.objects.get(username='admin_user')
        equipment = self.db_mvt.set_equipment("kettlebell", founder)

        new_movement = self.db_mvt.set_movement(movement_name, founder, equipment)

        movement_exists = Movement.objects.filter(name='squat').exists()
        self.assertTrue(movement_exists)

        movement_registered = Movement.objects.get(name=movement_name.lower())
        self.assertEqual(movement_registered.name, 'squat')

    def test_set_movement_not_unique(self):
        """
        This test check if the method set_movement returns the string
        "already_exists" when we try to register a movement which is
        already in the table
        """

        movement_name = 'Squat'
        founder = User.objects.get(username='admin_user')
        equipment = self.db_mvt.set_equipment("kettlebell", founder)

        first_movement = self.db_mvt.set_movement(movement_name, founder, equipment)
        movement_exists = Movement.objects.filter(name='squat').exists()
        self.assertTrue(movement_exists)

        second_movement = self.db_mvt.set_movement(movement_name, founder, equipment)
        self.assertEqual(second_movement, None)

    def test_set_settings_movement_one_setting_success(self):
        """
        This test check if:
            - the method set_settings_to_movement associates correctly a
             setting to a chosen movement already created
            - it returns the movement settings
        """
        movement_name = 'squat'
        founder = User.objects.get(username='admin_user')
        equipment = self.db_mvt.set_equipment("kettlebell", founder)
        movement = self.db_mvt.set_movement(movement_name, founder, equipment)

        setting = self.db_mvt.set_movement_setting("Repetitions", founder)
        movement_settings = self.db_mvt.set_settings_to_movement(movement, setting)

        self.assertEqual(movement.settings.all().count(), 1)

    def test_set_settings_movement_several_settings_success(self):

        movement_name = 'squat'
        founder = User.objects.get(username='admin_user')
        equipment = self.db_mvt.set_equipment("kettlebell", founder)
        movement = self.db_mvt.set_movement(movement_name, founder, equipment)

        first_setting = self.db_mvt.set_movement_setting("Repetitions", founder)
        second_setting = self.db_mvt.set_movement_setting("Poids", founder)
        movement_settings = self.db_mvt.set_settings_to_movement(movement, first_setting, second_setting)

        self.assertEqual(movement.settings.all().count(), 2)

    def test_set_settings_movement_setting_already_exists(self):
        movement_name = 'squat'
        founder = User.objects.get(username='admin_user')
        equipment = self.db_mvt.set_equipment("kettlebell", founder)
        movement = self.db_mvt.set_movement(movement_name, founder, equipment)

        first_setting = self.db_mvt.set_movement_setting("Repetitions", founder)
        movement_settings = self.db_mvt.set_settings_to_movement(movement, first_setting)

        second_setting = self.db_mvt.set_movement_setting("Poids", founder)
        movement_settings = self.db_mvt.set_settings_to_movement(movement, first_setting, second_setting)
        self.assertEqual(movement.settings.all().count(), 2)

    def test_del_movement_success(self):
        """
        This test checks if the methods removes weel a movement
        """

        # We create a movement
        movement_name = 'squat'
        founder = User.objects.get(username='admin_user')
        equipment = self.db_mvt.set_equipment("kettlebell", founder)
        movement = self.db_mvt.set_movement(movement_name, founder, equipment)

        first_setting = self.db_mvt.set_movement_setting("Repetitions", founder)
        movement_settings = self.db_mvt.set_settings_to_movement(movement, first_setting)

        second_setting = self.db_mvt.set_movement_setting("Poids", founder)
        movement_settings = self.db_mvt.set_settings_to_movement(movement, first_setting, second_setting)

        # We delete the movement
        movement_to_delete = self.db_mvt.del_movement(movement.pk)

        # We test
        movement_existence = Movement.objects.filter(name=movement.name).exists()
        self.assertFalse(movement_existence)

    def test_del_movement_associated_to_exercise(self):
        """
        This test has to checked that the method does not remove the movement if it is
        associated at least one exercise
        It will need to be done after setting all exercises features
        """


class TestDBExercise(TestCase):
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
        self.db_mvt = DBMovement()
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
        founder = User.objects.get(username='admin_user')

        exercise = self.db_exo.set_exercise(exercise_name, exercise_type, description, founder)

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

        # We create an exercise
        exercise_name = 'Angie'
        exercise_type = "RUNNING"
        description = "test exo"
        exercise = self.db_exo.set_exercise(exercise_name, exercise_type, description, founder)

        # We create one movement
        equipment = self.db_mvt.set_equipment("kettlebell", founder)
        movement = self.db_mvt.set_movement("russian swing kettlebell", founder, equipment)

        # We associate this two movements to the exercise
        exercise_mvt = self.db_exo.set_movement_to_exercise(exercise, movement)

        # We test
        self.assertEqual(exercise.movements.all().count(), 1)
        self.assertEqual(exercise_mvt.movement_number, 1)

    def test_set_several_movements_to_exercise_success(self):
        """
        This test checks if the method set_exercise registers well several
        movements to an exercise(repeting the same method several times) by
        managing correctly the field movement_number
        """
        
        #We get the user
        founder = User.objects.get(username='admin_user')

        # We create an exercise
        exercise_name = 'Angie'
        exercise_type = "RUNNING"
        description = "test exo"
        exercise = self.db_exo.set_exercise(exercise_name, exercise_type, description, founder)

        # We create one movement
        equipment = self.db_mvt.set_equipment("kettlebell", founder)
        first_mvt = self.db_mvt.set_movement("russian swing kettlebell", founder, equipment)
        second_mvt = self.db_mvt.set_movement("american swing kettlebell", founder, equipment)

        # We associate this two movements to the exercise
        exercise_first_mvt = self.db_exo.set_movement_to_exercise(exercise, first_mvt)
        exercise_second_mvt = self.db_exo.set_movement_to_exercise(exercise, second_mvt)

        # We test
        self.assertEqual(exercise.movements.all().count(), 2)
        self.assertEqual(exercise_first_mvt.movement_number, 1)
        self.assertEqual(exercise_second_mvt.movement_number, 2)

    def test_set_settings_value_to_movement_linked_to_exercise_success(self):

        ## ENVIRONMENT SET UP ##
        #We get the user
        founder = User.objects.get(username='admin_user')

        # We create an exercise
        exercise_name = 'Angie'
        exercise_type = "RUNNING"
        description = "test exo"
        exercise = self.db_exo.set_exercise(exercise_name, exercise_type, description, founder)

        # We create one movement
        equipment = self.db_mvt.set_equipment("kettlebell", founder)
        movement = self.db_mvt.set_movement("russian swing kettlebell", founder, equipment)

        # We create some settings that we linked to the movement
        repetitions = self.db_mvt.set_movement_setting("Repetitions", founder)
        weight = self.db_mvt.set_movement_setting("Poids", founder)
        movement_settings = self.db_mvt.set_settings_to_movement(movement, repetitions, weight)

        # We associate the movement to the exercise
        exercise_mvt = self.db_exo.set_movement_to_exercise(exercise, movement)

        ## TEST ##
        # We set some values for each settings linked to the movement of the exercise
        rep_value = self.db_exo.set_settings_value_to_movement_linked_to_exercise(exercise_mvt, repetitions, 10)
        weight_value = self.db_exo.set_settings_value_to_movement_linked_to_exercise(exercise_mvt, weight, 40)

        # We test
        self.assertEqual(rep_value.setting_value, 10)
        self.assertEqual(rep_value.setting, repetitions)
        self.assertEqual(rep_value.exercise_movement.exercise, exercise)
        self.assertEqual(rep_value.exercise_movement.movement, movement)

        self.assertEqual(weight_value.setting_value, 40)
        self.assertEqual(weight_value.setting, weight)
        self.assertEqual(weight_value.exercise_movement.exercise, exercise)
        self.assertEqual(weight_value.exercise_movement.movement, movement)
