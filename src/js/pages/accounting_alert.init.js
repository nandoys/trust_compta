var perPage = 8;

//Table
var options = {
    valueNames: [
        "id",
        "accounting_number",
        "accounting_name",
        "accounting_type",
    ],
    page: perPage,
    pagination: true,
    plugins: [
        ListPagination({
            left: 2,
            right: 2
        })
    ]
};

var addModal = document.getElementById('add-modal-btn'),
 editsModal = document.getElementsByClassName('edit-modal-btn'),

modalLabel = document.getElementById('modalLabel'),

addBtn = document.getElementById('add-btn'),
editBtn = document.getElementById('edit-btn'),
removeBtns = document.getElementsByClassName("remove-item-btn"),

idField = document.getElementById('id-field'),
accountNumber= document.getElementById('accounting-number-field'),
accountName= document.getElementById('accounting-name-field'),
accountDesc= document.getElementById('accounting-desc-field'),
accountType = document.getElementById('accounting-type-field');
deleteField = document.getElementById('delete-item')

// Init list
if (document.getElementById("accountingList"))
    var accountingList = new List("accountingList", options).on("updated", function (list) {
        list.matchingItems.length == 0 ?
            (document.getElementsByClassName("noresult")[0].style.display = "block") :
            (document.getElementsByClassName("noresult")[0].style.display = "none");
        var isFirst = list.i == 1;
        var isLast = list.i > list.matchingItems.length - list.page;
        // make the Prev and Nex buttons disabled on first and last pages accordingly
        (document.querySelector(".pagination-prev.disabled")) ? document.querySelector(".pagination-prev.disabled").classList.remove("disabled"): '';
        (document.querySelector(".pagination-next.disabled")) ? document.querySelector(".pagination-next.disabled").classList.remove("disabled"): '';
        if (isFirst) {
            document.querySelector(".pagination-prev").classList.add("disabled");
        }
        if (isLast) {
            document.querySelector(".pagination-next").classList.add("disabled");
        }
        if (list.matchingItems.length <= perPage) {
            document.querySelector(".pagination-wrap").style.display = "none";
        } else {
            document.querySelector(".pagination-wrap").style.display = "flex";
        }

        if (list.matchingItems.length == perPage) {
            document.querySelector(".pagination.listjs-pagination").firstElementChild.children[0].click()
        }

        if (list.matchingItems.length > 0) {
            document.getElementsByClassName("noresult")[0].style.display = "none";
        } else {
            document.getElementsByClassName("noresult")[0].style.display = "block";
        }
    });

    addModal.addEventListener('click', (evt) =>{
        modalLabel.innerText = "Ajouter compte"
        addBtn.style.display  = "block"
        editBtn.style.display = "none"
    })

    document.getElementById('showModal').addEventListener('hidden.bs.modal', (evt) => {
        clearFields()
    })

function update(tag){
        modalLabel.innerText = "Modifier compte"
        addBtn.style.display  = "none"
        editBtn.style.display = "block"

        idField.value = tag.getAttribute('data-id')
        accountNumber.value = tag.getAttribute('data-number')
        accountName.value = tag.getAttribute('data-name')
        accountDesc.value = tag.getAttribute('data-description')
        if (accountType != null){
            accountType.value = tag.getAttribute('data-type')
        }

}

function remove(tag){
    idField = tag.getAttribute('data-id')
    deleteField.value = idField
}

function clearFields(){
        idField.value = ""
        accountNumber.value = ""
        accountName.value = ""
        accountDesc.value = ""
        if (accountType != null){
            accountType.value = ""
        }
        deleteField.value = ""
    }

if (document.querySelector(".pagination-next"))
    document.querySelector(".pagination-next").addEventListener("click", function () {
        (document.querySelector(".pagination.listjs-pagination")) ? (document.querySelector(".pagination.listjs-pagination").querySelector(".active")) ?
        document.querySelector(".pagination.listjs-pagination").querySelector(".active").nextElementSibling.children[0].click(): '': '';
    });
if (document.querySelector(".pagination-prev"))
    document.querySelector(".pagination-prev").addEventListener("click", function () {
        (document.querySelector(".pagination.listjs-pagination")) ? (document.querySelector(".pagination.listjs-pagination").querySelector(".active")) ?
        document.querySelector(".pagination.listjs-pagination").querySelector(".active").previousSibling.children[0].click(): '': '';
    });
