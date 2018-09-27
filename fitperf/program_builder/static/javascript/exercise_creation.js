// -------------------------------
// Exercise Prototype
// -------------------------------

function Exercise() {
    this.id = Number();
    this.name = String();
    this.exerciseType = String();
    this.description = String();
    this.founder = String();
    this.performanceType = String();
    this.permormanceValue = Number();
    this.movements = {};

    this.definePerformanceType(this.exerciseType);
};

Exercise.prototype.definePerformanceType= function(exerciseType) {
    if (exerciseType === 'MAXIMUM DE REPETITION') {
        this.performanceType = 'repetitions';
    } else if (exerciseType === 'AMRAP' | exerciseType === 'EMOM') {
        this.performanceType = 'duree';
    } else if (exerciseType === 'RUNNING') {
        this.performanceType = 'distance';
    } else {
        this.performanceType = 'tours';
    }
};

// -------------------------------
// Movement Prototype
// -------------------------------

function Movement() {
    this.id = Number();
    this.name = String();
    this.equipment = Number();
    this.founder = String();
    this.settings = Array();
}

// -------------------------------
// Exercise Creation
// -------------------------------

// ---- Step 1 -----

var exercise = new Exercise();
var modalStep1 = new Modal('exerciseModalStep1');
modalStep1.form.addEventListener("submit", function(e) {
    exercise.name = modalStep1.getFormTextInput("id_name");
    exercise.exerciseType = modalStep1.getFormSelectInput("id_exercise_type");
    exercise.description = modalStep1.getFormTextInput("id_description");
$('#exerciseModalStep1').modal('hide');
    e.preventDefault();
})