// ----------------------------
// Modal Constructor
// ----------------------------

function Modal(id, step) {
    this.id = id;
    this.modal = document.getElementById(this.id);
    this.form = document.getElementById(this.id + "Form");
}

// ----------------------------
// Movement Constructor
// ----------------------------
function Movement(name, settings) {
    this.name = name;
    this.settings = settings // Array
}



// ----------------------------
// Manage Exercise Creation
// ----------------------------

// First Step, indicate a name, an exercise type and a description
// Second Step, indicate performance value + movements if necessary
// All this things has to be managed in javascript

// Define Modal Object and its prototype

function Modal(id, step) {
    this.id = id;
    this.modal = document.getElementById(this.id);
    this.form = document.getElementById(this.id + "Form");
}



function Exercise(name, exerciseType, description) {
    this.name = name;
    this.exerciseType = exerciseType;
    this.description = description;
    this.performanceType = Str();
    this.permormanceValue = Numb();
    this.movements = {};
}

Exercise.prototype.definePerformanceType = function() {

}



function MovementInExercise() {

}

// Get Modals on Exercises List Page for Exercise Creation

var modalExerciseStep1 = new Modal('exerciseModalFormStep1', 1);
var modalExerciseStep2 = new Modal('exerciseModalFormStep2', 2);
var modalExerciseStep3 = new Modal('exerciseModalFormStep3', 3);

// Movement JSON
{
    "name": "squat",
    "settings": [
        "repetitions",
        "poids",
    ]
}

// Exercise JSON
{   
    "name": "angie",
    "description": "un truc qui fait mal",
    "completed": True,
    "exercise_type": "FORTIME",
    "performance_type": "tours",
    "performance_value": 5,
    "movements": {
        {
            "name": "squat",
            "position": 1,
            "settings": {
                "name": "repetitions",
                "number": 10,
            }
        },
        {
            "name": "push ups",
            "position": 2,
            "settings": {
                "name": "repetitions",
                "number": 20,
            }
        },
    }
}
