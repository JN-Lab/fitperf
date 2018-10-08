#! /usr/bin/env python3
# coding: utf-8
import math
from .db_interactions import DBMovement, DBExercise, DBTraining

class DataTreatment:
    """
    This class manages all the treatments to transform:
        -> DB queries in dictionnary
        -> dictionnary in DB queries
    To reach its goals, the call use all the classes from db_interactions
    """

    def __init__(self):
        self.db_mvt = DBMovement()
        self.db_exercise = DBExercise()
        self.db_training = DBTraining()

    def get_all_movements_in_dict(self):
        """
        This method transforms the query set with all movement into a list of dictionnaries:
        [
            {   
                "id": movement.pk,
                "name": movement.name,
                "equipement": movement.equipment.name,
                "settings": [movement.settings.name]
            }
        ]
        """
        mvts_list = []
        mvts_queryset = self.db_mvt.get_all_movements()
        
        for mvt in mvts_queryset:
            mvt_dict = {
                "id": mvt.pk,
                "name": mvt.name,
                "equipement": mvt.equipment.name,
                "settings": [setting.name for setting in mvt.settings.all()]
            }
            mvts_list.append(mvt_dict)
        
        return mvts_list

    def register_exercise_from_dict(self, exercise_dict, user):
        """
        This method registers an exercise and all its links with movements in database
        from a dictionnary:
        {
            "name": "exercise_name",
            "exerciseType": "exercise_type",
            "description": "description",
            "goalType", "goal_type",
            "goalValue", "goal_value",
            "movements" : [
                {
                    "id": "movement_id",
                    "name" : "movement_name",
                    "order": "movement_order",
                    "settings": [
                        {
                            "name": "setting_name",
                            "value": "setting_value,
                        },
                        ...
                    ]
                },
                ...
            ]
        }
        """
        goal_value_converted = self._manage_goal_value(exercise_dict["goalType"], exercise_dict["goalValue"])
        exercise = self.db_exercise.set_exercise(exercise_dict["name"],
                                                exercise_dict["exerciseType"],
                                                exercise_dict["description"],
                                                exercise_dict["goalType"],
                                                goal_value_converted,
                                                user)
        if exercise:
            for movement_dict in exercise_dict["movements"]:
                movement = self.db_mvt.get_one_movement(movement_dict["name"])
                movement_associated = self.db_exercise.set_movement_to_exercise(exercise, 
                                                          movement,
                                                          movement_dict["order"])
                for setting_dict in movement_dict["settings"]:
                    setting = self.db_mvt.get_one_movement_setting(setting_dict["name"])
                    setting_associated = self.db_exercise.set_settings_value_to_movement_linked_to_exercise(movement_associated,
                                                                                                            setting,
                                                                                                            setting_dict["value"])

        return exercise

    def _manage_goal_value(self, goal_type, goal_value):
        """
        This private method ensure securiy and logic before registering numerical
        value in performance_value field in Exercise model.
        To be sure to integrate the good integer in db
        """
        
        if goal_type == "Distance" and goal_value < 100:
            goal_value = goal_value * 1000

        return int(goal_value)




    def get_all_exercises_dict_linked_to_one_user(self, user):
        """
        This method returns all the information of the exercises associated with a user
        in a list of dict:
            [
                {
                    "id": "exercise primary_key",
                    "name": "exercise.name",
                    "exerciseType": "exercise_type",
                    "description": "description",
                    "goalType": "goal_type",
                    "goalValue": "goal_value",
                    "is_default": False,
                    "done": "False or True",
                    "pb: "best performance_value",
                    "movements" : [
                        {
                            "name" : "movement_name",
                            "order": "movement_order",
                            "settings": [
                                {
                                    "name": "setting_name",
                                    "value": "setting_value,
                                },
                                ...
                            ]
                        },
                        ...
                    ]
                }
            ]
        """       
        exercises = self.db_exercise.get_all_user_exercises(user)
        exercise_list = []
        for exercise in exercises:
            exercise_dict = self.get_one_exercise_in_dict_linked_to_one_user(exercise.pk, user)
            if exercise_dict:
                exercise_list.append(exercise_dict)
        return exercise_list

    def get_one_exercise_in_dict_linked_to_one_user(self, exercise_pk, user):
        """
        This method returns all the information linked to an exercise in a dictionnary.
        The method uses the primary key to get the targeted exercise
            {
                "id": "exercise primary_key",
                "name": "exercise.name",
                "exerciseType": "exercise_type",
                "description": "description",
                "goalType": "goal_type",
                "goalValue": "goal_value",
                "is_default": False,
                "done": "False or True",
                "pb: "best performance_value",
                "movements" : [
                    {
                        "name" : "movement_name",
                        "order": "movement_order",
                        "settings": [
                            {
                                "name": "setting_name",
                                "value": "setting_value,
                            },
                            ...
                        ]
                    },
                    ...
                ]
            }
        """

        completed = True
        exercise = self.db_exercise.get_one_exercise_by_pk(exercise_pk)
        exercise_dict = {
            "id": "",
            "name": "",
            "exerciseType": "",
            "description": "",
            "goalType": "",
            "goalValue": 0,
            "is_default": False,
            "pb": 0,
            "movements": []
        }

        # We push all informations from exercise except movements
        try:
            exercise_dict["id"] = exercise.pk
        except:
            completed = False
        
        try:
            exercise_dict["name"] = exercise.name
        except:
            completed = False

        try:
            exercise_dict["description"] = exercise.description
        except:
            exercise_dict["description"] = ""

        try:
            exercise_dict["exerciseType"] = exercise.exercise_type
        except:
            completed = False

        try:
            exercise_dict["goalType"] = exercise.goal_type
        except:
            completed = False

        try:
            exercise_dict["goalValue"] = exercise.goal_value
        except:
            completed = False

        try:
            exercise_dict["is_default"] = exercise.is_default
        except:
            completed = False

        try:
            exercise_dict["pb"] = self._get_best_perf_for_one_exercise(exercise, user)
        except:
            completed = False

        try:
            exercise_dict["movements"] = self._get_movements_dict_linked_to_exercise(exercise) 
        except:
            completed = False

        if completed:
            return exercise_dict
        else:
            return None

    def _get_best_perf_for_one_exercise(self, exercise, user):
        """
        This private method return a personal record if the user register a training with this exercise
        """
        trainings = self.db_training.get_all_trainings_from_one_user_from_one_exercise(exercise, user)
        if trainings:
            pb = 0
            for training in trainings:
                if training.performance_value > pb:
                    pb = training.performance_value
            return pb
        else:
            return None

    def _get_movements_dict_linked_to_exercise(self,exercise):
        """
        This private method gets all the movements linked to an exercise,
        transforms them into dict and push them in a list
        """
        
        completed = True
        movements_list = []
        # We Get all movements linked to the exercise
        movements_linked = self.db_exercise.get_all_movements_linked_to_exercise(exercise)
        for movement_linked in movements_linked:
            movement_dict = {
                "id": "",
                "name": "",
                "order": "",
                "settings": [],
            }

            try:
                movement_dict["id"] = movement_linked.movement.pk
            except:
                completed = False
            
            try:
                movement_dict["name"] = movement_linked.movement.name
            except:
                completed = False

            try:
                movement_dict["order"] = movement_linked.movement_number
            except:
                completed = False
            
            # We get all settings linked to a movement
            settings_linked = self.db_exercise.get_all_settings_linked_to_movement_linked_to_exercise(movement_linked)
            for setting_linked in settings_linked:
                setting_dict = {
                    "name": "",
                    "value": "",
                }

                try:
                    setting_dict["name"] = setting_linked.setting.name
                except:
                    completed = False

                try:
                    setting_dict["value"] = setting_linked.setting_value
                except:
                    completed = False

                movement_dict["settings"].append(setting_dict)                
            movements_list.append(movement_dict)
            
        if completed:
            return movements_list
        else:
            return None

    def get_one_training_in_dict(self, training_pk):
        """
        This method returns all the information linked to a training in a dictionnary.
        The method uses the primary key to get the targeted training:
            {
                "id": "training primary_key",
                "date": "training date",
                "done": "training boolean",
                "performanceType": "training perf_type",
                "performanceValue": "training perf_value",
                "exercise": {
                    "id": "exercise primary_key",
                    "name": "exercise.name",
                    "exerciseType": "exercise_type",
                    "description": "description",
                    "goalType": "goal_type",
                    "goalValue": "goal_value",
                    "is_default": False,
                    "movements" : [
                        {
                            "name" : "movement_name",
                            "order": "movement_order",
                            "settings": [
                                {
                                    "name": "setting_name",
                                    "value": "setting_value,
                                },
                                ...
                            ]
                        },
                        ...
                    ]
                }
            }
        """
        completed = True
        training = self.db_training.get_one_training_from_pk(training_pk)
        training_dict = {
            "id": "",
            "date": "",
            "done": "",
            "performanceType": "",
            "performanceValue": "",
            "exercise": {},
        }

        try:
            training_dict["id"] = training.pk
        except:
            completed = False
        
        try:
            training_dict["date"] = training.date
        except:
            completed = False

        try:
            training_dict["done"] = training.done
        except:
            completed = False
        
        try:
            training_dict["performanceType"] = training.performance_type
        except:
            completed = False
        
        try:
            training_dict["performanceValue"] = training.performance_value
        except:
            completed = False

        try:
            training_dict["exercise"] = self.get_one_exercise_in_dict(training.exercise.pk)
        except:
            completed = False

        if completed:
            return training_dict
        else:
            return None

    def get_all_trainings_per_user_in_dict(self, user):    
        """
        This method returns all the trainings realized from a user in a list
        of dict:
            [
                {
                    "id": "training primary_key",
                    "date": "training date",
                    "done": "training boolean",
                    "performanceType": "training perf_type",
                    "performanceValue": "training perf_value",
                    "exercise": {
                        "id": "exercise primary_key",
                        "name": "exercise.name",
                        "exerciseType": "exercise_type",
                        "description": "description",
                        "goalType": "goal_type",
                        "goalValue": "goal_value",
                        "is_default": False,
                        "movements" : [
                            {
                                "name" : "movement_name",
                                "order": "movement_order",
                                "settings": [
                                    {
                                        "name": "setting_name",
                                        "value": "setting_value,
                                    },
                                    ...
                                ]
                            },
                            ...
                        ]
                    }
                },
                ...
            ]
        """
        training_list= []
        trainings = self.db_training.get_all_trainings_from_one_user(user)
        for training in trainings:
            training_dict = self.get_one_training_in_dict(training.pk)
            if training_dict:
                training_list.append(training_dict)

        return training_list

    def get_all_trainings_per_user_linked_to_an_exercise(self, exercise, user):
        """
        This method returns all the trainings realized from a user in a list
        of dict:
            [
                {
                    "id": "training primary_key",
                    "date": "training date",
                    "done": "training boolean",
                    "performanceType": "training perf_type",
                    "performanceValue": "training perf_value",
                    "exercise": {
                        "id": "exercise primary_key",
                        "name": "exercise.name",
                        "exerciseType": "exercise_type",
                        "description": "description",
                        "goalType": "goal_type",
                        "goalValue": "goal_value",
                        "is_default": False,
                        "movements" : [
                            {
                                "name" : "movement_name",
                                "order": "movement_order",
                                "settings": [
                                    {
                                        "name": "setting_name",
                                        "value": "setting_value,
                                    },
                                    ...
                                ]
                            },
                            ...
                        ]
                    }
                },
                ...
            ]
        """
        training_list= []
        trainings = self.db_training.get_all_trainings_from_one_user_from_one_exercise(exercise, user)
        for training in trainings:
            training_dict = self.get_one_training_in_dict(training.pk)
            if training_dict:
                training_list.append(training_dict)

        return training_list

