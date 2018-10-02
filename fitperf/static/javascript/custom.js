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
    this.permormanceValue = Number();
    this.movements = {};
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

function Movement() {
    this.id = Number();
    this.name = String();
    this.equipment = Number();
    this.founder = String();
    this.settings = Array();
};
// ---------------------------------------------------------------
// Modal Prototypes
// ---------------------------------------------------------------

// ---- Modal Parent ----

function Modal(id) {
    this.id = id;
    this.modal = document.getElementById(this.id);
    this.title = document.getElementById(this.id + "Label");
    this.form = document.getElementById(this.id + "Form");
};

// Get value from textinputform
Modal.prototype.getFormTextInput = function(inputId) {
    return document.getElementById(inputId).value;
};

// Get option selected from select form
Modal.prototype.getFormSelectInput = function(selectId) {
    return document.getElementById(selectId).value;
};

// Get checkbox clicked from form
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

// Manage modal option through bootstrap JQuery function
Modal.prototype.pushOptions = function(option) {
    $('#' + this.id).modal(option);
};

// Change the title of the modal
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

ModalBuilder.prototype.returnSettingsMovementForm = function (movementSelected, mvtFormIndex) {

    var allSettingsElt = document.createElement("div")
    allSettingsElt.id = "Settings" + mvtFormIndex;
    
    for (i=0; i < movementSelected.settings.length; i++) {
        var formElt = document.createElement("div");
        formElt.classList.add("form-group", "d-flex", "justify-content-end");
    
        var labelElt = document.createElement("label");
        labelElt.setAttribute("for", movementSelected.name + movementSelected.settings[i] + mvtFormIndex);
        labelElt.classList.add("col-4", "col-form-label", "text-right");
        labelElt.textContent = movementSelected.settings[i];

        var divInputElt = document.createElement("div");
        divInputElt.classList.add("col-4");

        var inputElt = document.createElement("input");
        inputElt.id = movementSelected.name + movementSelected.settings[i] + mvtFormIndex;
        inputElt.setAttribute("type", "number");
        inputElt.setAttribute("required", "true");
        inputElt.classList.add("form-control", "form-control-sm");

        divInputElt.appendChild(inputElt);
        formElt.appendChild(labelElt);
        formElt.appendChild(divInputElt);
        allSettingsElt.appendChild(formElt);
    }
    return allSettingsElt;
}

ModalBuilder.prototype.returnMovementForm = function(movementsList, mvtFormIndex) {
    var formElt = document.createElement("div");
    formElt.classList.add("form-group","row", "mb-2", "d-flex", "justify-content-end");

    var labelElt = document.createElement("label");
    labelElt.setAttribute("for", "select" + mvtFormIndex);
    labelElt.textContent = mvtFormIndex + ". ";
    labelElt.classList.add("col-2", "col-form-label", "text-right");

    var divSelectElt = document.createElement("div");
    divSelectElt.classList.add("col-10", "mb-2");

    var selectElt = document.createElement("select");
    selectElt.classList.add("form-control");
    selectElt.id = "select" + mvtFormIndex;

    optionDefaultElt = document.createElement("option");
    optionDefaultElt.value = "none";
    optionDefaultElt.textContent = "Sélectionnez un mouvement";
    selectElt.appendChild(optionDefaultElt);

    for (var i = 0; i < movementsList.length; i++) {
        var optionElt = document.createElement("option");
        optionElt.setAttribute("value", movementsList[i].id);
        optionElt.textContent = movementsList[i].name;
        optionElt.value = movementsList[i].name;
        selectElt.appendChild(optionElt);
    }
    
    divSelectElt.appendChild(selectElt);
    formElt.appendChild(labelElt);
    formElt.appendChild(divSelectElt);
    
    //addEventListener change on selectElt element
    selectElt.addEventListener("change", function() {

        // We get the value of the selected option
        var mvtName = selectElt[selectElt.selectedIndex].value;

        // With nvtName, we get the adeaquate movement in movementsList
        var mvtSelected = {};
        if (mvtName != "none") {
            var i = 0
            var mvtNumb = movementsList.length;
            var notFound = true;
            while (i < mvtNumb && notFound) {
                if (mvtName != movementsList[i].name) {
                    i++;
                } else {
                    mvtSelected = movementsList[i];
                    notFound = false;
                }
            }
        }

        // We need to remove a previous settings block before pushing another one
        // These blocks have the id equal to "Settings" + mvtFormIndex : see returnMovementForm prototype
        var settingElt = document.getElementById("Settings" + mvtFormIndex); 
        if (settingElt != null) {
            settingElt.parentNode.removeChild(settingElt);
        }

        // For each setting linked to the movement, we create an text input with a number type
        mvtSettingsForm = this.returnSettingsMovementForm(mvtSelected, mvtFormIndex);
        formElt.appendChild(mvtSettingsForm);

    }.bind(this));

    return formElt;
};

ModalBuilder.prototype.addMovementBlock = function(movementsList) {

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

    // mvtFormIndex used to set-up id in selected form + order
    var mvtFormIndex = 1;
    var mvtForm = this.returnMovementForm(movementsList, mvtFormIndex);
    this.form.insertBefore(mvtForm, endHrElt);

    buttonElt.addEventListener("click", function() {
        mvtFormIndex = mvtFormIndex + 1;
        var mvtForm = this.returnMovementForm(movementsList, mvtFormIndex);
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

// ---------------------------------------------------------------
// Function to get csrf token
// ---------------------------------------------------------------

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


// ---------------------------------------------------------------
// Ajax Interactions
// ---------------------------------------------------------------

// Ajax with Promise

function getAjaxJson(url) {
    return new Promise(function (resolve, reject) {
        var xhr = new XMLHttpRequest();
        xhr.open("GET", url);
        xhr.onload = function() {
            if (this.status >= 200 && this.status < 300) {
                resolve(JSON.parse(xhr.response));
            }
            else {
                reject({
                    status: this.status,
                    statusText: this.statusText
                });
            }
        };
        xhr.onerror = function () {
            reject({
                status: this.status,
                statusText: this.statusText
            });
        };
        xhr.open("GET", url);
        xhr.send();
    });
}

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
