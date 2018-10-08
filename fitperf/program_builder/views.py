import json
from datetime import datetime
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .forms import RegisterMovement, RegisterExerciseStep1
from .utils.db_interactions import DBMovement, DBExercise, DBTraining
from .utils.treatments import DataTreatment

def index(request):
    if request.user.is_authenticated:
        return redirect(reverse("program_builder:homepage"), locals())
    else:
        return redirect(reverse("authentification:log_in"), locals())

# Create your views here.
@login_required
def homepage(request):
    """
    This is just a view to have an homepage for the example.
    Usually, this view will be out of the application in another project
    """
    return render(request, 'homepage.html', locals())

@login_required
def movements_list(request):
    """
    This view manages the movements:
        - print the list
        - add a movement
    """

    db = DBMovement()
    if request.method == "POST":
        new_movement_form = RegisterMovement(request.POST)
        if new_movement_form.is_valid():
            name = new_movement_form.cleaned_data["name"]
            equipment = new_movement_form.cleaned_data["equipment"]
            settings = new_movement_form.cleaned_data["settings"]

            new_movement = db.set_movement(name, request.user, equipment)
            if new_movement: # For uppercase in movement name not blocked by is_valid() method
                for setting in settings:
                    new_movement_setting = db.set_settings_to_movement(new_movement, setting)
                messages.success(request, """Le mouvement a bien été créé.""")
            else:
                messages.error(request, """Le mouvement existe déjà. """)                
        else:
            messages.error(request, """Le mouvement existe déjà. """) 

        movements = db.get_all_movements()            
        return render(request, 'movements_list.html', locals())
    else:
        movements = db.get_all_movements()
        new_movement_form = RegisterMovement()
        return render(request, 'movements_list.html', locals())

@login_required
def delete_movement(request, movement_pk):
    """
    This view manages only the movement's removal
    """
    db = DBMovement()
    deleted_movement = db.del_movement(movement_pk)
    messages.success(request, """Le mouvement a été supprimé.""")

    referer = request.META.get("HTTP_REFERER")
    return redirect(referer, locals())

@login_required
def ajax_all_movements(request):
    """
    This view returns all the movements in JSON
    For JSON structure -> see JSONTreatments class > def get_all_movements
    in utils.treatments.py
    """
    treatment = DataTreatment()
    movements = treatment.get_all_movements_in_dict()

    return JsonResponse(movements, safe=False)

@csrf_protect
@login_required
def exercises_list(request):
    """
    This view manages the exercises:
        - print a list of exercise
        - create an exercise and redirect on the exercise page to finalize
    """
    db = DataTreatment()
    exercises = db.get_all_exercises_in_dict_for_user(request.user)
    new_exercise_form = RegisterExerciseStep1()
    return render(request, 'exercises_list.html', locals())

@csrf_protect
@login_required
def add_exercise(request): 
    if request.body:
        treatment = DataTreatment()
        exercise_dict = json.loads(request.body)

        new_exercise = treatment.register_exercise_from_dict(exercise_dict, request.user)
        return JsonResponse(new_exercise.pk, safe=False)
    else:
        messages.error(request, """Un problème a été rencontré.""")
        referer = request.META.get("HTTP_REFERER")
        return redirect(referer, locals())

@login_required
def exercise_page(request, exercise_pk):
    
    treatment = DataTreatment()
    exercise_dict = treatment.get_one_exercise_in_dict(exercise_pk)
    if request.method == "POST":
        db_training = DBTraining()
        db_exercise = DBExercise()
        exercise = db_exercise.get_one_exercise_by_pk(exercise_dict["id"])
        training = db_training.set_training(exercise, request.user)
        if training:
            messages.success(request, """Votre entraînement a été créé. Donnez le maximum de vous même!""")
            return redirect(reverse('program_builder:training_page', args=[str(training.pk)]))
        else:
            messages.error(request, """Un problème a été rencontré lors de la création de votre entraînement. 
                                    Veuillez réessayer s'il vous plait.""")
            return render(request, "exercise_page.html", locals())
    else:
        date = datetime.now
        return render(request, 'exercise_page.html', locals())

@login_required
def delete_exercise(request, exercise_pk):
    """
    This view manages only the exercise's removal
    """
    db = DBExercise()
    deleted_exercise = db.del_exercise(exercise_pk)
    messages.success(request, """L'exercice a été supprimé.""")

    referer = request.META.get("HTTP_REFERER")
    return redirect(referer, locals())

@login_required
def training_page(request, training_pk):

    db = DataTreatment()
    training = db.get_one_training_in_dict(training_pk)
    return render(request, 'training_page.html', locals())