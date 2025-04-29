from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from .account_class import AccountClass

class AccountGroup(models.Model):
    """
    Groupe de comptes (niveau 2 du plan comptable OHADA).
    Exemple: 10 - Capital et réserves, 11 - Report à nouveau, etc.
    Chaque groupe appartient à une classe de compte (1-8).
    """
    # Dictionnaire des noms de groupes de comptes par classe selon OHADA
    NOMS_GROUPES = {
        # Classe 1: Comptes de ressources durables
        10: "Capital",
        11: "Réserves",
        12: "Report à nouveau",
        13: "Résultat net de l'exercice",
        14: "Subventions d'investissement",
        15: "Provisions réglementées et fonds assimilés",
        16: "Emprunts et dettes financières",
        17: "Dettes de crédit-bail et contrats assimilés",
        18: "Dettes liées à des participations et comptes de liaison",
        19: "Provisions financières pour risques et charges",
        
        # Classe 2: Comptes d'actif immobilisé
        20: "Charges immobilisées",
        21: "Immobilisations incorporelles",
        22: "Terrains",
        23: "Bâtiments, installations techniques et agencements",
        24: "Matériel",
        25: "Avances et acomptes versés sur immobilisations",
        26: "Titres de participation",
        27: "Autres immobilisations financières",
        28: "Amortissements",
        29: "Provisions pour dépréciation",
        
        # Classe 3: Comptes de stocks
        30: "Marchandises",
        31: "Matières premières et fournitures liées",
        32: "Autres approvisionnements",
        33: "En-cours",
        34: "Produits fabriqués",
        35: "Stocks de produits ou services",
        36: "Stocks provenant d'immobilisations",
        37: "Stocks en cours de route, en consignation ou en dépôt",
        38: "Marchandises hors activités ordinaires",
        39: "Dépréciations des stocks",
        
        # Classe 4: Comptes de tiers
        40: "Fournisseurs et comptes rattachés",
        41: "Clients et comptes rattachés",
        42: "Personnel",
        43: "Organismes sociaux",
        44: "État et collectivités publiques",
        45: "Organismes internationaux",
        46: "Associés et groupe",
        47: "Débiteurs et créditeurs divers",
        48: "Créances et dettes hors activités ordinaires",
        49: "Dépréciations et provisions pour risques",
        
        # Classe 5: Comptes de trésorerie
        50: "Titres de placement",
        51: "Valeurs à encaisser",
        52: "Banques",
        53: "Établissements financiers et assimilés",
        54: "Instruments de trésorerie",
        55: "Caisse",
        56: "Virements de fonds",
        57: "Autres trésoreries",
        58: "Régies d'avances et accréditifs",
        59: "Dépréciations et provisions pour risques financiers",
        
        # Classe 6: Comptes de charges des activités ordinaires
        60: "Achats et variations de stocks",
        61: "Transports",
        62: "Services extérieurs A",
        63: "Services extérieurs B",
        64: "Impôts et taxes",
        65: "Autres charges",
        66: "Charges de personnel",
        67: "Frais financiers et charges assimilées",
        68: "Dotations aux amortissements",
        69: "Dotations aux provisions",
        
        # Classe 7: Comptes de produits des activités ordinaires
        70: "Ventes",
        71: "Variations de stocks de produits et encours",
        72: "Production immobilisée",
        73: "Variations des stocks de produits fabriqués",
        74: "Subventions d'exploitation",
        75: "Autres produits",
        76: "Transferts de charges",
        77: "Revenus financiers et assimilés",
        78: "Transferts de frais",
        79: "Reprises de provisions",
        
        # Classe 8: Comptes des autres charges et des autres produits
        80: "Résultat des activités ordinaires",
        81: "Charges hors activités ordinaires",
        82: "Produits hors activités ordinaires",
        83: "Charges de l'exercice imputables aux exercices antérieurs",
        84: "Produits imputés aux exercices antérieurs",
        85: "Dotations hors activités ordinaires",
        86: "Reprises hors activités ordinaires",
        87: "Participation des travailleurs",
        88: "Subventions d'équilibre",
        89: "Impôts sur le résultat"
    }
    
    # Dictionnaire des descriptions des groupes de comptes
    DESCRIPTIONS_GROUPES = {
        # Classe 1
        10: "Comprend le capital social, le capital personnel, les dotations et le capital souscrit non appelé.",
        11: "Comprend les réserves légales, statutaires, contractuelles et les autres réserves.",
        12: "Comprend le report à nouveau bénéficiaire ou déficitaire.",
        13: "Enregistre le résultat net de l'exercice en attente d'affectation.",
        14: "Enregistre les subventions d'investissement reçues pour financer des biens durables.",
        15: "Comprend les provisions réglementées et les fonds assimilés.",
        16: "Comprend les emprunts obligataires, avances reçues et dettes financières diverses.",
        17: "Enregistre les dettes liées au crédit-bail et contrats assimilés.",
        18: "Comprend les dettes liées à des participations et comptes de liaison des établissements.",
        19: "Enregistre les provisions pour risques et charges à caractère financier.",
        
        # Classe 2
        20: "Enregistre les frais d'établissement, les charges à répartir et primes de remboursement des obligations.",
        21: "Comprend les brevets, licences, logiciels, fonds commercial et autres droits incorporels.",
        22: "Enregistre les terrains agricoles, bâtis, nus, de carrière, etc.",
        23: "Comprend les constructions, installations, agencements et aménagements.",
        24: "Comprend le matériel de transport, bureautique, informatique et autres équipements.",
        25: "Enregistre les avances et acomptes versés sur commandes d'immobilisations.",
        26: "Enregistre les titres de participation dans d'autres entités.",
        27: "Comprend les prêts, dépôts et cautionnements versés, et autres créances immobilisées.",
        28: "Enregistre les amortissements des immobilisations.",
        29: "Enregistre les provisions pour dépréciation des immobilisations.",
        
        # Classe 3
        30: "Enregistre les marchandises achetées pour être revendues en l'état.",
        31: "Comprend les matières premières et fournitures liées à la production.",
        32: "Comprend les matières consommables, fournitures et autres approvisionnements.",
        33: "Enregistre les biens et services en cours de production.",
        34: "Enregistre les produits intermédiaires et produits finis.",
        35: "Enregistre les stocks de produits ou services.",
        36: "Enregistre les stocks provenant d'immobilisations démontées ou mises au rebut.",
        37: "Comprend les stocks en cours de route, en consignation ou en dépôt.",
        38: "Enregistre les marchandises hors activités ordinaires.",
        39: "Enregistre les dépréciations des stocks.",
        
        # Classe 4
        40: "Comprend les dettes envers les fournisseurs et comptes rattachés.",
        41: "Comprend les créances sur les clients et comptes rattachés.",
        42: "Comprend les dettes et créances envers le personnel.",
        43: "Comprend les dettes et créances envers les organismes sociaux.",
        44: "Comprend les dettes et créances envers l'État et les collectivités publiques.",
        45: "Comprend les opérations avec les organismes internationaux.",
        46: "Comprend les opérations avec les associés et le groupe.",
        47: "Comprend les créances et dettes diverses non liées à l'exploitation courante.",
        48: "Enregistre les créances et dettes hors activités ordinaires.",
        49: "Enregistre les dépréciations des comptes de tiers et provisions pour risques.",
        
        # Classe 5
        50: "Comprend les actions, obligations et valeurs assimilées détenues à court terme.",
        51: "Comprend les effets et chèques à encaisser.",
        52: "Enregistre les disponibilités en banque.",
        53: "Enregistre les disponibilités auprès des établissements financiers.",
        54: "Comprend les options de taux, options de change et autres instruments de trésorerie.",
        55: "Enregistre les espèces disponibles en caisse.",
        56: "Enregistre les transferts de fonds entre comptes de trésorerie.",
        57: "Comprend les autres instruments et valeurs de trésorerie.",
        58: "Enregistre les régies d'avances et accréditifs.",
        59: "Enregistre les dépréciations des valeurs de placement et provisions pour risques financiers.",
        
        # Classe 6
        60: "Comprend les achats de marchandises, matières premières et variations de stocks.",
        61: "Comprend les transports sur achats, sur ventes et autres transports.",
        62: "Comprend les loyers, entretiens, primes d'assurance et documentations.",
        63: "Comprend les rémunérations d'intermédiaires, publicité et relations publiques.",
        64: "Comprend les impôts, taxes et versements assimilés.",
        65: "Comprend les pertes sur créances irrécouvrables et autres charges diverses.",
        66: "Comprend les rémunérations du personnel et charges sociales.",
        67: "Comprend les intérêts, escomptes et autres frais financiers.",
        68: "Comprend les dotations aux amortissements.",
        69: "Comprend les dotations aux provisions.",
        
        # Classe 7
        70: "Comprend les ventes de marchandises, produits et services.",
        71: "Enregistre les variations de stocks de produits et en-cours.",
        72: "Enregistre les immobilisations créées par l'entreprise pour elle-même.",
        73: "Enregistre les variations des stocks de produits fabriqués.",
        74: "Comprend les subventions d'exploitation reçues.",
        75: "Comprend les produits divers de gestion courante.",
        76: "Enregistre les transferts de charges d'exploitation.",
        77: "Comprend les revenus des titres, prêts, différences positives de change.",
        78: "Enregistre les transferts de frais financiers.",
        79: "Comprend les reprises de provisions.",
        
        # Classe 8
        80: "Détermine le résultat des activités ordinaires.",
        81: "Comprend les charges exceptionnelles, non récurrentes.",
        82: "Comprend les produits exceptionnels, non récurrents.",
        83: "Enregistre les charges des exercices antérieurs constatées dans l'exercice courant.",
        84: "Enregistre les produits des exercices antérieurs constatés dans l'exercice courant.",
        85: "Comprend les dotations aux provisions hors activités ordinaires.",
        86: "Comprend les reprises de provisions hors activités ordinaires.",
        87: "Enregistre la participation des travailleurs aux bénéfices.",
        88: "Enregistre les subventions d'équilibre reçues.",
        89: "Comprend les impôts sur les bénéfices."
    }
    
    account_class = models.ForeignKey(
        AccountClass,
        on_delete=models.CASCADE,
        verbose_name="Classe de compte",
        help_text="Classe de compte à laquelle appartient ce groupe."
    )
    
    number = models.PositiveSmallIntegerField(
        unique=True,
        validators=[
            MinValueValidator(10, message="Le numéro de groupe doit être au minimum 10."),
            MaxValueValidator(89, message="Le numéro de groupe doit être au maximum 89.")
        ],
        verbose_name="Numéro",
        help_text="Numéro du groupe de comptes (ex: 10, 11, etc.)"
    )
    
    name = models.CharField(
        max_length=100,
        verbose_name="Nom",
        editable=False,  # Rend le champ non modifiable dans l'interface
        help_text="Nom du groupe de comptes (généré automatiquement)."
    )
    
    description = models.TextField(
        blank=True,
        verbose_name="Description",
        editable=False,  # Rend le champ non modifiable dans l'interface
        help_text="Description détaillée du groupe de comptes (générée automatiquement)."
    )
    
    actif = models.BooleanField(
        default=True,
        verbose_name="Actif",
        help_text="Indique si ce groupe est actif dans le plan comptable."
    )
    
    date_creation = models.DateTimeField(
        verbose_name="Date de création",
        auto_now_add=True
    )
    
    class Meta:
        app_label = 'accounts'
        ordering = ['number']
        unique_together = [['account_class', 'number']]
        verbose_name = "Groupe de comptes"
        verbose_name_plural = "Groupes de comptes"
    
    def __str__(self):
        return f"{self.account_class.number}{self.number} - {self.name}"
    
    def clean(self):
        # Vérifier que le numéro de groupe est cohérent avec la classe sélectionnée
        if self.account_class and self.number:
            # Obtenir le premier chiffre du numéro de groupe
            first_digit = self.number // 10
            
            # Vérifier que le premier chiffre correspond à la classe
            if first_digit != self.account_class.number:
                raise ValidationError({
                    'number': f"Le numéro de groupe doit commencer par {self.account_class.number} pour la classe sélectionnée."
                })
            
            # Vérifier que le deuxième chiffre est entre 0 et 9
            second_digit = self.number % 10
            if second_digit < 0 or second_digit > 9:
                raise ValidationError({
                    'number': "Le deuxième chiffre du numéro de groupe doit être entre 0 et 9."
                })
        
        super().clean()
    
    def save(self, *args, **kwargs):
        # Définir automatiquement le nom et la description en fonction du numéro
        if self.number in self.NOMS_GROUPES:
            self.name = self.NOMS_GROUPES[self.number]
            self.description = self.DESCRIPTIONS_GROUPES.get(self.number, "")
        
        # Vérifier la cohérence avec la classe avant sauvegarde
        self.clean()
        
        super().save(*args, **kwargs)
