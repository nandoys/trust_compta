//buttons exmples
document.addEventListener('DOMContentLoaded', function () {
  let table = new DataTable('#treasury_table', {
        dom: 'Bfrtip',
        buttons: [
            'csv', 'excel', 'print'
        ],
        fixedHeader: true,
        responsive: true,
        select: true,
        order: false,
        language: {
            "decimal":        "",
            "emptyTable":     "aucune donnée disponible",
            "info":           "Affichage _START_ à _END_ of _TOTAL_ enregistrement(s)",
            "infoEmpty":      "Affichage de 0 à 0 sur 0 entrées",
            "infoFiltered":   "(filtré de _MAX_ enregistrement(s) total)",
            "infoPostFix":    "",
            "thousands":      ",",
            "lengthMenu":     "Affiche _MENU_ enregistrements",
            "loadingRecords": "Chargement...",
            "processing":     "",
            "search":         "Recherche:",
            "zeroRecords":    "Aucun enregistrements correspondants trouvés",
            "paginate": {
                "first":      "Premier",
                "last":       "Dernier",
                "next":       "Suivant",
                "previous":   "Précédent"
            },
            "aria": {
                "sortAscending":  ": activer pour trier les colonnes par ordre croissant",
                "sortDescending": ": activer pour trier les colonnes par ordre décroissant"
            }
        },
        "oTableTools": {
            "aButtons": [
                {
                    "sExtends": "print",
                    "sButtonText": "Imprimer",
                    "mColumns": [ 0, 1, 2 ]
                },
            ]
        }
    });
});