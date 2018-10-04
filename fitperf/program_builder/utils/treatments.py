#! /usr/bin/env python3
# coding: utf-8
import math
from .db_interactions import DBMovement, DBExercise

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
            "performanceType", "performance_type",
            "performanceValue", "performance_value",
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
        performance_value_converted = self._manage_performance_value(exercise_dict["performanceType"], exercise_dict["performanceValue"])
        exercise = self.db_exercise.set_exercise(exercise_dict["name"],
                                                exercise_dict["exerciseType"],
                                                exercise_dict["description"],
                                                exercise_dict["performanceType"],
                                                performance_value_converted,
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

    def _manage_performance_value(self, performance_type, performance_value):
        """
        This private method ensure securiy and logic before registering numerical
        value in performance_value field in Exercise model.
        To be sure to integrate the good integer in db
        """
        
        if performance_type == "Distance" and performance_value < 100:
            performance_value = performance_value * 1000

        return int(performance_value)

    def get_all_exercises_in_dict(self):
        """
        This gets all the exercises from the database and set them in a list of dictionnaries:
        [
            {
                "id": "exercise primary_key",
                "founder": "founder"
                "name": "exercise.name",
                "exerciseType": "exercise_type",
                "description": "description",
                "performanceType", "performance_type",
                "performanceValue", "performance_value",
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
        pass