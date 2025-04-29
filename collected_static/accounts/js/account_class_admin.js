// Ce fichier doit être placé dans static/accounts/js/account_class_admin.js
// Il met à jour dynamiquement les champs de prévisualisation lorsque l'utilisateur change le numéro de classe

document.addEventListener('DOMContentLoaded', function() {
    // Dictionnaires des noms et descriptions standard des classes de comptes OHADA
    const NOMS_CLASSES = {
        '1': "Comptes de ressources durables",
        '2': "Comptes d'actif immobilisé",
        '3': "Comptes de stocks",
        '4': "Comptes de tiers",
        '5': "Comptes de trésorerie",
        '6': "Comptes de charges des activités ordinaires",
        '7': "Comptes de produits des activités ordinaires",
        '8': "Comptes des autres charges et des autres produits"
    };

    const DESCRIPTIONS_CLASSES = {
        '1': "Regroupe les comptes de capitaux propres, provisions, emprunts et dettes financières diverses.",
        '2': "Regroupe les comptes d'immobilisations incorporelles, corporelles et financières.",
        '3': "Regroupe les comptes de stocks de marchandises, matières premières et autres approvisionnements.",
        '4': "Regroupe les comptes de fournisseurs, clients et autres débiteurs ou créditeurs.",
        '5': "Regroupe les comptes de banque, établissements financiers, caisse et autres valeurs.",
        '6': "Regroupe les comptes d'achats, services extérieurs, impôts et taxes, charges de personnel.",
        '7': "Regroupe les comptes de ventes, subventions d'exploitation et autres produits.",
        '8': "Regroupe les comptes de charges et produits hors activités ordinaires."
    };

    // Fonction pour mettre à jour les champs de prévisualisation en fonction du numéro sélectionné
    function updatePreviewFields() {
        const numberField = document.getElementById('id_number');
        const previewNameField = document.getElementById('id_preview_name');
        const previewDescriptionField = document.getElementById('id_preview_description');
        
        if (numberField && previewNameField && previewDescriptionField) {
            const selectedValue = numberField.value;
            
            // Mettre à jour le nom de la classe
            if (NOMS_CLASSES[selectedValue]) {
                previewNameField.value = NOMS_CLASSES[selectedValue];
            } else {
                previewNameField.value = '';
            }
            
            // Mettre à jour la description de la classe
            if (DESCRIPTIONS_CLASSES[selectedValue]) {
                previewDescriptionField.value = DESCRIPTIONS_CLASSES[selectedValue];
            } else {
                previewDescriptionField.value = '';
            }
            
            // Déterminer automatiquement la position dans le bilan
            const positionField = document.getElementById('id_position_bilan');
            if (positionField) {
                const numberValue = parseInt(selectedValue);
                if (numberValue <= 2) {
                    positionField.value = "Actif";
                } else if (numberValue <= 5) {
                    positionField.value = "Passif";
                } else if (numberValue === 6 || numberValue === 8) {
                    positionField.value = "Charges";
                } else if (numberValue === 7) {
                    positionField.value = "Produits";
                }
            }
        }
    }

    // Ajouter un écouteur d'événement au champ de numéro
    const numberField = document.getElementById('id_number');
    if (numberField) {
        numberField.addEventListener('change', updatePreviewFields);
        
        // Mettre à jour les champs dès le chargement de la page
        updatePreviewFields();
    }
});