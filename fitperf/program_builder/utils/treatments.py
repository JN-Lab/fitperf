#! /usr/bin/env python3
# coding: utf-8
from .db_interactions import DBMovement

class DataTreatment:
    """
    This class manages all the treatments to transform:
        -> DB queries in dictionnary
        -> dictionnary in DB queries
    To reach its goals, the call use all the classes from db_interactions
    """

    def __init__(self):
        self.db_mvt = DBMovement()

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
        
        pass