###################################################
# Maybe these methods will be deleted bedore v1.0 #
###################################################

    def get_all_exercises_in_dict(self):
        """
        This method gets all the exercises and returns them in a list of dictionnary
        -> see _build_exercises_list_of_dict method
        """
        exercises = self.db_exercise.get_all_exercises()
        exercises_list = self._build_exercises_list_of_dict(exercises)
        if exercises_list:
            return exercises_list

    def get_all_exercises_in_dict_for_user(self, user):
        """
        This method gets all the exercises by default + exercise created by a specific user
        and returns them in a list of dictionnary -> see _build_exercises_list_of_dict method
        """
        exercises = self.db_exercise.get_all_user_exercises(user)
        exercises_list = self._build_exercises_list_of_dict(exercises)
        if exercises_list:
            return exercises_list

    def _build_exercises_list_of_dict(self, exercises):
        """
        This method returns all the exercises from the queryset into a list of dictionnaries:
        [
            {
                "id": "exercise primary_key",
                "name": "exercise.name",
                "exerciseType": "exercise_type",
                "description": "description",
                "goalType": "goal_type",
                "goalValue": "goal_value",
                "is_default": False,
                "movements" : [
                    {
                        "name" : "movement_name",
                        "order": "movement_order",
                        "settings": [
                            {
                                "name": "setting_name",
                                "value": "setting_value,
                            },
                            ...
                        ]
                    },
                    ...
                ]
            }
        ]
        """

        completed = True
        exercise_list = []

        for exercise in exercises:
            exercise_dict = {
                "id": "",
                "name": "",
                "exerciseType": "",
                "description": "",
                "goalType": "",
                "goalValue": "",
                "is_default": False,
                "movements": []
            }

            # We push all informations from exercise except movements
            try:
                exercise_dict["id"] = exercise.pk
            except:
                completed = False
            
            try:
                exercise_dict["name"] = exercise.name
            except:
                completed = False

            try:
                exercise_dict["description"] = exercise.description
            except:
                exercise_dict["description"] = ""

            try:
                exercise_dict["exerciseType"] = exercise.exercise_type
            except:
                completed = False

            try:
                exercise_dict["goalType"] = exercise.goal_type
            except:
                completed = False

            try:
                exercise_dict["goalValue"] = exercise.goal_value
            except:
                completed = False

            try:
                exercise_dict["is_default"] = exercise.is_default
            except:
                completed = False

            try:
                exercise_dict["movements"] = self._get_movements_dict_linked_to_exercise(exercise) 
            except:
                completed = False

            exercise_list.append(exercise_dict)

        if completed:
            return exercise_list
        else:
            return None


    def get_one_exercise_in_dict(self, exercise_pk):
        """
        This method returns all the information linked to an exercise in a dictionnary.
        The method uses the primary key to get the targeted exercise
            {
                "id": "exercise primary_key",
                "name": "exercise.name",
                "exerciseType": "exercise_type",
                "description": "description",
                "goalType": "goal_type",
                "goalValue": "goal_value",
                "is_default": False,
                "movements" : [
                    {
                        "name" : "movement_name",
                        "order": "movement_order",
                        "settings": [
                            {
                                "name": "setting_name",
                                "value": "setting_value,
                            },
                            ...
                        ]
                    },
                    ...
                ]
            }
        """

        completed = True
        exercise = self.db_exercise.get_one_exercise_by_pk(exercise_pk)
        exercise_dict = {
            "id": "",
            "name": "",
            "exerciseType": "",
            "description": "",
            "goalType": "",
            "goalValue": "",
            "is_default": False,
            "movements": []
        }

        # We push all informations from exercise except movements
        try:
            exercise_dict["id"] = exercise.pk
        except:
            completed = False
        
        try:
            exercise_dict["name"] = exercise.name
        except:
            completed = False

        try:
            exercise_dict["description"] = exercise.description
        except:
            exercise_dict["description"] = ""

        try:
            exercise_dict["exerciseType"] = exercise.exercise_type
        except:
            completed = False

        try:
            exercise_dict["goalType"] = exercise.goal_type
        except:
            completed = False

        try:
            exercise_dict["goalValue"] = exercise.goal_value
        except:
            completed = False

        try:
            exercise_dict["is_default"] = exercise.is_default
        except:
            completed = False

        try:
            exercise_dict["movements"] = self._get_movements_dict_linked_to_exercise(exercise) 
        except:
            completed = False

        if completed:
            return exercise_dict
        else:
            return None