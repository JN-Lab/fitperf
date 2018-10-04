// ---------------------------------------------------------------
// Exercise Prototype
// ---------------------------------------------------------------

function Exercise() {
    this.id = Number();
    this.name = String();
    this.exerciseType = String();
    this.description = String();
    this.founder = String();
    this.performanceType = String();
    this.performanceValue = Number();
    this.movements = Array();
};

Exercise.prototype.definePerformanceType = function(exerciseType) {
    // To define performanceType according exerciseType
    performanceType = String();

    if (exerciseType === 'MAXIMUM DE REPETITION') {
        performanceType = 'Nombre de répétitions';
    } else if (exerciseType === 'AMRAP' || exerciseType === 'EMOM') {
        performanceType = 'Temps';
    } else if (exerciseType === 'RUNNING') {
        performanceType = 'Distance';
    } else {
        performanceType = 'Nombre de tours';
    }
    return performanceType;
};

// ---------------------------------------------------------------
// Movement Prototype
// ---------------------------------------------------------------

function Movement(name, order) {
    this.name = name;
    this.order = order;
    this.settings = Array();
};

function Setting(name, value) {
    this.name = name;
    this.value = value;
}

