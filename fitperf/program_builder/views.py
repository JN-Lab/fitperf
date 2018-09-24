from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterMovement
from .models import Movement
from .utils.db_interactions import DBMovement

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
            for setting in settings:
                new_movement_setting = db.set_settings_to_movement(new_movement, setting)

            messages.success(request, """Le mouvement a bien été créé.""")
        else:
            messages.error(request, """Le mouvement existe déjà. """) 

        movements = db.get_all_movements()            
        return render(request, 'movements_list.html', locals())
    else:
        movements = db.get_all_movements()
        new_movement_form = RegisterMovement()
        return render(request, 'movements_list.html', locals())