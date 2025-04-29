# Documentation Technique du Projet ComptaApp

## Introduction

ComptaApp est une application de comptabilité développée avec le framework Django, conçue avec une architecture modulaire pour une maintenance facilitée et une évolutivité optimale. Cette documentation présente la structure du projet et les fonctionnalités implémentées à ce jour.

## Structure Modulaire

L'application est organisée selon une architecture modulaire qui sépare clairement les préoccupations :

```
compta_project/                  # Dossier racine du projet
│
├── compta_project/              # Configuration du projet Django
│   ├── __init__.py
│   ├── settings/                # Paramètres divisés par environnement
│   │   ├── __init__.py
│   │   ├── base.py             # Configuration commune
│   │   ├── development.py      # Configuration développement
│   │   └── production.py       # Configuration production
│   ├── urls.py                  # URLs principales
│   ├── asgi.py
│   └── wsgi.py
│
├── apps/                        # Dossier contenant toutes les applications
│   ├── __init__.py
│   │
│   ├── core/                    # Fonctionnalités partagées
│   │
│   ├── accounts/                # Application des comptes
│   │   ├── __init__.py
│   │   ├── admin/              # Administration modularisée
│   │   │   ├── __init__.py
│   │   │   ├── account_admin.py
│   │   │   ├── account_class_admin.py
│   │   │   ├── account_group_admin.py
│   │   │   └── account_type_admin.py
│   │   ├── apps.py
│   │   ├── forms/              # Formulaires modularisés
│   │   │   ├── __init__.py
│   │   │   └── account_forms.py
│   │   ├── models/             # Modèles modularisés
│   │   │   ├── __init__.py
│   │   │   ├── account.py
│   │   │   ├── account_class.py
│   │   │   ├── account_group.py
│   │   │   └── account_type.py
│   │   ├── services/           # Logique métier
│   │   │   └── __init__.py
│   │   ├── tests/              # Tests unitaires
│   │   │   ├── __init__.py
│   │   │   ├── models/
│   │   │   └── views/
│   │   ├── urls/               # URLs modularisées
│   │   │   ├── __init__.py
│   │   │   └── account_urls.py
│   │   └── views/              # Vues modularisées
│   │       ├── __init__.py
│   │       └── account_views.py
│   │
│   ├── transactions/           # Application des transactions (à développer)
│   │
│   └── reporting/              # Application des rapports (à développer)
│
├── static/                      # Fichiers statiques
│   ├── accounts/
│   │   ├── css/
│   │   │   └── accounts.css
│   │   └── js/
│   │       └── accounts.js
│   └── ...
│
├── templates/                   # Templates HTML
│   ├── base.html
│   ├── home.html
│   ├── admin/                   # Templates personnalisés pour l'administration
│   │   └── accounts/
│   │       └── accountclass/
│   │           └── change_form.html  # Template personnalisé pour les classes de compte
│   └── accounts/
│       ├── account_list.html
│       └── account_form.html
│
├── manage.py
└── requirements/                # Dépendances par environnement
    ├── base.txt
    ├── development.txt
    └── production.txt
```

## Modules et Fonctionnalités

### Module Accounts (Comptes)

#### Modèles

1. **AccountClass** - Classes de comptes (niveau 1 du plan comptable OHADA)
   - Attributs: number (PK), name, description, position_bilan, actif, date_creation
   - Exemple: 1 - Comptes de ressources durables
   - **Nouveauté**: Implémentation automatique des règles OHADA pour la position dans le bilan
   - **Nouveauté**: Génération automatique des noms et descriptions selon le plan comptable OHADA

2. **AccountGroup** - Groupes de comptes (niveau 2 du plan comptable)
   - Attributs: account_class (FK), number, name, description
   - Exemple: 10 - Capital et réserves

3. **AccountType** - Types de comptes
   - Attributs: code (PK), name
   - Exemples: Actif, Passif, Charge, Produit, Capitaux propres

4. **Account** - Comptes comptables individuels
   - Attributs: account_group (FK), number, name, description, account_type (FK), is_active
   - Exemple: 10100 - Capital social

#### Vues

1. **AccountListView** - Affiche la liste hiérarchique des comptes
   - Template: account_list.html
   - URL: /accounts/

2. **AccountCreateView** - Formulaire de création de compte
   - Template: account_form.html
   - URL: /accounts/create/

3. **AccountDetailView** - Détails d'un compte spécifique
   - Template: account_detail.html (à créer)
   - URL: /accounts/<pk>/

4. **AccountUpdateView** - Modifier un compte existant
   - Template: account_form.html
   - URL: /accounts/<pk>/update/

