document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM chargé, début du script");
    
    // Récupérer le champ code qui devrait exister
    var codeField = document.getElementById('id_code');
    
    if (!codeField) {
        console.error("Impossible de trouver le champ code");
        return;
    }
    
    // Correspondance entre codes et valeurs
    var typeNames = {
        'AC': 'Actif',
        'PA': 'Passif',
        'CH': 'Charge',
        'PR': 'Produit',
        'CP': 'Capitaux propres'
    };
    
    var typeDescriptions = {
        'AC': "Éléments qui représentent une valeur économique positive pour l'entreprise",
        'PA': "Dettes et obligations financières de l'entreprise",
        'CH': "Dépenses encourues pour générer des revenus",
        'PR': "Produits générés par l'activité de l'entreprise",
        'CP': "Valeur résiduelle des actifs après déduction des passifs"
    };
    
    // Fonction pour trouver les champs par leur label
    function findFieldByLabel(labelText) {
        var labels = document.querySelectorAll('label');
        for (var i = 0; i < labels.length; i++) {
            if (labels[i].textContent.trim().includes(labelText)) {
                // Trouver le champ associé à ce label
                var fieldContainer = labels[i].closest('.form-row, .fieldBox');
                if (fieldContainer) {
                    var field = fieldContainer.querySelector('input, textarea, select, .readonly');
                    if (field) return field;
                }
            }
        }
        return null;
    }
    
    // Fonction pour mettre à jour les valeurs affichées
    function updateValues() {
        var code = codeField.value;
        var name = typeNames[code] || '';
        var description = typeDescriptions[code] || '';
        
        console.log("Code:", code, "Nom:", name, "Description:", description);
        
        // Trouver les champs par leur label
        var nameField = findFieldByLabel('Nom');
        var descriptionField = findFieldByLabel('Description');
        
        console.log("Champ nom trouvé:", nameField ? "Oui" : "Non");
        console.log("Champ description trouvé:", descriptionField ? "Oui" : "Non");
        
        // Mettre à jour les valeurs si les champs existent
        if (nameField) {
            if (nameField.tagName === 'INPUT' || nameField.tagName === 'TEXTAREA') {
                nameField.value = name;
            } else {
                nameField.textContent = name;
            }
        }
        
        if (descriptionField) {
            if (descriptionField.tagName === 'INPUT' || descriptionField.tagName === 'TEXTAREA') {
                descriptionField.value = description;
            } else {
                descriptionField.textContent = description;
            }
        }
        
        return { nameField, descriptionField };
    }
    
    // Ajouter l'événement change au champ code
    codeField.addEventListener('change', function() {
        updateValues();
    });
    
    // Initialiser au chargement
    updateValues();
    
    // Supprimer les doublons s'ils existent
    setTimeout(function() {
        var namePreviewContainer = document.getElementById('name_preview_container');
        var descPreviewContainer = document.getElementById('description_preview_container');
        
        if (namePreviewContainer) namePreviewContainer.remove();
        if (descPreviewContainer) descPreviewContainer.remove();
    }, 500);
});