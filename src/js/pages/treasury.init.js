let form = document.getElementById('treasury_form')

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

let accounting_additional_url = form.getAttribute('data-url-accounting-additional')

let accounting_adjunct_url = form.getAttribute('data-url-adjunct')
let fiscal_year = form.getAttribute('data-year')

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
})


