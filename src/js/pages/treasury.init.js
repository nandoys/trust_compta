let form = document.getElementById('treasury_form')
let treasury_table = document.getElementById('treasury_table')


let accounting_field = document.getElementById('accounting-field')

let accounting_additional_div = document.getElementById('accounting-additional-div')
let html_label_accounting_additional = `<label for="addtional-field" class="form-label" id="additional-label">Sous compte</label>`
let html_select_accounting_additional = `<select class="form-select" name="accounting_additional" id="accounting-additional-field" required>
                                         <option value="" disabled selected>Entrez un sous compte</option>
                                    </select>`

let accounting_adjunct_div = document.getElementById('accounting-adjunct-div')
let html_label_accounting_adjunct = `<label for="adjunct-field" class="form-label" id="adjunct-label">Annexe</label>`
let html_select_accounting_adjunct = `<select class="form-select" name="accounting_adjunct" id="accounting-adjunct-field" required>
                                         <option value="" disabled selected>Entrez un annexe </option>
                                    </select>`

let update_main_div = document.getElementById('update_main_div')
let update_additional_div = document.getElementById('update_additional_div')
let update_adjunct_div = document.getElementById('update_adjunct_div')

let html_select_update_main= `<select class="form-select" name="update_main" id="update_main_field" required>
                                </select>`

let html_label_update_additional = `<label for="update_additional_field" class="form-label" id="update_additional_label">Sous compte</label>`
let html_select_update_additional= `<select class="form-select" name="update_additional" id="update_additional_field" required>
                                </select>`

let html_label_update_adjunct = `<label for="update_adjunct_field" class="form-label" id="update_adjunct_label">Annexe</label>`
let html_select_update_adjunct = `<select class="form-select" name="update_adjunct" id="update_adjunct_field" required>
                                </select>`

let accounting_additional_url = form.getAttribute('data-url-accounting-additional')

let accounting_adjunct_url = form.getAttribute('data-url-adjunct')
let fiscal_year = form.getAttribute('data-year')

let treasury_type = treasury_table.getAttribute('data-treasury-type')
let treasury_api_url = treasury_table.getAttribute('data-api-url')

let getEditid = 0;
let getEdit;

accounting_field.addEventListener('change',function (evt){

    let id_accounting = evt.detail.value

    const xhttp = new XMLHttpRequest();

    xhttp.onload = function () {
      let json_records = JSON.parse(this.responseText);

        if(json_records.length > 0) {

            accounting_additional_div.innerHTML=""
            accounting_adjunct_div.innerHTML=""

            accounting_additional_div.insertAdjacentHTML('afterbegin', html_label_accounting_additional)
            accounting_additional_div.insertAdjacentHTML('beforeend', html_select_accounting_additional)

            let accounting_additional_field = document.getElementById('accounting-additional-field')

            const choices_accounting_additional = new Choices(accounting_additional_field, {
                loadingText: 'Chargement...',
                noResultsText: 'Aucun résultat trouvé',
                searchFields: ['label'],
                searchResultLimit: 6,
            });

            let accounting_additional = []

            Array.from(json_records).forEach((data, index) => {

                const found = choices_accounting_additional._store.state.choices.find(item => item.value === data.id)

                if(found === undefined){
                    accounting_additional.push({
                        value: data.id,
                        label: data.account_name,
                        selected: false,
                        disabled: false,
                    })
                }
            });
           choices_accounting_additional.setChoices(accounting_additional)

        } else {
            accounting_additional_div.innerHTML=""
            accounting_adjunct_div.innerHTML=""
        }
    }
    xhttp.open("GET", accounting_additional_url+"?accounting_main_id="+id_accounting, true);
    xhttp.send();

})

