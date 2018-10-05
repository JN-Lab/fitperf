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
    // To define performanceType according exerciseType only for 
    // Modal Label
    // A treatment id done on backend from exercise type value
    performanceType = String();

    if (exerciseType === 'RUNNING') {
        performanceType = 'Distance';
    } else if (exerciseType === 'AMRAP' || exerciseType === 'EMOM') {
        performanceType = 'Duree';
    } else {
        performanceType = 'Nombre de rounds';
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

