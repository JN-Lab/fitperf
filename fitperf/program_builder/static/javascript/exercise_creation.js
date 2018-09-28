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

// ---- Initialization -----

var exercise = new Exercise();
var modalStep1 = new Modal('exerciseModalStep1');
var modalStep2 = new Modal('exerciseModalStep2');

// ---- Step 1 -----

var exercise = new Exercise();
var modalStep1 = new Modal('exerciseModalStep1');
var modalStep2 = new ModalBuilder('exerciseModalStep2');

modalStep1.form.addEventListener("submit", function(e) {

    // Get First Exercise Elements from Step 1
    exercise.name = modalStep1.getFormTextInput("id_name");
    exercise.exerciseType = modalStep1.getFormSelectInput("id_exercise_type");
    exercise.description = modalStep1.getFormTextInput("id_description");

    // Build Modal for Step2 according first exercise elements
    modalStep2.changeTitle(exercise.name);
    modalStep2.addFormSection("Type: " + exercise.exerciseType);
    modalStep2.addFormTextInput("modalStep2Performance", exercise.performanceType);
    modalStep2.addSplittedLine();
    modalStep2.addSubmitButton("Suivant");
    // -----------
    // -> Premiere etape: definir formulaire pour récuperer la performance value 
    // -> Si performance type impose le choix de mouvement alors:
        // -> Recupérer tous les mouvements disponibles ainsi que leurs settings
        // -> Rajouter le bloc pour les mouvements les éléments au formulaire 
    // -----------

    // Hide Modal for Step1 and show Modal for Step 2 
    modalStep1.pushOptions('hide');
    modalStep2.pushOptions('show');
    e.preventDefault();
})

// ---- Step 2 -----
