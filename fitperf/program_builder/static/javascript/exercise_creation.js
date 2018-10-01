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
    // Remove form component
    modalStep2.cleanFormElt();

    // Get First Exercise Elements from Step 1
    exercise.name = modalStep1.getFormTextInput("id_name");
    exercise.exerciseType = modalStep1.getFormSelectInput("id_exercise_type");
    exercise.description = modalStep1.getFormTextInput("id_description");
    exercise.performanceType = exercise.definePerformanceType(exercise.exerciseType);

    // Build Modal for Step2 according first exercise elements
    modalStep2.changeTitle(exercise.name);
    modalStep2.addFormSection("Type: " + exercise.exerciseType);
    if (exercise.exerciseType != "RUNNING") {
        modalStep2.addFormTextInput("modalStep2Performance", exercise.performanceType, "number", false);
        
        // We get all the movements and when we have them, we generate the movement blocks + end of the form
        getAjaxJson("/app/get-all-movements/", "GET")
        .then(function (response) {
            modalStep2.addMovementBlock(response);
            modalStep2.addSplittedLine();
            modalStep2.addSubmitButton("Suivant");
        })
        .catch(function (error) {
            console.log(error.status);
            console.log(error.statusText);
        })
    } else {
        // This is to manage the exercise it if is running type
            // No need movement block
            // Need decimal in performance value
        modalStep2.addFormTextInput("modalStep2Performance", exercise.performanceType, "number", true);
        modalStep2.addSplittedLine();
        modalStep2.addSubmitButton("Suivant");
    }
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
