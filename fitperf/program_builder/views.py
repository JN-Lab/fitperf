from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterMovement, RegisterExerciseStep1
from .utils.db_interactions import DBMovement, DBExercise

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
def exercises_list(request):
    """
    This view manages the exercises:
        - print a list of exercise
        - create an exercise and redirect on the exercise page to finalize
    """
    db = DBExercise()
    if request.method == "POST":
        new_exercise_form = RegisterExerciseStep1(request.POST)
        if new_exercise_form.is_valid():
            name = new_exercise_form.cleaned_data["name"]
            exercise_type = new_exercise_form.cleaned_data["exercise_type"]
            description = new_exercise_form.cleaned_data["description"]

            new_exercise = db.set_exercise(name, exercise_type, description, request.user)
            if new_exercise:
                messages.success(request, """L'exercice a bien été créé. Afin de le finaliser,
                                 veuillez construire votre entraînement. """)
                return redirect('program_builder:exercise_page', exercise_pk=str(new_exercise.pk))
            else:
                messages.error(request, """Un problème a eu lieu lors de la création de l'exercice.
                               Veuillez recommencer s'il vous plaît.""")
                return render(request, 'exercises_list.html', locals)
        else:
            messages.error(request, """Les informations que vous avez indiqué semblent présenter
                           des erreurs.""")
            return render(request, 'exercises_list.html', locals)
    else:
        new_exercise_form = RegisterExerciseStep1()
        return render(request, 'exercises_list.html', locals())

@login_required
def exercise_page(request, exercise_pk):
    
    db = DBExercise()
    exercise = db.get_one_exercise_by_pk(exercise_pk)
    return render(request, 'exercise_page.html', locals())