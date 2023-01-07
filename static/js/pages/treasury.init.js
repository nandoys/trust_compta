let form=document.getElementById("treasury_form"),treasury_table=document.getElementById("treasury_table"),accounting_field=document.getElementById("accounting-field"),accounting_additional_div=document.getElementById("accounting-additional-div"),html_label_accounting_additional='<label for="addtional-field" class="form-label" id="additional-label">Sous compte</label>',html_select_accounting_additional=`<select class="form-select" name="accounting_additional" id="accounting-additional-field" required>
                                         <option value="" disabled selected>Entrez un sous compte</option>
                                    </select>`,accounting_adjunct_div=document.getElementById("accounting-adjunct-div"),html_label_accounting_adjunct='<label for="adjunct-field" class="form-label" id="adjunct-label">Annexe</label>',html_select_accounting_adjunct=`<select class="form-select" name="accounting_adjunct" id="accounting-adjunct-field" required>
                                         <option value="" disabled selected>Entrez un annexe </option>
                                    </select>`,update_main_div=document.getElementById("update_main_div"),update_additional_div=document.getElementById("update_additional_div"),update_adjunct_div=document.getElementById("update_adjunct_div"),html_select_update_main=`<select class="form-select" name="update_main" id="update_main_field" required>
                                </select>`,html_label_update_additional='<label for="update_additional_field" class="form-label" id="update_additional_label">Sous compte</label>',html_select_update_additional=`<select class="form-select" name="update_additional" id="update_additional_field" required>
                                </select>`,html_label_update_adjunct='<label for="update_adjunct_field" class="form-label" id="update_adjunct_label">Annexe</label>',html_select_update_adjunct=`<select class="form-select" name="update_adjunct" id="update_adjunct_field" required>
                                </select>`,accounting_additional_url=form.getAttribute("data-url-accounting-additional"),accounting_adjunct_url=form.getAttribute("data-url-adjunct"),fiscal_year=form.getAttribute("data-year"),treasury_type=treasury_table.getAttribute("data-treasury-type"),treasury_api_url=treasury_table.getAttribute("data-api-url"),getEditid=0,getEdit;function editTodoList(){let n=document.getElementById("slip_number_input"),i=document.getElementById("amount_input"),l=document.getElementById("done_at_input"),c=document.getElementById("description_input");Array.from(document.querySelectorAll(".edit-list")).forEach(function(a){a.addEventListener("click",function(e){getEditid=a.getAttribute("data-edit-id");var t=new XMLHttpRequest;t.onload=function(){let d=JSON.parse(this.responseText);if(11===Object.keys(d).length){getEdit=d,update_main_div.innerHTML="",update_main_div.insertAdjacentHTML("beforeend",html_select_update_main);let t=document.getElementById("update_main_field");if(void 0!==t){var e=new XMLHttpRequest;if(e.onload=function(){var e=JSON.parse(this.responseText);const a=new Choices(t,{loadingText:"Chargement...",noResultsText:"Aucun résultat trouvé",noChoicesText:"Aucun élément à choisir",searchFields:["label"],searchResultLimit:6});let n=[];0<e.length&&Array.from(e).forEach((t,e)=>{void 0===a._store.state.choices.find(e=>e.value===t.id)&&(d.accounting_main===t.id?n.push({value:t.id,label:t.account_name,selected:!0,disabled:!1}):n.push({value:t.id,label:t.account_name,selected:!1,disabled:!1}))}),a.setChoices(n)},e.open("GET","/plan-comptable/comptes/"+treasury_type,!0),e.send(),null!=d.accounting_additional){update_additional_div.innerHTML="",update_additional_div.insertAdjacentHTML("afterbegin",html_label_update_additional),update_additional_div.insertAdjacentHTML("beforeend",html_select_update_additional);let t=document.getElementById("update_additional_field");if(void 0!==t){var e=new XMLHttpRequest;if(e.onload=function(){var e=JSON.parse(this.responseText);const a=new Choices(t,{loadingText:"Chargement...",noResultsText:"Aucun résultat trouvé",noChoicesText:"Aucun élément à choisir",searchFields:["label"],searchResultLimit:6});let n=[];0<e.length&&Array.from(e).forEach((t,e)=>{void 0===a._store.state.choices.find(e=>e.value===t.id)&&(d.accounting_additional===t.id?n.push({value:t.id,label:t.account_name,selected:!0,disabled:!1}):n.push({value:t.id,label:t.account_name,selected:!1,disabled:!1}))}),a.setChoices(n)},e.open("GET",accounting_additional_url+"?accounting_main_id="+d.accounting_main,!0),e.send(),null!=d.accounting_adjunct){update_adjunct_div.innerHTML="",update_adjunct_div.insertAdjacentHTML("afterbegin",html_label_update_adjunct),update_adjunct_div.insertAdjacentHTML("beforeend",html_select_update_adjunct);let t=document.getElementById("update_adjunct_field");void 0!==t&&((e=new XMLHttpRequest).onload=function(){var e=JSON.parse(this.responseText);const a=new Choices(t,{loadingText:"Chargement...",noResultsText:"Aucun résultat trouvé",noChoicesText:"Aucun élément à choisir",searchFields:["label"],searchResultLimit:6});let n=[];0<e.length&&Array.from(e).forEach((t,e)=>{void 0===a._store.state.choices.find(e=>e.value===t.id)&&(d.accounting_adjunct===t.id?n.push({value:t.id,label:t.adjunct_account_name,selected:!0,disabled:!1}):n.push({value:t.id,label:t.adjunct_account_name,selected:!1,disabled:!1}))}),a.setChoices(n)},e.open("GET",accounting_adjunct_url+"?accounting_additional_id="+d.accounting_additional,!0),e.send())}else update_adjunct_div.innerHTML=""}}else update_additional_div.innerHTML="",update_adjunct_div.innerHTML=""}n.value=d.slip_number,i.value=d.amount,"encaissement"===treasury_type?l.value=d.in_at:"decaissement"===treasury_type&&(l.value=d.out_at),c.value=d.more}},t.open("GET",treasury_api_url+getEditid,!0),t.send()})})}accounting_field.addEventListener("change",function(e){var e=e.detail.value,t=new XMLHttpRequest;t.onload=function(){var e=JSON.parse(this.responseText);if(0<e.length){accounting_additional_div.innerHTML="",accounting_adjunct_div.innerHTML="",accounting_additional_div.insertAdjacentHTML("afterbegin",html_label_accounting_additional),accounting_additional_div.insertAdjacentHTML("beforeend",html_select_accounting_additional);var t=document.getElementById("accounting-additional-field");const n=new Choices(t,{loadingText:"Chargement...",noResultsText:"Aucun résultat trouvé",searchFields:["label"],searchResultLimit:6});let a=[];Array.from(e).forEach((t,e)=>{void 0===n._store.state.choices.find(e=>e.value===t.id)&&a.push({value:t.id,label:t.account_name,selected:!1,disabled:!1})}),n.setChoices(a)}else accounting_additional_div.innerHTML="",accounting_adjunct_div.innerHTML=""},t.open("GET",accounting_additional_url+"?accounting_main_id="+e,!0),t.send()}),document.addEventListener("change",e=>{var t,a;"accounting-additional-field"===e.target.id&&(t=e.detail.value,(a=new XMLHttpRequest).onload=function(){var e=JSON.parse(this.responseText);if(0<e.length){accounting_adjunct_div.innerHTML="",accounting_adjunct_div.insertAdjacentHTML("afterbegin",html_label_accounting_adjunct),accounting_adjunct_div.insertAdjacentHTML("beforeend",html_select_accounting_adjunct);var t=document.getElementById("accounting-adjunct-field");const n=new Choices(t,{loadingText:"Chargement...",noResultsText:"Aucun résultat trouvé",searchFields:["label"],searchResultLimit:6});let a=[];Array.from(e).forEach((t,e)=>{void 0===n._store.state.choices.find(e=>e.value===t.id)&&a.push({value:t.id,label:t.adjunct_account_name,selected:!1,disabled:!1})}),n.setChoices(a)}else accounting_adjunct_div.innerHTML=""},a.open("GET",accounting_adjunct_url+"?accounting_additional_id="+t+"&fiscal_year="+fiscal_year,!0),a.send()),"update_main_field"===e.target.id&&(t=e.detail.value,(a=new XMLHttpRequest).onload=function(){var e=JSON.parse(this.responseText),t=(update_additional_div.innerHTML="",update_additional_div.insertAdjacentHTML("afterbegin",html_label_update_additional),update_additional_div.insertAdjacentHTML("beforeend",html_select_update_additional),document.getElementById("update_additional_field"));if(void 0!==t){const n=new Choices(t,{loadingText:"Chargement...",noResultsText:"Aucun résultat trouvé",noChoicesText:"Aucun élément à choisir",searchFields:["label"],searchResultLimit:6});let a=[];0<e.length?Array.from(e).forEach((t,e)=>{void 0===n._store.state.choices.find(e=>e.value===t.id)&&(getEdit.accounting_additional===t.id?a.push({value:t.id,label:t.account_name,selected:!0,disabled:!1}):a.push({value:t.id,label:t.account_name,selected:!1,disabled:!1}))}):(update_additional_div.innerHTML="",update_adjunct_div.innerHTML=""),n.setChoices(a)}},a.open("GET",accounting_additional_url+"?accounting_main_id="+t,!0),a.send()),"update_additional_field"===e.target.id&&(t=e.detail.value,(a=new XMLHttpRequest).onload=function(){var e=JSON.parse(this.responseText),t=(update_adjunct_div.innerHTML="",update_adjunct_div.insertAdjacentHTML("afterbegin",html_label_update_adjunct),update_adjunct_div.insertAdjacentHTML("beforeend",html_select_update_adjunct),document.getElementById("update_adjunct_field"));if(void 0!==t){const n=new Choices(t,{loadingText:"Chargement...",noResultsText:"Aucun résultat trouvé",noChoicesText:"Aucun élément à choisir",searchFields:["label"],searchResultLimit:6});let a=[];0<e.length?Array.from(e).forEach((t,e)=>{void 0===n._store.state.choices.find(e=>e.value===t.id)&&(console.log(t),getEdit.accounting_adjunct===t.id?a.push({value:t.id,label:t.adjunct_account_name,selected:!0,disabled:!1}):a.push({value:t.id,label:t.adjunct_account_name,selected:!1,disabled:!1}))}):update_adjunct_div.innerHTML="",n.setChoices(a)}},a.open("GET",accounting_adjunct_url+"?accounting_additional_id="+t,!0),a.send())}),editTodoList();