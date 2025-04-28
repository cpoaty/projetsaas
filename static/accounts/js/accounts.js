document.addEventListener('DOMContentLoaded', function() {
    // Gestion des expansions/réductions des classes et groupes
    document.querySelectorAll('.class-header').forEach(function(header) {
        header.addEventListener('click', function() {
            const classId = this.getAttribute('data-class-id');
            const groupsContainer = document.getElementById(`class-${classId}-groups`);
            const expandIcon = this.querySelector('.expand-icon');
            
            if (groupsContainer.style.display === 'none') {
                groupsContainer.style.display = 'block';
                expandIcon.textContent = '-';
            } else {
                groupsContainer.style.display = 'none';
                expandIcon.textContent = '+';
            }
        });
    });
    
    document.querySelectorAll('.group-header').forEach(function(header) {
        header.addEventListener('click', function() {
            const groupId = this.getAttribute('data-group-id');
            const accountsContainer = document.getElementById(`group-${groupId}-accounts`);
            const expandIcon = this.querySelector('.expand-icon');
            
            if (accountsContainer.style.display === 'none') {
                accountsContainer.style.display = 'block';
                expandIcon.textContent = '-';
            } else {
                accountsContainer.style.display = 'none';
                expandIcon.textContent = '+';
            }
        });
    });
    
    // Fonction de recherche
    const searchInput = document.getElementById('account-search');
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        
        // Masquer tous les conteneurs d'abord
        document.querySelectorAll('.account-groups, .accounts').forEach(function(container) {
            container.style.display = 'none';
        });
        
        document.querySelectorAll('.expand-icon').forEach(function(icon) {
            icon.textContent = '+';
        });
        
        if (searchTerm.length > 0) {
            // Recherche dans les comptes
            document.querySelectorAll('.account-item').forEach(function(item) {
                const accountText = item.textContent.toLowerCase();
                
                if (accountText.includes(searchTerm)) {
                    // Montrer ce compte et ses parents
                    item.style.display = 'block';
                    const accountsContainer = item.closest('.accounts');
                    accountsContainer.style.display = 'block';
                    
                    const groupHeader = accountsContainer.previousElementSibling;
                    groupHeader.querySelector('.expand-icon').textContent = '-';
                    
                    const groupContainer = groupHeader.closest('.account-group');
                    const groupsContainer = groupContainer.closest('.account-groups');
                    groupsContainer.style.display = 'block';
                    
                    const classHeader = groupsContainer.previousElementSibling;
                    classHeader.querySelector('.expand-icon').textContent = '-';
                } else {
                    item.style.display = 'none';
                }
            });
        } else {
            // Réinitialiser l'affichage
            document.querySelectorAll('.account-item').forEach(function(item) {
                item.style.display = 'block';
            });
        }
    });
});