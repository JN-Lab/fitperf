from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import RegisterMovement
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
    db = DBMovement()
    movements = db.get_all_movements()
    new_movement_form = RegisterMovement()
    return render(request, 'movements_list.html', locals())