/*
    this section handle select fields on creating new data and on updating existing data
*/
document.addEventListener('change',(evt)=>{
    if(evt.target.id === "accounting-additional-field"){
       let id_accounting = evt.detail.value

        const xhttp = new XMLHttpRequest();

       xhttp.onload = function () {
            let json_records = JSON.parse(this.responseText);

            if(json_records.length > 0) {
                accounting_adjunct_div.innerHTML=""

                accounting_adjunct_div.insertAdjacentHTML('afterbegin', html_label_accounting_adjunct)
                accounting_adjunct_div.insertAdjacentHTML('beforeend', html_select_accounting_adjunct)

                let accounting_adjunct_field = document.getElementById('accounting-adjunct-field')

                const choices_accounting_adjunct = new Choices(accounting_adjunct_field, {
                    loadingText: 'Chargement...',
                    noResultsText: 'Aucun résultat trouvé',
                    searchFields: ['label'],
                    searchResultLimit: 6,
                });

                let accounting_adjunct = []

                Array.from(json_records).forEach((data, index) => {

                    const found = choices_accounting_adjunct._store.state.choices.find(item => item.value === data.id)

                    if(found === undefined){
                        accounting_adjunct.push({
                            value: data.id,
                            label: data.adjunct_account_name,
                            selected: false,
                            disabled: false,
                        })
                    }
                });
                choices_accounting_adjunct.setChoices(accounting_adjunct)

            } else {
                accounting_adjunct_div.innerHTML=""
            }
       }

        xhttp.open("GET", accounting_adjunct_url+"?accounting_additional_id="+id_accounting+"&fiscal_year="+fiscal_year, true);
        xhttp.send();
    }
    if (evt.target.id === "update_main_field"){
        let id_accounting = evt.detail.value

        const xhttp_update_additional = new XMLHttpRequest();
        xhttp_update_additional.onload = function () {
            let json_records_additional = JSON.parse(this.responseText);

             update_additional_div.innerHTML = ""

            update_additional_div.insertAdjacentHTML('afterbegin', html_label_update_additional)
            update_additional_div.insertAdjacentHTML('beforeend', html_select_update_additional)

            let update_additional_field = document.getElementById('update_additional_field')

            if (update_additional_field !== undefined){
                const choices_update_additional = new Choices(update_additional_field, {
                                loadingText: 'Chargement...',
                                noResultsText: 'Aucun résultat trouvé',
                                noChoicesText: 'Aucun élément à choisir',
                                searchFields: ['label'],
                                searchResultLimit: 6,
                            });
                let accounting_additional = []

                if(json_records_additional.length > 0) {

                    Array.from(json_records_additional).forEach((data, index) => {
                        const found = choices_update_additional._store.state.choices.find(item => item.value === data.id)
                        if(found === undefined){
                             if( getEdit.accounting_additional === data.id){
                                accounting_additional.push({
                                    value: data.id,
                                    label: data.account_name,
                                    selected: true,
                                    disabled: false,
                                })
                            } else {
                                accounting_additional.push({
                                    value: data.id,
                                    label: data.account_name,
                                    selected: false,
                                    disabled: false,
                                })
                            }
                        }
                    });
                } else {
                    update_additional_div.innerHTML = ""
                    update_adjunct_div.innerHTML = ""
                }
                choices_update_additional.setChoices(accounting_additional)
            }
        }
        xhttp_update_additional.open("GET", accounting_additional_url+"?accounting_main_id="+id_accounting, true);
        xhttp_update_additional.send();
    }
    if(evt.target.id === "update_additional_field"){
        let id_accounting = evt.detail.value
        const xhttp_update_additional = new XMLHttpRequest();
        xhttp_update_additional.onload = function (){
            let json_records_adjunct = JSON.parse(this.responseText);

             update_adjunct_div.innerHTML = ""

            update_adjunct_div.insertAdjacentHTML('afterbegin', html_label_update_adjunct)
            update_adjunct_div.insertAdjacentHTML('beforeend', html_select_update_adjunct)

            let update_adjunct_field = document.getElementById('update_adjunct_field')

            if (update_adjunct_field !== undefined){
                const choices_update_adjunct = new Choices(update_adjunct_field, {
                                loadingText: 'Chargement...',
                                noResultsText: 'Aucun résultat trouvé',
                                noChoicesText: 'Aucun élément à choisir',
                                searchFields: ['label'],
                                searchResultLimit: 6,
                            });
                let accounting_adjunct = []

                if(json_records_adjunct.length > 0) {

                    Array.from(json_records_adjunct).forEach((data, index) => {
                        const found = choices_update_adjunct._store.state.choices.find(item => item.value === data.id)
                        if(found === undefined){
                            console.log(data)
                             if( getEdit.accounting_adjunct === data.id){
                                accounting_adjunct.push({
                                    value: data.id,
                                    label: data.adjunct_account_name,
                                    selected: true,
                                    disabled: false,
                                })
                            } else {
                                accounting_adjunct.push({
                                    value: data.id,
                                    label: data.adjunct_account_name,
                                    selected: false,
                                    disabled: false,
                                })
                            }
                        }
                    });
                } else {
                    update_adjunct_div.innerHTML = ""
                }
                choices_update_adjunct.setChoices(accounting_adjunct)
            }
        }
        xhttp_update_additional.open("GET", accounting_adjunct_url+"?accounting_additional_id="+id_accounting, true);
        xhttp_update_additional.send();

    }
})


