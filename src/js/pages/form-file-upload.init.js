
/*
// Dropzone
var dropzonePreviewNode = document.querySelector("#dropzone-preview-list");
dropzonePreviewNode.id = "";
if(dropzonePreviewNode){
    var previewTemplate = dropzonePreviewNode.parentNode.innerHTML;
    dropzonePreviewNode.parentNode.removeChild(dropzonePreviewNode);
    var dropzone = new Dropzone(".dropzone", {
        previewTemplate: previewTemplate,
        previewsContainer: "#dropzone-preview",
    });
}
*/
// FilePond
FilePond.registerPlugin(
    // encodes the file as base64 data
    FilePondPluginFileEncode,
    // validates the size of the file
    FilePondPluginFileValidateSize,
    // corrects mobile image orientation
    FilePondPluginImageExifOrientation,
    // previews dropped images
    FilePondPluginImagePreview
);

let inputElement = document.querySelector('input[type="file"]');
let formElement = document.getElementById('budget-form')
const url = formElement.getAttribute('data-url')
const csrf_token = document.getElementsByName('csrfmiddlewaretoken')[1]

if(inputElement){

  FilePond.create(inputElement, {
        server: {
              url: url,
              headers: {
                  'X-CSRFToken': csrf_token.value
              }
        },
        labelIdle: 'Faites glisser et déposez votre fichier ou <span class="filepond--label-action">Parcourez</span>',
        dropValidation: true,
        storeAsFile: true,
        required: true,
        acceptedFileTypes: ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, text/csv'],
        labelFileLoading: 'chargement',
        labelFileProcessing: 'Envoi en cours',
        labelFileProcessingComplete: 'Envoi terminé',
        labelFileProcessingAborted: 'Envoi annulé',
        labelButtonProcessItem: 'Charge',
        labelFileWaitingForSize: 'En attente de la taille',
        labelFileSizeNotAvailable: 'Taille non disponible',
        labelMinFileSizeExceeded: 'Le fichier est trop petit',
        labelMaxFileSizeExceeded: 'Le fichier est trop grand',
        labelMinFileSize: 'La taille minimale du fichier est {filesize}',
        labelMaxFileSize: 'La taille maximale du fichier est {filesize}',
        labelMaxTotalFileSizeExceeded: 'Taille totale maximale dépassée',
        labelMaxTotalFileSize: 'La taille totale maximale du fichier est de {filesize}',
        labelTapToCancel: 'Tapez pour annuler',
        labelTapToRetry: 'Tapez pour réesayer',
        labelTapToUndo: 'Tapez pour revenir en arrière',
        labelButtonRemoveItem: 'Retirer',
        labelButtonAbortItemLoad: 'Annuler',
        labelButtonRetryItemLoad: 'Réessayez',
        labelButtonAbortItemProcessing: 'Annuler',
        labelButtonUndoItemProcessing: 'Revenir',
        labelButtonRetryItemProcessing: 'Réessayez',
        labelFileRemoveError: 'Erreur lors du retrait',
        labelFileProcessingRevertError: "Erreur lors de l'inversion",
        labelFileProcessingError: 'Erreur lors du chargement',
        labelFileLoadError: 'Erreur lors du chargement',
        labelInvalidField: 'Le champ contient des fichiers invalides',
        labelFileTypeNotAllowed: 'Type de fichier invalide'
    });
}