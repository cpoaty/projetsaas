// Ajoute des classes Bootstrap aux champs du formulaire
document.addEventListener('DOMContentLoaded', function() {
    const formControls = document.querySelectorAll('input, select, textarea');
    formControls.forEach(function(element) {
        if (element.type !== 'checkbox') {
            element.classList.add('form-control');
        } else {
            element.classList.add('form-check-input');
        }
    });
});