#### Administration

Module d'administration modulaire avec des classes personnalisées pour chaque modèle :

- **AccountClassAdmin** (Mise à jour récente)
  - Interface améliorée avec prévisualisation en temps réel des informations OHADA
  - Seul le numéro de classe est modifiable, tout le reste est généré automatiquement
  - Implémentation d'une API JavaScript pour la mise à jour dynamique des informations
  - Template personnalisé pour injecter le JavaScript nécessaire
  - Affichage des libellés OHADA officiels dans la liste des classes

- AccountGroupAdmin
- AccountTypeAdmin
- AccountAdmin

### Configuration du Projet

#### Système de paramètres multi-environnements

La configuration est divisée en trois fichiers:
- `base.py`: Paramètres communs à tous les environnements
- `development.py`: Paramètres spécifiques au développement
- `production.py`: Paramètres optimisés pour la production

#### Chemin Python modifié

Le dossier `apps/` est ajouté au chemin Python pour permettre des imports plus courts et plus lisibles:

```python
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR / 'apps'))
```

## Interfaces Utilisateur

### Template de base

Un template de base (`base.html`) qui fournit:
- Barre de navigation
- Structure HTML commune
- Chargement des CSS et JavaScript

### Liste des comptes

Interface utilisateur pour consulter la hiérarchie du plan comptable:
- Affichage arborescent des classes, groupes et comptes
- Fonctionnalité de recherche en JavaScript
- Interface expansible/réductible

### Formulaire de compte

Formulaire de création/modification de compte avec:
- Sélection du groupe de compte
- Sélection du type de compte
- Champs pour numéro, nom et description
- Option pour activer/désactiver un compte

### Interface d'administration personnalisée

**Nouveauté**: Interface d'administration améliorée pour les classes de compte :
- Prévisualisation en temps réel du nom, de la description et de la position dans le bilan
- Formulaire simplifié où seul le numéro est modifiable
- Affichage des labels sans retour à la ligne (nowrap)
- Injection de JavaScript via un template personnalisé
- API pour récupérer dynamiquement les informations des classes de compte

## Avancées Techniques

### Architecture Modulaire

L'application utilise une architecture modulaire qui:
- Sépare les modèles, vues, formulaires et logique métier
- Facilite la maintenance et l'extension
- Permet un développement parallèle des différentes parties

### Plan Comptable OHADA

**Nouveauté**: Implémentation complète du plan comptable OHADA :
- Dictionnaires contenant les noms et descriptions normalisés des classes de compte
- Règles automatiques pour déterminer la position dans le bilan (Actif, Passif, Charges, Produits)
- Validation des numéros de compte selon les standards OHADA

### Interaction JavaScript/Django

**Nouveauté**: Utilisation avancée de JavaScript dans l'interface d'administration :
- API Django exposée via URL personnalisée pour récupérer les informations des comptes
- Génération dynamique d'éléments d'interface utilisateur
- Mise à jour en temps réel des champs de prévisualisation

### Tests Unitaires

Structure de tests mise en place (à compléter):
- Tests pour les modèles
- Tests pour les vues

### Compatibilité avec Django Admin

L'application s'intègre parfaitement avec l'interface d'administration Django tout en maintenant sa structure modulaire et en ajoutant des fonctionnalités personnalisées.

## Prochaines Étapes

1. Compléter le module des groupes de comptes:
   - Améliorer l'interface utilisateur pour la création et la modification des groupes de comptes
   - Implémentation des règles OHADA pour les groupes de comptes

2. Compléter le module des comptes:
   - Développer l'interface utilisateur pour la gestion des comptes individuels
   - Ajouter la fonction d'importation de plan comptable
   - Ajouter des vues pour la suppression des comptes

3. Développer le module des transactions:
   - Modèles pour les écritures comptables
   - Interface d'enregistrement des transactions

4. Développer le module de reporting:
   - Génération de rapports comptables (bilan, compte de résultat)
   - Exports au format PDF, Excel

5. Améliorer les tests:
   - Atteindre une couverture de code significative
   - Ajouter des tests d'intégration

## Conclusion

Le projet ComptaApp dispose désormais d'une architecture modulaire solide et évolutive. Le module des classes de comptes est pleinement fonctionnel avec une interface utilisateur intuitive qui respecte les règles du plan comptable OHADA. Cette base solide facilitera le développement des modules de groupes de comptes, comptes individuels, transactions et reporting.

# Ajouter la documentation au dépôt Git
git add docs/documentation_technique.md

# Créer un commit
git commit -m "Ajout de la documentation technique du projet"

# Pousser vers GitHub
git push origin main