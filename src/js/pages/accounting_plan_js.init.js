
var checkAll = document.getElementById("checkAll");
if (checkAll) {
    checkAll.onclick = function () {
        var checkboxes = document.querySelectorAll('.form-check-all input[type="checkbox"]');
        if (checkAll.checked === true) {
            Array.from(checkboxes).forEach(function (checkbox) {
                checkbox.checked = true;
                checkbox.closest("tr").classList.add("table-active");
            });
        } else {
            Array.from(checkboxes).forEach(function (checkbox) {
                checkbox.checked = false;
                checkbox.closest("tr").classList.remove("table-active");
            });
        }
    };
}

var perPage = 8;

//Table
var options = {
    valueNames: [
        "id",
        "accounting_number",
        "accounting_name",
        "accounting_type",
        "accounting_desc",
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
// Init list
if (document.getElementById("accountingList"))
    var accountingList = new List("accountingList", options).on("updated", function (list) {
        list.matchingItems.length == 0 ?
            (document.getElementsByClassName("noresult")[0].style.display = "block") :
            (document.getElementsByClassName("noresult")[0].style.display = "none");
            (document.getElementById("edit-btn").style.display = "none");
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


isCount = new DOMParser().parseFromString(
    accountingList.items.slice(-1)[0]._values.id,
    "text/html"
);

var isValue = isCount.body.firstElementChild.innerHTML;

var idField = document.getElementById("id-field"),
    accounting_number_field = document.getElementById("accounting-number-field"),
    accounting_name_field = document.getElementById("accounting-name-field"),
    accounting_desc_field = document.getElementById("accounting-desc-field"),
    accounting_type_field = document.getElementById("accounting-type-field"),

    addBtn = document.getElementById("add-btn"),
    editBtn = document.getElementById("edit-btn"),
    removeBtns = document.getElementsByClassName("remove-item-btn"),

    editBtns = document.getElementsByClassName("edit-item-btn");


refreshCallbacks();
//filterContact("All");

function filterContact(isValue) {
    var values_status = isValue;
    accountingList.filter(function (data) {
        var statusFilter = false;
        matchData = new DOMParser().parseFromString(
            data.values().status,
            "text/html"
        );
        var status = matchData.body.firstElementChild.innerHTML;
        if (status == "All" || values_status == "All") {
            statusFilter = true;
        } else {
            statusFilter = status == values_status;
        }
        return statusFilter;
    });

    accountingList.update();
}

function updateList() {
    var values_status = document.querySelector("input[name=accounting-type-field]:checked").value;

    data = userList.filter(function (item) {
        var statusFilter = false;

        if (values_status == "All") {
            statusFilter = true;
        } else {
            statusFilter = item.values().sts == values_status;
        }
        return statusFilter;
    });
    userList.update();
}

if (document.getElementById("showModal")) {

    document.getElementById("showModal").addEventListener("show.bs.modal", function (e) {
        if (e.relatedTarget.classList.contains("edit-item-btn")) {
            document.getElementById("exampleModalLabel").innerHTML = "Modifier Compte";
            document.getElementById("showModal").querySelector(".modal-footer").style.display = "block";
            document.getElementById("add-btn") != null ? document.getElementById("add-btn").style.display = "none" : null;
            document.getElementById("edit-btn").style.display = "block";
        } else if (e.relatedTarget.classList.contains("add-btn")) {
            document.getElementById("exampleModalLabel").innerHTML = "Ajouter Compte";
            document.getElementById("showModal").querySelector(".modal-footer").style.display = "block";
            document.getElementById("edit-btn").style.display = "none";
            document.getElementById("add-btn").style.display = "block";
        } else {
            document.getElementById("exampleModalLabel").innerHTML = "Liste Compte";
            document.getElementById("showModal").querySelector(".modal-footer").style.display = "none";
        }
    });
    ischeckboxcheck();

    document.getElementById("showModal").addEventListener("hidden.bs.modal", function (evt) {
        clearFields();
    });

}


if (document.getElementById("deleteRecordModal")) {

    document.getElementById("deleteRecordModal").addEventListener("show.bs.modal", function (e) {
        if (e.relatedTarget.classList.contains("remove-item-btn")) {
            document.getElementById("delete-item").value = e.relatedTarget.dataset.id
        }
    });

}

document.querySelector("#accountingList").addEventListener("click", function () {
    refreshCallbacks();
    ischeckboxcheck();
});

var table = document.getElementById("accountingPlanTable");
// save all tr
var tr = table.getElementsByTagName("tr");
var trlist = table.querySelectorAll(".list tr");

var count = 11;
if (addBtn)
    addBtn.addEventListener("click", function (e) {
        if (
            accounting_number_field.value !== "" &&
            accounting_name_field.value !== "" &&
            accounting_desc_field.value !== ""
        ) {
            accountingList.add({
                id: '<a href="javascript:void(0);" class="fw-medium link-primary">#VZ'+count+"</a>",
                accounting_number: accounting_number_field.value,
                accounting_name: accounting_name_field.value,
                accounting_desc: accounting_desc_field.value,
                accounting_type: isStatus(accounting_type_field.value),
            });
            accountingList.sort('id', { order: "desc" });
            document.getElementById("close-modal").click();
            clearFields();
            refreshCallbacks();
            filterContact("All");
            count++;
            Swal.fire({
              position: 'center',
              icon: 'success',
              title: 'Compte ajouté avec succès!',
              showConfirmButton: false,
              timer: 2000,
              showCloseButton: true
            });
        }
    });
if (editBtn)
    editBtn.addEventListener("click", function (e) {
        document.getElementById("exampleModalLabel").innerHTML = "Modifier Compte";

        var editValues = accountingList.get({
            id: idField.value,
        });

        Array.from(editValues).forEach(function (x) {
            isid = new DOMParser().parseFromString(x._values.id, "text/html");
            var selectedid = isid.body.firstElementChild.innerHTML;
            if (selectedid == itemId) {
                x.values({
                    id: '<a href="javascript:void(0);" class="fw-medium link-primary">'+idField.value+"</a>",
                    accounting_number: accounting_number_field.value,
                    accounting_name: accounting_name_field.value,
                    accounting_desc: accounting_desc_field.value,
                    accounting_type: isStatus(accounting_type_field.value),
                });
            }
        });
        document.getElementById("close-modal").click();
        clearFields();
        Swal.fire({
            position: 'center',
            icon: 'success',
            title: 'Customer updated Successfully!',
            showConfirmButton: false,
            timer: 2000,
            showCloseButton: true
        });
    });


var accountingTypeVal = new Choices(accounting_type_field);

function isStatus(val) {
    switch (val) {
        case "encaissement":
            return (
                '<span class="badge badge-soft-success text-uppercase">' +
                val +
                "</span>"
            );
        case "decaissement":
            return (
                '<span class="badge badge-soft-danger text-uppercase">' +
                val +
                "</span>"
            );
    }
}

function ischeckboxcheck() {

    document.getElementsByName("chk_child").forEach(function (x) {

        x.addEventListener("click", function (e) {

            if (e.target.checked) {
                e.target.closest("tr").classList.add("table-active");
            } else {
                e.target.closest("tr").classList.remove("table-active");
            }
        });
    })}

function refreshCallbacks() {
    if (removeBtns)
    Array.from(removeBtns).forEach(function (btn) {
            btn.addEventListener("click", function (e) {
                e.target.closest("tr").children[1].innerText;
                itemId = e.target.closest("tr").children[1].innerText;
                var itemValues = accountingList.get({
                    id: itemId,
                });

                Array.from(itemValues).forEach(function (x) {
                    deleteid = new DOMParser().parseFromString(x._values.id, "text/html");
                    var isElem = deleteid.body.firstElementChild;
                    var isdeleteid = deleteid.body.firstElementChild.innerHTML;
                    if (isdeleteid == itemId) {
                        document.getElementById("delete-record").addEventListener("click", function () {
                            accountingList.remove("id", isElem.outerHTML);
                            document.getElementById("deleteRecordModal").click();
                        });
                    }
                });
            });
        });
    if (editBtn)
        Array.from(editBtns).forEach(function (btn) {
            btn.addEventListener("click", function (e) {
                e.target.closest("tr").children[1].innerText;
                itemId = e.target.closest("tr").children[1].innerText;

                var itemValues = accountingList.get({
                    id: itemId,
                });



                Array.from(itemValues).forEach(function (x) {
                    isid = new DOMParser().parseFromString(x._values.id, "text/html");
                    var selectedid = isid.body.firstElementChild.innerHTML;

                    if (selectedid == itemId) {
                        idField.value = selectedid;
                        accounting_number_field.value = x._values.accounting_number;
                        accounting_name_field.value = x._values.accounting_name;
                        accounting_desc_field.value = x._values.accounting_desc;

                        if (accountingTypeVal) accountingTypeVal.destroy();
                        accountingTypeVal = new Choices(accounting_type_field);
                        val = new DOMParser().parseFromString(x._values.accounting_type, "text/html");
                        var typeSelec = val.body.firstElementChild.innerHTML;
                        accountingTypeVal.setChoiceByValue(typeSelec);

                    }
                });
            });
        });
}

function clearFields() {
    accounting_number_field.value = "";
    accounting_name_field.value = "";
    accounting_desc_field.value = "";
}

function deleteMultiple() {
  ids_array = [];
  var items = document.getElementsByName('chk_child');
  Array.from(items).forEach(function (ele) {
    if (ele.checked == true) {
      var trNode = ele.parentNode.parentNode.parentNode;
      var id = trNode.querySelector('.id a').innerHTML;
      ids_array.push(id);
    }
  });
  if (typeof ids_array !== 'undefined' && ids_array.length > 0) {
    if (confirm('Êtes-vous sûr de vouloir supprimer ceci?')) {
        Array.from(ids_array).forEach(function (id) {
        accountingList.remove("id", `<a href="javascript:void(0);" class="fw-medium link-primary">${id}</a>`);
      });
      document.getElementById('checkAll').checked = false;
    } else {
      return false;
    }
  } else {
    Swal.fire({
      title: 'Veuillez cocher au moins une case',
      confirmButtonClass: 'btn btn-info',
      buttonsStyling: false,
      showCloseButton: true
    });
  }
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

// data- attribute example
var attroptions = {
    valueNames: [
        'name',
        'born',
        {
            data: ['id']
        },
        {
            attr: 'src',
            name: 'image'
        },
        {
            attr: 'href',
            name: 'link'
        },
        {
            attr: 'data-timestamp',
            name: 'timestamp'
        }
    ]
};


// Existing List
var existOptionsList = {
    valueNames: ['contact-name', 'contact-message']
};
var existList = new List('contact-existing-list', existOptionsList);

// Fuzzy Search list
var fuzzySearchList = new List('fuzzysearch-list', {
    valueNames: ['name']
});

// pagination list
var paginationList = new List('pagination-list', {
    valueNames: ['pagi-list'],
    page: 3,
    pagination: true
});