document.addEventListener('DOMContentLoaded', function() {
    // Éléments du DOM
    const classField = document.getElementById('id_account_class');
    const numberField = document.getElementById('id_number');
    
    // Si les éléments n'existent pas, sortir
    if (!classField || !numberField) return;
    
    console.log('Script de gestion des groupes de comptes chargé');
    
    // Fonction pour mettre à jour les options de numéro
    function updateNumberOptions(classId) {
        if (!classId) return;
        
        console.log('Mise à jour des options pour la classe:', classId);
        
        // Faire un appel AJAX pour récupérer les options
        fetch(`/admin/accounts/accountgroup/get_group_options/${classId}/`)
            .then(response => response.json())
            .then(data => {
                // Vider les options actuelles
                numberField.innerHTML = '<option value="">---------</option>';
                
                // Ajouter les nouvelles options
                if (data.options) {
                    data.options.forEach(option => {
                        const opt = document.createElement('option');
                        opt.value = option.value;
                        opt.textContent = option.label;
                        numberField.appendChild(opt);
                    });
                    console.log('Options mises à jour:', data.options.length, 'options');
                }
            })
            .catch(error => console.error('Erreur:', error));
    }
    
    // Fonction pour mettre à jour la prévisualisation
    function updatePreview(number) {
        // Vérifier si les éléments de prévisualisation existent déjà
        let nameDiv = document.getElementById('preview_name');
        let descDiv = document.getElementById('preview_description');
        
        // Si les éléments n'existent pas, les créer
        if (!nameDiv || !descDiv) {
            const formRow = numberField.closest('.form-row');
            if (!formRow) return;
            
            console.log('Création des champs de prévisualisation');
            
            // Créer les éléments
            const nameRow = document.createElement('div');
            nameRow.className = 'form-row field-preview_name';
            nameRow.style.marginTop = '20px';
            nameRow.innerHTML = `
                <div>
                    <label style="white-space: nowrap; font-weight: bold; color: #2271b1;">Libellé (généré automatiquement) :</label>
                    <div class="readonly" id="preview_name" style="padding: 10px; background: #f5f9ff; border: 1px solid #ddd; min-height: 20px; margin-top: 5px;"></div>
                </div>
            `;
            
            const descRow = document.createElement('div');
            descRow.className = 'form-row field-preview_description';
            descRow.style.marginTop = '20px';
            descRow.innerHTML = `
                <div>
                    <label style="white-space: nowrap; font-weight: bold; color: #2271b1;">Description (générée automatiquement) :</label>
                    <div class="readonly" id="preview_description" style="padding: 10px; background: #f5f9ff; border: 1px solid #ddd; min-height: 100px; margin-top: 5px;"></div>
                </div>
            `;
            
            // Insérer les éléments après le champ de numéro
            const parent = formRow.parentNode;
            parent.insertBefore(nameRow, formRow.nextSibling);
            parent.insertBefore(descRow, nameRow.nextSibling);
            
            // Récupérer les références
            nameDiv = document.getElementById('preview_name');
            descDiv = document.getElementById('preview_description');
        }
        
        // Si number n'est pas défini, vider les champs
        if (!number) {
            nameDiv.textContent = '';
            descDiv.textContent = '';
            return;
        }
        
        console.log('Mise à jour de la prévisualisation pour le numéro:', number);
        
        // Appeler l'API pour récupérer les informations
        fetch(`/admin/accounts/accountgroup/get_group_info/${number}/`)
            .then(response => response.json())
            .then(data => {
                nameDiv.textContent = data.name || '';
                descDiv.textContent = data.description || '';
                console.log('Prévisualisation mise à jour avec:', data.name);
            })
            .catch(error => console.error('Erreur:', error));
    }
    
    // Ajouter les écouteurs d'événements
    classField.addEventListener('change', function() {
        console.log('Classe changée:', this.value);
        updateNumberOptions(this.value);
        // Réinitialiser la prévisualisation
        updatePreview(null);
    });
    
    numberField.addEventListener('change', function() {
        console.log('Numéro changé:', this.value);
        updatePreview(this.value);
    });
    
    // Initialisation
    console.log('Initialisation - Classe:', classField.value, 'Numéro:', numberField.value);
    if (classField.value) {
        updateNumberOptions(classField.value);
    }
    
    if (numberField.value) {
        updatePreview(numberField.value);
    }
});