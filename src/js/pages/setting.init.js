/*
Template Name: Velzon - Admin & Dashboard Template
Author: Themesbrand
Website: https://Themesbrand.com/
Contact: Themesbrand@gmail.com
File: Profile-setting init js
*/

// Profile Foreground Img
if (document.querySelector("#profile-foreground-img-file-input")) {
    document.querySelector("#profile-foreground-img-file-input").addEventListener("change", function () {
        var preview = document.querySelector(".profile-wid-img");
        var file = document.querySelector(".profile-foreground-img-file-input")
            .files[0];
        var reader = new FileReader();
        reader.addEventListener(
            "load",
            function () {
                preview.src = reader.result;
            },
            false
        );
        if (file) {
            reader.readAsDataURL(file);
        }
    });
}

// Profile Foreground Img
if (document.querySelector("#profile-img-file-input")) {
    document.querySelector("#profile-img-file-input").addEventListener("change", function () {
        var preview = document.querySelector(".user-profile-image");
        var file = document.querySelector(".profile-img-file-input").files[0];
        var reader = new FileReader();
        reader.addEventListener(
            "load",
            function () {
                preview.src = reader.result;
            },
            false
        );
        if (file) {
            reader.readAsDataURL(file);
        }
    });
}


var count = 2;

// var genericExamples = document.querySelectorAll("[data-trigger]");
// for (i = 0; i < genericExamples.length; ++i) {
//     var element = genericExamples[i];
//     new Choices(element, {
//         placeholderValue: "This is a placeholder set in the config",
//         searchPlaceholderValue: "This is a search placeholder",
//         searchEnabled: false,
//     });
// }

function deleteEl(eleId) {
    d = document;
    var ele = d.getElementById(eleId);
    var parentEle = d.getElementById('newlink');
    parentEle.removeChild(ele);
}

function selectedTab(evt){
    const tag_id = evt.id
    localStorage.setItem('selectedTab', tag_id)
}

function getAccounting(event){
    const accounting_id = event.getAttribute('data-id')
     const accounting_name = event.getAttribute('data-name')

    const accounting_input = document.getElementById('accounting-id')
    const accounting_label = document.getElementById('accounting-alert')
    accounting_input.value = accounting_id

    accounting_label.innerText = 'Ajoutez une alerte pour le compte '+accounting_name
}

document.addEventListener("DOMContentLoaded", () => {
    const selectedTab = localStorage.getItem('selectedTab')

    if(selectedTab){
        const activeLink = document.getElementsByClassName('nav-link active')
        activeLink.item(2).classList.remove('active')

        const paneTab = document.getElementsByClassName('tab-pane active')
        paneTab.item(2).classList.remove('active')

        const link = document.getElementById(selectedTab)
        link.classList.add('active')

        const paneId = link.getAttribute('data-name')
        const pane = document.getElementById(paneId)
        pane.classList.add('active')

    }
});

modal_warning = document.getElementById('set_warning')

modal_warning.addEventListener('shown.bs.modal', ()=>{
    const accounting_input = document.getElementById('accounting-id').value
    const accounting_label = document.getElementById('accounting-alert')

    if (accounting_input === ""){

         accounting_label.innerText = 'Ajoutez des alertes pour tous les comptes'
    }

    console.log(accounting_input)
})

modal_warning.addEventListener('hide.bs.modal', ()=>{
    const accounting_input = document.getElementById('accounting-id')
    const accounting_label = document.getElementById('accounting-alert')

    accounting_input.value = ""
    accounting_label.innerText = ""
})