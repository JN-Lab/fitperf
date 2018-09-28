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
};

Exercise.prototype.definePerformanceType= function(exerciseType) {
    // To define performanceType according exerciseType when got
    if (exerciseType === 'MAXIMUM DE REPETITION') {
        this.performanceType = 'Nombre de répétitions';
    } else if (exerciseType === 'AMRAP' || exerciseType === 'EMOM') {
        this.performanceType = 'Temps';
    } else if (exerciseType === 'RUNNING') {
        this.performanceType = 'Distance';
    } else {
        this.performanceType = 'Nombre de tours';
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
};
// ----------------------------------
// Modal Prototypes
// ----------------------------------

// ---- Modal Parent ----

function Modal(id) {
    this.id = id;
    this.modal = document.getElementById(this.id);
    this.title = document.getElementById(this.id + "Label");
    this.form = document.getElementById(this.id + "Form");
};

Modal.prototype.getFormTextInput = function(inputId) {
    return document.getElementById(inputId).value;
};

Modal.prototype.getFormSelectInput = function(selectId) {
    return document.getElementById(selectId).value;
};

Modal.prototype.getFormCheckboxClicked = function(inputName) {
    clickedCheckboxesValues = []
    var checkboxes = document.getElementsByName(inputName);
    for (i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            clickedCheckboxesValues.push(checkboxes[i].value);
        }
    }
    return clickedCheckboxesValues;
};

Modal.prototype.pushOptions = function(option) {
    $('#' + this.id).modal(option);
};

Modal.prototype.changeTitle = function(title) {
    this.title.textContent = title;
};

// ---- Modal Child with block builder ----

function ModalBuilder(id) {
    Modal.call(this, id);
};
ModalBuilder.prototype = Object.create(Modal.prototype);
ModalBuilder.prototype.constructor = ModalBuilder;

ModalBuilder.prototype.cleanFormElt = function() {
    if (this.form.hasChildNodes()) {
        var formElts = this.form.childNodes;
        while (formElts.length > 0) {
            this.form.removeChild(formElts[0]);
        }
    }
}

ModalBuilder.prototype.addSplittedLine = function() {
    var hrElt = document.createElement('hr');
    this.form.appendChild(hrElt);
}

ModalBuilder.prototype.addFormSection = function(sectionName) {
    var sectionElt = document.createElement('h6');
    sectionElt.textContent = sectionName;
    this.form.appendChild(sectionElt);
};

ModalBuilder.prototype.returnSplittedLine = function() {
    var hrElt = document.createElement('hr');
    return hrElt
}

ModalBuilder.prototype.returnFormSection = function(sectionName) {
    var sectionElt = document.createElement('h6');
    sectionElt.textContent = sectionName;
    return sectionElt;
};

ModalBuilder.prototype.returnMovementForm = function() {
    var mvtForm = document.createElement("div");
    mvtForm.classList.add("form-control", "mb-2");
    mvtForm.textContent = "TEST";
    return mvtForm;
};

ModalBuilder.prototype.addFormTextInput = function(id, labelName, type, is_decimal) {
    var divElt = document.createElement("div");
    divElt.classList.add("form-group");

    var labelElt = document.createElement("label");
    labelElt.setAttribute("for", id);
    labelElt.textContent = labelName;

    var inputElt = document.createElement("input");
    inputElt.id = id;
    inputElt.setAttribute("required", "true");
    inputElt.classList.add("form-control");
    inputElt.setAttribute("type", type);
    if (type === "number" && is_decimal) {
        inputElt.setAttribute("step", "0.1");
    }

    divElt.appendChild(labelElt);
    divElt.appendChild(inputElt);
    this.form.appendChild(divElt);
};


ModalBuilder.prototype.addMovementBlock = function(movements) {

    var startHrElt = this.returnSplittedLine();
    this.form.appendChild(startHrElt);
    
    var sectionElt = this.returnFormSection("Mouvements");
    this.form.appendChild(sectionElt);
    
    var endHrElt = this.returnSplittedLine();
    this.form.appendChild(endHrElt);


    var buttonElt = document.createElement('button');
    buttonElt.setAttribute("type", "button");
    buttonElt.classList.add("btn", "btn-sm", "btn-outline-info");
    buttonElt.textContent = "+ Mouvement";

    var mvtForm = this.returnMovementForm();
    this.form.insertBefore(mvtForm, endHrElt);

    buttonElt.addEventListener("click", function() {
        var mvtForm = this.returnMovementForm()
        this.form.insertBefore(mvtForm, endHrElt);
    }.bind(this));

    this.form.appendChild(buttonElt);
};

ModalBuilder.prototype.addSubmitButton = function(buttonText) {
    var buttonElt = document.createElement("button");
    buttonElt.setAttribute("type", "submit");
    buttonElt.classList.add("btn", "btn-block" ,"btn-primary");
    buttonElt.textContent = buttonText;

    this.form.appendChild(buttonElt);
};

// ----------------------------------
// Function to get csrf token
// ----------------------------------

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


// ----------------------------------
// Ajax Interactions
// ----------------------------------

// Ajax Get function
function ajaxGet(url, callback) {
    var req = new XMLHttpRequest();
    req.open("GET", url);
    req.addEventListener("load", function () {
        if (req.status >= 200 && req.status < 400) {
            // appelle la fonction callback en lui passant la response de la requête
            callback(req.responseText);
        } else {
            console.error(req.status + " " + req.statusText + " " + url);
        }
    });
    req.addEventListener("error", function () {
        console.error("Erreur réseau avec l'URL " + url);
    });
    req.send(null);
}

// Ajax Post function
function ajaxPost(url, data, callback, isJson) {
    var req = new XMLHttpRequest();
    req.open("POST", url);
    req.addEventListener("load", function () {
        if (req.status >= 200 && req.status < 400) {
            // Appelle la fonction callback en lui passant la réponse de la requête
            callback(req.responseText);
        } else {
            console.error(req.status + " " + req.statusText + " " + url);
        }
    });
    req.addEventListener("error", function () {
        console.error("Erreur réseau avec l'URL " + url);
    });
    if (isJson) {
        // Définit le contenu de la requête comme étant du JSON
        req.setRequestHeader("Content-Type", "application/json");
        // Transforme la donnée du format JSON vers le format texte avant l'envoi
        data = JSON.stringify(data);
    }
    req.send(data);
}