function editTodoList() {

    let slip_number = document.getElementById('slip_number_input')
    let amount = document.getElementById('amount_input');
    let done_at = document.getElementById('done_at_input')
    let more = document.getElementById('description_input')

    Array.from(document.querySelectorAll(".edit-list")).forEach(function (elem) {
        elem.addEventListener('click', function (event) {
            getEditid = elem.getAttribute('data-edit-id');
            const xhttp = new XMLHttpRequest();

            xhttp.onload = function () {
                let json_records = JSON.parse(this.responseText);

                if(Object.keys(json_records).length === 11) {
                    getEdit = json_records

                    update_main_div.innerHTML=""
                    update_main_div.insertAdjacentHTML('beforeend', html_select_update_main)

                    let update_main_field = document.getElementById('update_main_field')

                    if(update_main_field !== undefined){

                        const xhttp_account_main = new XMLHttpRequest();
                        xhttp_account_main.onload = function () {
                            let json_records_accounting_main = JSON.parse(this.responseText);

                            const choices_update_main = new Choices(update_main_field, {
                                loadingText: 'Chargement...',
                                noResultsText: 'Aucun résultat trouvé',
                                noChoicesText: 'Aucun élément à choisir',
                                searchFields: ['label'],
                                searchResultLimit: 6,
                            });

                            let accounting_main = []

                            if(json_records_accounting_main.length > 0){
                                Array.from(json_records_accounting_main).forEach((data, index) => {

                                    const found = choices_update_main._store.state.choices.find(item => item.value === data.id)

                                    if(found === undefined){

                                        if( json_records.accounting_main === data.id){
                                            accounting_main.push({
                                                value: data.id,
                                                label: data.account_name,
                                                selected: true,
                                                disabled: false,
                                            })
                                        } else {
                                            accounting_main.push({
                                                value: data.id,
                                                label: data.account_name,
                                                selected: false,
                                                disabled: false,
                                            })
                                        }
                                    }
                                });
                            }
                            choices_update_main.setChoices(accounting_main)
                        }
                        xhttp_account_main.open("GET", "/plan-comptable/comptes/"+treasury_type, true);
                        xhttp_account_main.send();

                        if(json_records.accounting_additional != null){
                            update_additional_div.innerHTML =""

                            update_additional_div.insertAdjacentHTML('afterbegin', html_label_update_additional)
                            update_additional_div.insertAdjacentHTML('beforeend', html_select_update_additional)

                            let update_additional_field = document.getElementById('update_additional_field')

                            if(update_additional_field !== undefined){

                                const xhttp_account_additional = new XMLHttpRequest();
                                xhttp_account_additional.onload = function (){
                                    let json_records_accounting_additional = JSON.parse(this.responseText);

                                    const choices_update_additional = new Choices(update_additional_field, {
                                loadingText: 'Chargement...',
                                noResultsText: 'Aucun résultat trouvé',
                                noChoicesText: 'Aucun élément à choisir',
                                searchFields: ['label'],
                                searchResultLimit: 6,
                            });

                                    let accounting_additional = []

                                    if(json_records_accounting_additional.length > 0){
                                        Array.from(json_records_accounting_additional).forEach((data, index) => {

                                            const found = choices_update_additional._store.state.choices.find(item => item.value === data.id)

                                            if(found === undefined){

                                                if( json_records.accounting_additional === data.id){
                                                    accounting_additional.push({
                                                        value: data.id,
                                                        label: data.account_name,
                                                        selected: true,
                                                        disabled: false,
                                                    })
                                                } else {
                                                    accounting_additional.push({
                                                        value: data.id,
                                                        label: data.account_name,
                                                        selected: false,
                                                        disabled: false,
                                                    })
                                                }
                                            }
                                        });
                                    }
                                    choices_update_additional.setChoices(accounting_additional)
                                }
                                xhttp_account_additional.open("GET", accounting_additional_url+"?accounting_main_id="+json_records.accounting_main, true);
                                xhttp_account_additional.send();

                                if(json_records.accounting_adjunct != null){
                                    update_adjunct_div.innerHTML =""

                                    update_adjunct_div.insertAdjacentHTML('afterbegin', html_label_update_adjunct)
                                    update_adjunct_div.insertAdjacentHTML('beforeend', html_select_update_adjunct)

                                    let update_adjunct_field = document.getElementById('update_adjunct_field')

                                    if(update_adjunct_field !== undefined){
                                        const xhttp_account_adjunct = new XMLHttpRequest();
                                        xhttp_account_adjunct.onload = function (){
                                            let json_records_accounting_adjunct = JSON.parse(this.responseText);

                                            const choices_update_adjunct = new Choices(update_adjunct_field, {
                                        loadingText: 'Chargement...',
                                        noResultsText: 'Aucun résultat trouvé',
                                        noChoicesText: 'Aucun élément à choisir',
                                        searchFields: ['label'],
                                        searchResultLimit: 6,
                                    });

                                            let accounting_adjunct = []

                                            if(json_records_accounting_adjunct.length > 0){
                                                Array.from(json_records_accounting_adjunct).forEach((data, index) => {

                                                    const found = choices_update_adjunct._store.state.choices.find(item => item.value === data.id)

                                                    if(found === undefined){

                                                        if( json_records.accounting_adjunct === data.id){
                                                            accounting_adjunct.push({
                                                                value: data.id,
                                                                label: data.adjunct_account_name,
                                                                selected: true,
                                                                disabled: false,
                                                            })
                                                        } else {
                                                            accounting_adjunct.push({
                                                                value: data.id,
                                                                label: data.adjunct_account_name,
                                                                selected: false,
                                                                disabled: false,
                                                            })
                                                        }
                                                    }
                                                });
                                            }
                                            choices_update_adjunct.setChoices(accounting_adjunct)

                                        }
                                        xhttp_account_adjunct.open("GET", accounting_adjunct_url+"?accounting_additional_id="+json_records.accounting_additional, true);
                                        xhttp_account_adjunct.send();
                                    }

                                } else {

                                    update_adjunct_div.innerHTML =""
                                }
                            }

                        } else {
                            update_additional_div.innerHTML =""
                            update_adjunct_div.innerHTML =""
                        }
                    }

                    slip_number.value = json_records.slip_number
                    amount.value = json_records.amount
                    if(treasury_type === 'encaissement'){
                        done_at.value = json_records.in_at
                    } else if (treasury_type === 'decaissement') {
                        done_at.value = json_records.out_at
                    }
                    more.value = json_records.more

                } else {

                }

                /*
                todoList = todoList.map(function (item) {
                        if (item.id == getEditid) {
                            editFlag = true;
                            document.getElementById("amount-input").value = item.id;

                            flatpickr("#task-duedate-input", {
                                dateFormat: "d M, Y",
                                defaultDate: item.dueDate
                            });

                            var statusSelec = new DOMParser().parseFromString(item.status, "text/html").body;
                            statusVal.setChoiceByValue(statusSelec.innerHTML);

                            var prioritySelec = new DOMParser().parseFromString(item.priority, "text/html").body;
                            priorityVal.setChoiceByValue(prioritySelec.innerHTML);

                            Array.from(document.querySelectorAll(".select-element .dropdown-menu ul li a")).forEach(function (subElem) {
                                var nameelem = subElem.querySelector(".flex-grow-1").innerHTML;

                                item.assignedto.map(function (subItem) {
                                    if (subItem.assigneeName == nameelem) {
                                        subElem.classList.add("active");
                                        var folderListdata = document.getElementById("assignee-member");
                                        if(subElem.classList.contains("active")){
                                            folderlisthtml =
                                            '<a href="javascript: void(0);" class="avatar-group-item mb-2" data-img="'+subItem.assigneeImg+'"  data-bs-toggle="tooltip" data -bs-placement="top" title="'+subItem.assigneeName+'">\
                                            <img src="'+subItem.assigneeImg+'" alt="" class="rounded-circle avatar-xs" />\
                                            </a>';

                                            folderListdata.insertAdjacentHTML("beforeend", folderlisthtml);
                                            tooltipElm();
                                        }
                                    }

                                    return subElem;
                                });
                            });

                            var assigneelength = document.querySelectorAll('.select-element .dropdown-menu .dropdown-item.active').length;
                            document.getElementById("total-assignee").innerHTML = assigneelength

                        }
                        return item;
                    });
                 */

            }
            xhttp.open("GET", treasury_api_url+getEditid, true);
            xhttp.send();
        });
    });
};

editTodoList()

