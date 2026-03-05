import sys, os
from modules import (fluids, calculations)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QStackedWidget,
                             QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QSizePolicy, QSpacerItem,
                             QComboBox, QLineEdit, QMessageBox, QGridLayout, QRadioButton, QTabWidget, QTextEdit, QFileDialog)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from fpdf import FPDF

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Dimensionnement des Échangeurs de Chaleur")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #f4f4f9;")

        self.data = {}  # Stockage centralisé des données

        # Conteneur principal avec QStackedWidget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.stacked_widget = QStackedWidget()

        # Initialisation des pages (les fonctions seront créées ou ajustées plus tard)
        self.accueil_page = self.create_accueil_page()
        self.choix_fluides_page = self.create_choix_fluides_page()
        self.proprietes_huile_page = None
        self.proprietes_thermo_page = self.create_proprietes_thermo_page()

        self.passes_results_page = self.create_passes_results_page()
        self.viscosity_dimensions_page = self.create_viscosity_dimensions_page()
        self.intermediate_results_page = self.create_intermediate_results_page()
        self.coefficient_global_page = self.create_coefficient_global_page()
        self.pertes_charge_page = self.create_pertes_charge_page()
        self.synthese_page = self.create_synthese_page()
        

        # Ajout des pages au gestionnaire de pages
        self.stacked_widget.addWidget(self.accueil_page)
        self.stacked_widget.addWidget(self.choix_fluides_page)
        self.stacked_widget.addWidget(self.proprietes_thermo_page)
        
        self.stacked_widget.addWidget(self.passes_results_page)
        self.stacked_widget.addWidget(self.viscosity_dimensions_page)
        self.stacked_widget.addWidget(self.intermediate_results_page)
        self.stacked_widget.addWidget(self.coefficient_global_page)
        self.stacked_widget.addWidget(self.pertes_charge_page)
        self.stacked_widget.addWidget(self.synthese_page)


        # Layout principal
        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.central_widget.setLayout(layout)

        # Afficher l'écran d'accueil par défaut
        self.stacked_widget.setCurrentWidget(self.accueil_page)

    def create_accueil_page(self):
        """Créer l'écran d'accueil."""
        page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Ajouter un conteneur central pour centrer le contenu
        central_layout = QVBoxLayout()
        central_layout.setAlignment(Qt.AlignCenter)

        label = QLabel("Bienvenue dans l'outil de dimensionnement des échangeurs de chaleur")
        label.setFont(QFont("Arial", 16, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)

        bouton_commencer = QPushButton("Commencer")
        bouton_commencer.setFont(QFont("Arial", 12))
        bouton_commencer.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        bouton_commencer.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.choix_fluides_page))

        # Ajouter le label et le bouton dans le conteneur central
        central_layout.addWidget(label, alignment=Qt.AlignCenter)
        central_layout.addWidget(bouton_commencer, alignment=Qt.AlignCenter)

        # Ajouter le conteneur central au layout principal
        layout.addLayout(central_layout)

        page.setLayout(layout)
        return page

    def create_choix_fluides_page(self):
        """Créer l'écran de choix des fluides."""
        page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        label = QLabel("Choisissez les fluides et saisissez les paramètres initiaux")
        label.setFont(QFont("Arial", 14))
        label.setAlignment(Qt.AlignCenter)

        form_layout = QVBoxLayout()

        # Fluide chaud
        label_fluide_chaud = QLabel("Fluide chaud :")
        self.combo_fluide_chaud = QComboBox()
        self.combo_fluide_chaud.addItems(["Air", "Eau", "Huile lubrifiant"])

        label_temp_chaud = QLabel("Température entrée (°C) :")
        self.input_temp_entree_chaud = QLineEdit()
        label_temp_sortie_chaud = QLabel("Température sortie (°C) :")
        self.input_temp_sortie_chaud = QLineEdit()

        label_pression_chaud = QLabel("Pression (Pa) :")
        self.input_pression_chaud = QLineEdit()
        label_debit_chaud = QLabel("Débit massique (kg/s) :")
        self.input_debit_chaud = QLineEdit()

        # Ajouter un espace avant le fluide froid
        spacer = QSpacerItem(20, 25, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # Fluide froid
        label_fluide_froid = QLabel("Fluide froid :")
        self.combo_fluide_froid = QComboBox()
        self.combo_fluide_froid.addItems(["Air", "Eau", "Huile lubrifiant"])

        label_temp_froid = QLabel("Température entrée (°C) :")
        self.input_temp_entree_froid = QLineEdit()
        label_temp_sortie_froid = QLabel("Température sortie (°C) :")
        self.input_temp_sortie_froid = QLineEdit()

        label_pression_froid = QLabel("Pression (Pa) :")
        self.input_pression_froid = QLineEdit()
        label_debit_froid = QLabel("Débit massique (kg/s) :")
        self.input_debit_froid = QLineEdit()

        # Ajouter les widgets au formulaire
        form_layout.addWidget(label_fluide_chaud)
        form_layout.addWidget(self.combo_fluide_chaud)
        form_layout.addWidget(label_temp_chaud)
        form_layout.addWidget(self.input_temp_entree_chaud)
        form_layout.addWidget(label_temp_sortie_chaud)
        form_layout.addWidget(self.input_temp_sortie_chaud)
        form_layout.addWidget(label_pression_chaud)
        form_layout.addWidget(self.input_pression_chaud)
        form_layout.addWidget(label_debit_chaud)
        form_layout.addWidget(self.input_debit_chaud)
        form_layout.addItem(spacer) # Espace
        form_layout.addWidget(label_fluide_froid)
        form_layout.addWidget(self.combo_fluide_froid)
        form_layout.addWidget(label_temp_froid)
        form_layout.addWidget(self.input_temp_entree_froid)
        form_layout.addWidget(label_temp_sortie_froid)
        form_layout.addWidget(self.input_temp_sortie_froid)
        form_layout.addWidget(label_pression_froid)
        form_layout.addWidget(self.input_pression_froid)
        form_layout.addWidget(label_debit_froid)
        form_layout.addWidget(self.input_debit_froid)

        # Boutons navigation
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        bouton_retour = QPushButton("Retour")
        bouton_retour.setFont(QFont("Arial", 12))
        bouton_retour.setStyleSheet("background-color: #f44336; color: white; padding: 8px; border-radius: 5px;")
        bouton_retour.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        bouton_retour.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.accueil_page))
        button_layout.addWidget(bouton_retour)

        bouton_suivant = QPushButton("Suivant")
        bouton_suivant.setFont(QFont("Arial", 12))
        bouton_suivant.setStyleSheet("background-color: #2196F3; color: white; padding: 8px; border-radius: 5px;")
        bouton_suivant.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        bouton_suivant.clicked.connect(self.valider_choix_fluides)
        button_layout.addWidget(bouton_suivant)

        button_layout.addStretch()

        layout.addWidget(label)
        layout.addLayout(form_layout)
        layout.addStretch()
        layout.addLayout(button_layout)
        layout.addStretch()
        page.setLayout(layout)

        return page

    def valider_choix_fluides(self):
        """Valider les choix des fluides et rechercher les propriétés thermophysiques."""
        try:
            # Récupérer les entrées utilisateur
            fluide_chaud = self.combo_fluide_chaud.currentText().lower()
            T_in_chaud = float(self.input_temp_entree_chaud.text())
            T_out_chaud = float(self.input_temp_sortie_chaud.text())
            P_chaud = float(self.input_pression_chaud.text())
            debit_chaud = float(self.input_debit_chaud.text())

            fluide_froid = self.combo_fluide_froid.currentText().lower()
            T_in_froid = float(self.input_temp_entree_froid.text())
            T_out_froid = float(self.input_temp_sortie_froid.text())
            P_froid = float(self.input_pression_froid.text())
            debit_froid = float(self.input_debit_froid.text())

            # Calculer la température moyenne pour chaque fluide
            T_moy_chaud = (T_in_chaud + T_out_chaud) / 2
            T_moy_froid = (T_in_froid + T_out_froid) / 2

            # Enregistrer les données de base
            self.data['fluide_chaud'] = {"type": fluide_chaud, "T_in_chaud": T_in_chaud, "T_out_chaud": T_out_chaud, "P_chaud":P_chaud, "debit_chaud": debit_chaud, "T_moy_chaud":T_moy_chaud}
            self.data['fluide_froid'] = {"type": fluide_froid, "T_in_froid": T_in_froid, "T_out_froid": T_out_froid, "P_froid":P_froid, "debit_froid": debit_froid, "T_moy_froid":T_moy_froid}            

            # Gestion des redirections
            if fluide_chaud == "huile lubrifiant" and fluide_froid == "huile lubrifiant":
                # D'abord pour le fluide chaud, puis pour le fluide froid
                self.redirect_to_proprietes_huile("chaud")
                self.pending_redirect = "froid"  # Indique que le fluide froid doit être traité après
            elif fluide_chaud == "huile lubrifiant":
                self.data["fluide_froid"]["props"] = fluids.obtenir_proprietes(fluide_froid, T_moy_froid, P_froid) # Obtenir les props du fluide froid
                self.redirect_to_proprietes_huile("chaud")
            elif fluide_froid == "huile lubrifiant":
                self.data["fluide_chaud"]["props"] = fluids.obtenir_proprietes(fluide_chaud, T_moy_chaud, P_chaud) # Obtenir les props du fluide chaud
                self.redirect_to_proprietes_huile("froid")
            else:
                self.data["fluide_chaud"]["props"] = fluids.obtenir_proprietes(fluide_chaud, T_moy_chaud, P_chaud)
                self.data["fluide_froid"]["props"] = fluids.obtenir_proprietes(fluide_froid, T_moy_froid, P_froid) 
                ### QMessageBox.information(self, "Info", "Choix des fluides validés.")
                self.update_proprietes_thermo_page()
                self.stacked_widget.setCurrentWidget(self.proprietes_thermo_page)
                

        except ValueError as e:
            QMessageBox.warning(self, "Erreur", f"Entrée invalide : {e}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue : {e}")

    def redirect_to_proprietes_huile(self, type_fluide):
        """Rediriger vers la page des propriétés pour l'huile."""
        if not self.proprietes_huile_page:
            self.proprietes_huile_page = self.create_proprietes_huile_page()
            self.stacked_widget.addWidget(self.proprietes_huile_page)

        # Mettre à jour le contexte de la page
        self.proprietes_huile_page.set_context(type_fluide)
        self.stacked_widget.setCurrentWidget(self.proprietes_huile_page)

    def create_proprietes_huile_page(self):
        """Créer une page pour entrer les propriétés de l'huile."""
        page = QWidget()
        layout = QVBoxLayout()

        self.label_proprietes_huile = QLabel("")
        self.label_proprietes_huile.setFont(QFont("Arial", 14))
        self.label_proprietes_huile.setAlignment(Qt.AlignCenter)

        # Champs de saisie pour les propriétés
        self.input_cp = QLineEdit()
        self.input_k = QLineEdit()
        self.input_rho = QLineEdit()
        self.input_mu = QLineEdit()
        self.input_Pr = QLineEdit()

        form_layout = QVBoxLayout()
        form_layout.addWidget(QLabel("Capacité calorifique (cp, J/kg.K) :"))
        form_layout.addWidget(self.input_cp)
        form_layout.addWidget(QLabel("Conductivité thermique (k, W/m.K) :"))
        form_layout.addWidget(self.input_k)
        form_layout.addWidget(QLabel("Masse volumique (rho, kg/m³) :"))
        form_layout.addWidget(self.input_rho)
        form_layout.addWidget(QLabel("Viscosité dynamique (mu, Pa.s) :"))
        form_layout.addWidget(self.input_mu)
        form_layout.addWidget(QLabel("Nombre de Prandtl (Pr) :"))
        form_layout.addWidget(self.input_Pr)

        bouton_valider = QPushButton("Valider")
        bouton_valider.clicked.connect(lambda: self.valider_proprietes_huile())

        layout.addWidget(self.label_proprietes_huile)
        layout.addLayout(form_layout)
        layout.addWidget(bouton_valider, alignment=Qt.AlignRight)
        page.setLayout(layout)

        # Ajouter une méthode pour mettre à jour le contexte
        page.set_context = self.set_context_proprietes_huile

        return page

    def set_context_proprietes_huile(self, type_fluide):
        """Mettre à jour le contexte pour les propriétés de l'huile."""
        self.current_fluide = type_fluide
        self.label_proprietes_huile.setText(f"Entrez les propriétés de l'huile pour le fluide {type_fluide}.")


    def valider_proprietes_huile(self):
        """Valider les propriétés de l'huile et rediriger si nécessaire."""
        try:
            props = {
                "cp": float(self.input_cp.text()),
                "k": float(self.input_k.text()),
                "rho": float(self.input_rho.text()),
                "mu": float(self.input_mu.text()),
                "Pr": float(self.input_Pr.text()),
            }
            self.data[f"fluide_{self.current_fluide}"]["props"] = props

            # Vérifier si un autre fluide doit être traité
            if hasattr(self, "pending_redirect") and self.pending_redirect:
                next_fluide = self.pending_redirect
                self.pending_redirect = None
                ### Vider les champs ou charger les données précédentes...
                self.redirect_to_proprietes_huile(next_fluide)
            else:
                ### QMessageBox.information(self, "Info", "Propriétés de l'huile validées.")
                self.update_proprietes_thermo_page()
                self.stacked_widget.setCurrentWidget(self.proprietes_thermo_page)

        except ValueError:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer des valeurs valides pour toutes les propriétés.")


#===================================================================================================================
# Propriétés thermophysiques
#===================================================================================================================


    def create_proprietes_thermo_page(self):
        """Créer l'écran des propriétés thermophysiques avec un design amélioré."""
        page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # Titre principal
        label = QLabel("Propriétés thermophysiques des fluides")
        label.setFont(QFont("Arial", 18, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: #333333; padding: 10px;")

        # Tableau structuré pour les propriétés
        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(30)
        grid_layout.setVerticalSpacing(15)

        # Entêtes de colonnes avec style
        header_style = "font-size: 14px; font-weight: bold; background-color: #344955; color: white; padding: 5px; border-radius: 5px;"
        grid_layout.addWidget(self._create_header_label("Propriété", header_style), 0, 0)
        grid_layout.addWidget(self._create_header_label("Fluide chaud", header_style), 0, 1)
        grid_layout.addWidget(self._create_header_label("Fluide froid", header_style), 0, 2)

        # Champs des propriétés
        self.props_labels = {}
        properties = [
            "Type de fluide",
            "Température d'entrée (°C)",
            "Température de sortie (°C)",
            "Débit massique (kg/s)",
            "Capacité calorifique (cp, J/kg.K)",
            "Conductivité thermique (k, W/m.K)",
            "Masse volumique (ρ, kg/m³)",
            "Nombre de Prandtl (Pr)",
            "Viscosité dynamique (μ, Pa.s)"
        ]

        for row, prop in enumerate(properties, start=1):
            # Colonne des propriétés
            grid_layout.addWidget(self._create_property_label(prop), row, 0)

            # Labels dynamiques pour le fluide chaud
            chaud_label = self._create_value_label()
            grid_layout.addWidget(chaud_label, row, 1)
            self.props_labels[f"chaud_{prop}"] = chaud_label

            # Labels dynamiques pour le fluide froid
            froid_label = self._create_value_label()
            grid_layout.addWidget(froid_label, row, 2)
            self.props_labels[f"froid_{prop}"] = froid_label

        # Boutons de navigation
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        bouton_retour = QPushButton("Retour")
        bouton_retour.setFont(QFont("Arial", 12))
        bouton_retour.setStyleSheet("background-color: #f44336; color: white; padding: 8px; border-radius: 5px;")
        bouton_retour.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.choix_fluides_page))
        button_layout.addWidget(bouton_retour)

        bouton_suivant = QPushButton("Suivant")
        bouton_suivant.setFont(QFont("Arial", 12))
        bouton_suivant.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px; border-radius: 5px;")
        bouton_suivant.clicked.connect(self.update_to_next_page)
        button_layout.addWidget(bouton_suivant)

        button_layout.addStretch()

        # Ajouter les widgets au layout principal
        layout.addWidget(label)
        layout.addLayout(grid_layout)
        layout.addStretch()
        layout.addLayout(button_layout)
        layout.addStretch()
        page.setLayout(layout)

        return page

    def _create_header_label(self, text, style):
        """Créer un label pour les entêtes de colonnes."""
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(style)
        return label

    def _create_property_label(self, text):
        """Créer un label pour la colonne des propriétés."""
        label = QLabel(text)
        label.setFont(QFont("Arial", 12, QFont.Bold))
        label.setAlignment(Qt.AlignLeft)
        label.setStyleSheet("color: #555555; padding: 3px;")
        return label

    def _create_value_label(self):
        """Créer un label pour les valeurs dynamiques."""
        label = QLabel("N/A")
        label.setFont(QFont("Arial", 12))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: #333333; background-color: #f0f0f0; padding: 2px; border: 1px solid #ccc; border-radius: 2px;")
        return label

    def update_proprietes_thermo_page(self):
        """Mettre à jour les données affichées dans le tableau des propriétés thermophysiques."""
        if not hasattr(self, "data") or not self.data:
            for key in self.props_labels:
                self.props_labels[key].setText("N/A")
            return

        # Données pour le fluide chaud
        fluide_chaud = self.data.get("fluide_chaud", {})
        if fluide_chaud:
            props = fluide_chaud.get("props", {})
            self.props_labels["chaud_Type de fluide"].setText(fluide_chaud.get("type", "N/A").capitalize())
            self.props_labels["chaud_Température d'entrée (°C)"].setText(str(fluide_chaud.get("T_in_chaud", "N/A")))
            self.props_labels["chaud_Température de sortie (°C)"].setText(str(fluide_chaud.get("T_out_chaud", "N/A")))
            self.props_labels["chaud_Débit massique (kg/s)"].setText(str(fluide_chaud.get("debit_chaud", "N/A")))
            self.props_labels["chaud_Capacité calorifique (cp, J/kg.K)"].setText(str(props.get("cp", "N/A")))
            self.props_labels["chaud_Conductivité thermique (k, W/m.K)"].setText(str(props.get("k", "N/A")))
            self.props_labels["chaud_Masse volumique (ρ, kg/m³)"].setText(str(props.get("rho", "N/A")))
            self.props_labels["chaud_Nombre de Prandtl (Pr)"].setText(str(props.get("Pr", "N/A")))
            self.props_labels["chaud_Viscosité dynamique (μ, Pa.s)"].setText(str(props.get("mu", "N/A")))

        # Données pour le fluide froid
        fluide_froid = self.data.get("fluide_froid", {})
        if fluide_froid:
            props = fluide_froid.get("props", {})
            self.props_labels["froid_Type de fluide"].setText(fluide_froid.get("type", "N/A").capitalize())
            self.props_labels["froid_Température d'entrée (°C)"].setText(str(fluide_froid.get("T_in_froid", "N/A")))
            self.props_labels["froid_Température de sortie (°C)"].setText(str(fluide_froid.get("T_out_froid", "N/A")))
            self.props_labels["froid_Débit massique (kg/s)"].setText(str(fluide_froid.get("debit_froid", "N/A")))
            self.props_labels["froid_Capacité calorifique (cp, J/kg.K)"].setText(str(props.get("cp", "N/A")))
            self.props_labels["froid_Conductivité thermique (k, W/m.K)"].setText(str(props.get("k", "N/A")))
            self.props_labels["froid_Masse volumique (ρ, kg/m³)"].setText(str(props.get("rho", "N/A")))
            self.props_labels["froid_Nombre de Prandtl (Pr)"].setText(str(props.get("Pr", "N/A")))
            self.props_labels["froid_Viscosité dynamique (μ, Pa.s)"].setText(str(props.get("mu", "N/A")))

    def update_to_next_page(self):
        """Passer à la page suivante depuis les propriétés thermophysiques."""
        # self.update_calculs_intermediaires()
        self.stacked_widget.setCurrentWidget(self.passes_results_page)


#===================================================================================================================
# Résultats intermédiaires
#===================================================================================================================


    def create_passes_results_page(self):
        """Créer la page des résultats intermédiaires liés aux passes."""
        page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # Titre principal
        title_label = QLabel("Résultats Intermédiaires : Nombre de Passes et Coefficient d'Échange")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)

        # Ajouter un espace sous le titre
        layout.addSpacing(20)

        # Section 1 : Choix du nombre de passes et coefficient d'échange supposé
        section1_layout = QVBoxLayout()
        section1_title = QLabel("Paramètres : Nombre de Passes et Coefficient d'Échange")
        section1_title.setFont(QFont("Arial", 14, QFont.Bold))
        section1_layout.addWidget(section1_title)

        # Nombre de passes
        section1_layout.addWidget(QLabel("Nombre de passes :"))
        passes_layout = QVBoxLayout()
        self.radio_pass_1 = QRadioButton("1 Passe")
        self.radio_pass_2 = QRadioButton("2 Passes")
        self.radio_pass_1.setChecked(True)  # Valeur par défaut
        self.radio_pass_1.clicked.connect(self.hide_results_section)
        self.radio_pass_2.clicked.connect(self.hide_results_section)
        passes_layout.addWidget(self.radio_pass_1)
        passes_layout.addWidget(self.radio_pass_2)
        section1_layout.addLayout(passes_layout)

        # Coefficient d'échange supposé
        section1_layout.addWidget(QLabel("Coefficient d'échange supposé (W/m².K) :"))
        self.input_Uo_supp = QLineEdit()
        self.input_Uo_supp.textChanged.connect(self.hide_results_section)  # Cacher les résultats si modifié
        section1_layout.addWidget(self.input_Uo_supp)

        # Bouton Valider
        self.button_valider_passes = QPushButton("Valider")
        self.button_valider_passes.setFont(QFont("Arial", 12))
        self.button_valider_passes.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px; border-radius: 5px;")
        self.button_valider_passes.clicked.connect(self.calculate_passes_results)
        section1_layout.addWidget(self.button_valider_passes, alignment=Qt.AlignCenter)

        # Section 2 : Résultats intermédiaires (initialement masqués)
        self.results_section = QWidget()
        results_layout = QVBoxLayout(self.results_section)
        results_title = QLabel("Résultats Intermédiaires")
        results_title.setFont(QFont("Arial", 14, QFont.Bold))
        results_layout.addWidget(results_title)

        results_table = QGridLayout()
        results_table.setHorizontalSpacing(20)
        results_table.setVerticalSpacing(10)

        results_table.addWidget(QLabel("Nombre d'unités de transfert (NTU) :"), 0, 0)
        self.result_NTU = QLabel("N/A")
        self.result_NTU.setStyleSheet("background-color: #f4f4f4; padding: 5px; border: 1px solid #ccc;")
        results_table.addWidget(self.result_NTU, 0, 1)

        results_table.addWidget(QLabel("Rendement thermique (η) :"), 1, 0)
        self.result_eta = QLabel("N/A")
        self.result_eta.setStyleSheet("background-color: #f4f4f4; padding: 5px; border: 1px solid #ccc;")
        results_table.addWidget(self.result_eta, 1, 1)

        results_table.addWidget(QLabel("Surface d'échange thermique calculée (S₀, m²) :"), 2, 0)
        self.result_S0 = QLabel("N/A")
        self.result_S0.setStyleSheet("background-color: #f4f4f4; padding: 5px; border: 1px solid #ccc;")
        results_table.addWidget(self.result_S0, 2, 1)

        results_layout.addLayout(results_table)
        self.results_section.setVisible(False)  # Cacher la section initialement

        # Boutons de navigation
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        bouton_retour = QPushButton("Retour")
        bouton_retour.setFont(QFont("Arial", 12))
        bouton_retour.setStyleSheet("background-color: #f44336; color: white; padding: 8px; border-radius: 5px;")
        bouton_retour.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.proprietes_thermo_page))
        button_layout.addWidget(bouton_retour)

        self.bouton_suivant0 = QPushButton("Suivant")
        self.bouton_suivant0.setFont(QFont("Arial", 12))
        self.bouton_suivant0.setStyleSheet("background-color: #7AAD74; color: white; padding: 8px; border-radius: 5px;")
        self.bouton_suivant0.setEnabled(False)  # Désactiver initialement
        self.bouton_suivant0.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.viscosity_dimensions_page))
        button_layout.addWidget(self.bouton_suivant0)

        button_layout.addStretch()

        # Ajout au layout principal
        layout.addWidget(title_label)
        layout.addLayout(section1_layout)
        layout.addSpacing(20)
        layout.addWidget(self.results_section)
        layout.addStretch()
        layout.addLayout(button_layout)
        page.setLayout(layout)

        return page


    def calculate_passes_results(self):
        """Calculer les résultats intermédiaires et afficher la section des résultats."""
        try:
            # Récupération des entrées utilisateur
            Uo_supp = float(self.input_Uo_supp.text())
            passes = 1 if self.radio_pass_1.isChecked() else 2

            # Récupération des données des fluides
            fluide_chaud = self.data["fluide_chaud"]
            fluide_froid = self.data["fluide_froid"]

            # Débits calorifiques
            C_chaud = fluide_chaud["debit_chaud"] * fluide_chaud["props"]["cp"]
            C_froid = fluide_froid["debit_froid"] * fluide_froid["props"]["cp"]

            # Calculs intermédiaires
            eta, condition_eta = calculations.calculer_rendement(
                C_chaud, C_froid,
                fluide_chaud["T_in_chaud"], fluide_chaud["T_out_chaud"],
                fluide_froid["T_in_froid"], fluide_froid["T_out_froid"]
            )
            Z = calculations.calculer_rapport_Z(C_chaud, C_froid)
            NTU = calculations.calculer_NTU(eta, Z, passes)

            # Surface d'échange thermique (S₀)
            S0 = calculations.calculer_surface_echange(NTU, min(C_chaud, C_froid), Uo_supp)

            # Mise à jour des résultats
            self.result_NTU.setText(f"{NTU:.3f}")
            self.result_eta.setText(f"{eta:.2%}")
            self.result_S0.setText(f"{S0:.2f} m²")

            # Afficher la section des résultats et activer "Suivant"
            self.results_section.setVisible(True)
            self.bouton_suivant0.setEnabled(True)
            self.bouton_suivant0.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px; border-radius: 5px;")

            # Stockage des résultats dans self.data
            self.data["passes_results"] = {
                "Uo_supp": Uo_supp,
                "passes": passes,
                "NTU": NTU,
                "eta": eta,
                "S0": S0,
                "condition_eta":condition_eta
            }

        except ValueError:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un coefficient d'échange supposé valide.")
        except KeyError as e:
            QMessageBox.critical(self, "Erreur", f"Données manquantes : {e}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur inattendue est survenue : {e}")


    def hide_results_section(self):
        """Cacher la section des résultats intermédiaires si le coefficient supposé est modifié."""
        self.results_section.setVisible(False)
        self.bouton_suivant0.setEnabled(False)  # Désactiver le bouton "Suivant"
        self.bouton_suivant0.setStyleSheet("background-color: #7AAD74; color: white; padding: 8px; border-radius: 5px;")  # Assombrir la couleur du bouton "Suivant"
        

#===================================================================================================================
# Page de saisie viscosités et dimensions tube
#===================================================================================================================


    def create_viscosity_dimensions_page(self):
        """Créer la page pour saisir les viscosités dynamiques et dimensions des tubes."""
        page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # Titre principal
        title_label = QLabel("Saisie des Viscosités Dynamiques et Dimensions des Tubes")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        layout.addSpacing(20)  # Espacement sous le titre

        # Section 1 : Viscosités dynamiques
        section1_layout = QVBoxLayout()
        section1_title = QLabel("Viscosités Dynamiques")
        section1_title.setFont(QFont("Arial", 14, QFont.Bold))
        section1_layout.addWidget(section1_title)

        section1_layout.addWidget(QLabel("Viscosité dynamique côté paroi pour le fluide chaud (Pa.s) :"))
        self.input_viscosity_chaud = QLineEdit()
        section1_layout.addWidget(self.input_viscosity_chaud)

        section1_layout.addWidget(QLabel("Viscosité dynamique côté paroi pour le fluide froid (Pa.s) :"))
        self.input_viscosity_froid = QLineEdit()
        section1_layout.addWidget(self.input_viscosity_froid)

        layout.addLayout(section1_layout)
        layout.addSpacing(20)  # Espacement entre les sections

        # Section 2 : Dimensions des tubes et maille
        section2_layout = QVBoxLayout()
        section2_title = QLabel("Dimensions des Tubes et Type de Maille")
        section2_title.setFont(QFont("Arial", 14, QFont.Bold))
        section2_layout.addWidget(section2_title)

        form_layout = QGridLayout()
        form_layout.setHorizontalSpacing(20)
        form_layout.setVerticalSpacing(10)

        form_layout.addWidget(QLabel("Diamètre extérieur (m) :"), 0, 0)
        self.input_d_ext = QLineEdit()
        form_layout.addWidget(self.input_d_ext, 0, 1)

        form_layout.addWidget(QLabel("Diamètre intérieur (m) :"), 1, 0)
        self.input_d_int = QLineEdit()
        form_layout.addWidget(self.input_d_int, 1, 1)

        form_layout.addWidget(QLabel("Épaisseur suivant BWG (sans unité) :"), 2, 0)
        self.input_bwg = QLineEdit()
        form_layout.addWidget(self.input_bwg, 2, 1)

        form_layout.addWidget(QLabel("Épaisseur réelle (e, m) :"), 3, 0)
        self.input_e = QLineEdit()
        form_layout.addWidget(self.input_e, 3, 1)

        form_layout.addWidget(QLabel("Longueur des tubes (m) :"), 4, 0)
        self.input_longueur = QLineEdit()
        form_layout.addWidget(self.input_longueur, 4, 1)

        form_layout.addWidget(QLabel("Répartition des tubes dans le faisceau :"), 5, 0)
        self.input_repartition = QLineEdit()
        form_layout.addWidget(self.input_repartition, 5, 1)

        # Type de maille (Boutons d'option)
        form_layout.addWidget(QLabel("Type de maille :"), 6, 0)
        self.radio_carre = QRadioButton("Carré")
        self.radio_triangulaire = QRadioButton("Triangulaire")
        maille_layout = QHBoxLayout()
        maille_layout.addWidget(self.radio_carre)
        maille_layout.addWidget(self.radio_triangulaire)
        self.radio_carre.setChecked(True)  # Valeur par défaut
        form_layout.addLayout(maille_layout, 6, 1)

        section2_layout.addLayout(form_layout)
        layout.addLayout(section2_layout)
        layout.addStretch()

        # Boutons de navigation
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        bouton_retour = QPushButton("Retour")
        bouton_retour.setFont(QFont("Arial", 12))
        bouton_retour.setStyleSheet("background-color: #f44336; color: white; padding: 8px; border-radius: 5px;")
        bouton_retour.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.passes_results_page))
        button_layout.addWidget(bouton_retour)

        bouton_suivant = QPushButton("Suivant")
        bouton_suivant.setFont(QFont("Arial", 12))
        bouton_suivant.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px; border-radius: 5px;")
        bouton_suivant.clicked.connect(self.validate_viscosity_dimensions)
        button_layout.addWidget(bouton_suivant)

        button_layout.addStretch()
        layout.addLayout(button_layout)
        page.setLayout(layout)

        return page


    def validate_viscosity_dimensions(self):
        """Valider les viscosités dynamiques et dimensions des tubes."""
        errors = []  # Liste des messages d'erreur

        # Valider les viscosités dynamiques
        viscosity_chaud = self.validate_positive_float(self.input_viscosity_chaud.text(), "Viscosité dynamique côté paroi (fluide chaud)", errors)
        viscosity_froid = self.validate_positive_float(self.input_viscosity_froid.text(), "Viscosité dynamique côté paroi (fluide froid)", errors)

        # Valider les dimensions des tubes
        d_ext = self.validate_positive_float(self.input_d_ext.text(), "Diamètre extérieur des tubes", errors)
        d_int = self.validate_positive_float(self.input_d_int.text(), "Diamètre intérieur des tubes", errors)
        bwg = self.validate_positive_int(self.input_bwg.text(), "Épaisseur suivant BWG", errors)
        e = self.validate_positive_float(self.input_e.text(), "Épaisseur des tubes", errors)
        longueur = self.validate_positive_float(self.input_longueur.text(), "Longueur des tubes", errors)
        repartition = self.validate_positive_float(self.input_repartition.text(), "Répartition des tubes", errors)


        # Valider les relations physiques entre les dimensions
        if d_ext is not None and d_int is not None and d_ext <= d_int:
            errors.append("Le diamètre extérieur doit être supérieur au diamètre intérieur.")
        if d_int is not None and e is not None and e >= d_int:
            errors.append("L'épaisseur des tubes doit être inférieure au diamètre intérieur.")

        # Si des erreurs existent, afficher une boîte de dialogue
        if errors:
            QMessageBox.warning(self, "Erreurs de validation", "\n".join(errors))
            return

        # Type de maille
        maille = "Carré" if self.radio_carre.isChecked() else "Triangulaire"

        # Stocker les données validées dans self.data
        self.data["viscosities"] = {"chaud": viscosity_chaud, "froid": viscosity_froid}
        self.data["dimensions_tubes"] = {
            "d_ext": d_ext,
            "d_int": d_int,
            "bwg": bwg,
            "e": e,
            "longueur": longueur,
            "repartition": repartition,
            "maille": maille,
        }

        # Transition vers la page suivante
        self.update_results_display()
        self.stacked_widget.setCurrentWidget(self.intermediate_results_page)

    def validate_positive_float(self, value, field_name, errors):
        """
        Valider qu'une valeur est un float strictement positif.
        Args:
            value (str): Valeur saisie.
            field_name (str): Nom du champ (pour les messages d'erreur).
            errors (list): Liste des erreurs accumulées.
        Returns:
            float | None: La valeur validée ou None en cas d'erreur.
        """
        try:
            result = float(value)
            if result <= 0:
                raise ValueError
            return result
        except ValueError:
            errors.append(f"Le champ '{field_name}' doit contenir un nombre décimal strictement positif.")
            return None

    def validate_positive_int(self, value, field_name, errors):
        """
        Valider qu'une valeur est un entier strictement positif.
        Args:
            value (str): Valeur saisie.
            field_name (str): Nom du champ (pour les messages d'erreur).
            errors (list): Liste des erreurs accumulées.
        Returns:
            int | None: La valeur validée ou None en cas d'erreur.
        """
        try:
            result = int(value)
            if result <= 0:
                raise ValueError
            return result
        except ValueError:
            errors.append(f"Le champ '{field_name}' doit contenir un entier strictement positif.")
            return None


#===================================================================================================================
# Page des résultats avancés
#===================================================================================================================


    def create_intermediate_results_page(self):
        """Créer la page des résultats intermédiaires pour les tubes et la calandre."""
        page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # Titre principal
        title_label = QLabel("Résultats Intermédiaires : Tubes et Calandre")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        layout.addSpacing(20)

        # Création des onglets
        tabs = QTabWidget()
        tabs.addTab(self.create_tube_results_tab(), "Résultats des Tubes")
        tabs.addTab(self.create_calandre_results_tab(), "Résultats de la Calandre")
        layout.addWidget(tabs)

        # Boutons de navigation
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        bouton_retour = QPushButton("Retour")
        bouton_retour.setFont(QFont("Arial", 12))
        bouton_retour.setStyleSheet("background-color: #f44336; color: white; padding: 8px; border-radius: 5px;")
        bouton_retour.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.viscosity_dimensions_page))
        button_layout.addWidget(bouton_retour)

        bouton_suivant = QPushButton("Suivant")
        bouton_suivant.setFont(QFont("Arial", 12))
        bouton_suivant.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px; border-radius: 5px;")
        bouton_suivant.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.coefficient_global_page))
        button_layout.addWidget(bouton_suivant)

        button_layout.addStretch()
        layout.addLayout(button_layout)
        page.setLayout(layout)

        return page


    def create_tube_results_tab(self):
        """Créer l'onglet pour afficher les résultats des tubes."""
        tab = QWidget()
        layout = QVBoxLayout()

        # Titre de la section
        section_title = QLabel("Résultats pour les Tubes")
        section_title.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(section_title)

        # Tableau des résultats
        table = QGridLayout()
        table.setHorizontalSpacing(20)
        table.setVerticalSpacing(10)

        table.addWidget(QLabel("Paramètres calculés :"), 0, 0, 1, 2)
        table.addWidget(QLabel("N_t0 (Nombre de tubes) :"), 1, 0)
        self.result_N_t0 = QLabel("N/A")
        table.addWidget(self.result_N_t0, 1, 1)

        table.addWidget(QLabel("D_v0 (Diamètre des tubes, m) :"), 2, 0)
        self.result_D_v0 = QLabel("N/A")
        table.addWidget(self.result_D_v0, 2, 1)

        table.addWidget(QLabel("L_c0 (Longueur des tubes, m) :"), 3, 0)
        self.result_L_c0 = QLabel("N/A")
        table.addWidget(self.result_L_c0, 3, 1)

        table.addWidget(QLabel("Résultats supplémentaires :"), 4, 0, 1, 2)
        table.addWidget(QLabel("Reynolds (Re) :"), 5, 0)
        self.result_Re_tube = QLabel("N/A")
        table.addWidget(self.result_Re_tube, 5, 1)

        table.addWidget(QLabel("Prandtl (Pr) :"), 6, 0)
        self.result_Pr_tube = QLabel("N/A")
        table.addWidget(self.result_Pr_tube, 6, 1)

        table.addWidget(QLabel("Nusselt (Nu) :"), 7, 0)
        self.result_Nu_tube = QLabel("N/A")
        table.addWidget(self.result_Nu_tube, 7, 1)

        table.addWidget(QLabel("Vitesse moyenne (u1, m/s) :"), 8, 0)
        self.result_u1 = QLabel("N/A")
        table.addWidget(self.result_u1, 8, 1)

        table.addWidget(QLabel("Coefficient de convection (h1, W/m².K) :"), 9, 0)
        self.result_h1 = QLabel("N/A")
        table.addWidget(self.result_h1, 9, 1)

        layout.addLayout(table)
        layout.addStretch()
        tab.setLayout(layout)
        return tab


    def create_calandre_results_tab(self):
        """Créer l'onglet pour afficher les résultats de la calandre."""
        tab = QWidget()
        layout = QVBoxLayout()

        # Titre de la section
        section_title = QLabel("Résultats pour la Calandre")
        section_title.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(section_title)

        # Tableau des résultats
        table = QGridLayout()
        table.setHorizontalSpacing(20)
        table.setVerticalSpacing(10)

        table.addWidget(QLabel("Paramètres calculés :"), 0, 0, 1, 2)
        table.addWidget(QLabel("Diamètre hydraulique (m) :"), 1, 0)
        self.result_d_eq = QLabel("N/A")
        table.addWidget(self.result_d_eq, 1, 1)

        table.addWidget(QLabel("Section équivalente (m²) :"), 2, 0)
        self.result_S_eq = QLabel("N/A")
        table.addWidget(self.result_S_eq, 2, 1)

        table.addWidget(QLabel("Vitesse équivalente (m/s) :"), 3, 0)
        self.result_u_eq = QLabel("N/A")
        table.addWidget(self.result_u_eq, 3, 1)

        table.addWidget(QLabel("Résultats supplémentaires :"), 4, 0, 1, 2)
        table.addWidget(QLabel("Reynolds (Re) :"), 5, 0)
        self.result_Re_calandre = QLabel("N/A")
        table.addWidget(self.result_Re_calandre, 5, 1)

        table.addWidget(QLabel("Nusselt (Nu) :"), 6, 0)
        self.result_Nu_calandre = QLabel("N/A")
        table.addWidget(self.result_Nu_calandre, 6, 1)

        table.addWidget(QLabel("Coefficient de convection (W/m².K) :"), 7, 0)
        self.result_h2 = QLabel("N/A")
        table.addWidget(self.result_h2, 7, 1)

        layout.addLayout(table)
        layout.addStretch()
        tab.setLayout(layout)
        return tab

    def update_results_display(self):
        """Mettre à jour les résultats intermédiaires pour les tubes et la calandre."""
        try:
            # Récupérer les données nécessaires depuis self.data
            dimensions = self.data["dimensions_tubes"]
            viscosities = self.data["viscosities"]
            fluide_chaud = self.data["fluide_chaud"]
            fluide_froid = self.data["fluide_froid"]
            passes = self.data["passes_results"]["passes"]
            S0 = self.data["passes_results"]["S0"]  # Surface d'échange thermique calculée

            # === Calculs pour les tubes ===
            # Paramètres des tubes
            param_tubes = calculations.calcul_parametres_tubes(
                dimensions["d_ext"], dimensions["d_int"], float(dimensions["repartition"]),  # lt
                dimensions["longueur"], S0, dimensions["maille"].lower(), passes
            )

            # Résultats supplémentaires pour les tubes
            supp_tubes = calculations.calcul_supplementaire_tubes(
                fluide_chaud["debit_chaud"], fluide_chaud["props"]["rho"], fluide_chaud["props"]["Pr"],
                param_tubes["n_t0"], dimensions["d_int"], fluide_chaud["props"]["mu"],
                viscosities["chaud"], fluide_chaud["props"]["k"], dimensions["longueur"], passes
            )

            # === Enregistrement des résultats des tubes dans self.data ===
            self.data["results_tubes"] = {
                "n_t0": param_tubes["n_t0"],
                "D_v0": param_tubes["D_v0"],
                "l_c0": param_tubes["l_c0"],
                "Re": supp_tubes["Re"],
                "Pr": supp_tubes["Pr"],
                "Nu": supp_tubes["Nu"],
                "u1": supp_tubes["u1"],
                "h1": supp_tubes["h1"]
            }

            # Mise à jour des résultats pour les tubes
            self.result_N_t0.setText(f"N_t0 : {param_tubes['n_t0']:.2f}")
            self.result_D_v0.setText(f"D_v0 : {param_tubes['D_v0']:.4f} m")
            self.result_L_c0.setText(f"L_c0 : {param_tubes['l_c0']:.4f} m")
            self.result_Re_tube.setText(f"Re : {supp_tubes['Re']:.2f}")
            self.result_Pr_tube.setText(f"Pr : {supp_tubes['Pr']:.4f}")
            self.result_Nu_tube.setText(f"Nu : {supp_tubes['Nu']:.4f}")
            self.result_u1.setText(f"u1 : {supp_tubes['u1']:.4f} m/s")
            self.result_h1.setText(f"h1 : {supp_tubes['h1']:.4f} W/m².K")

            # === Calculs pour la calandre ===
            supp_calandre = calculations.calcul_supplementaire_calandre(
                fluide_froid["debit_froid"], fluide_froid["props"]["rho"], fluide_froid["props"]["Pr"],
                dimensions["d_ext"], fluide_froid["props"]["mu"], viscosities["froid"],
                fluide_froid["props"]["k"], param_tubes["D_v0"], float(dimensions["repartition"]), param_tubes["l_c0"]
            )

            self.data["results_calandre"] = {
                "d_eq": supp_calandre["d_eq"],
                "S_eq": supp_calandre["S_eq"],
                "u_eq": supp_calandre["u_eq"],
                "Re": supp_calandre["Re"],
                "Nu": supp_calandre["Nu"],
                "h2": supp_calandre["h2"]
            }

            # Mise à jour des résultats pour la calandre
            self.result_d_eq.setText(f"d_eq : {supp_calandre['d_eq']:.4f} m")
            self.result_S_eq.setText(f"S_eq : {supp_calandre['S_eq']:.4f} m²")
            self.result_u_eq.setText(f"u_eq : {supp_calandre['u_eq']:.4f} m/s")
            self.result_Re_calandre.setText(f"Re : {supp_calandre['Re']:.4f}")
            self.result_Nu_calandre.setText(f"Nu : {supp_calandre['Nu']:.4f}")
            self.result_h2.setText(f"h2 : {supp_calandre['h2']:.4f} W/m².K")

            print(self.data)

        except KeyError as e:
            QMessageBox.warning(self, "Erreur", f"Données manquantes pour les calculs : {e}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur inattendue est survenue : {e}")





#===================================================================================================================
# Page de validation
#===================================================================================================================


    def create_coefficient_global_page(self):
        """Créer la page de saisie et validation du coefficient global d'échange thermique."""
        page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # Titre principal
        title_label = QLabel("Validation du Coefficient Global d'Échange Thermique")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        layout.addSpacing(20)

        # Section 1 : Saisie des résistances et conductivité
        section1_layout = QVBoxLayout()
        section1_title = QLabel("Saisie des paramètres")
        section1_title.setFont(QFont("Arial", 14, QFont.Bold))
        section1_layout.addWidget(section1_title)

        form_layout = QGridLayout()
        form_layout.setHorizontalSpacing(20)
        form_layout.setVerticalSpacing(10)

        form_layout.addWidget(QLabel("Résistance de salissement côté tube (m².K/W) :"), 0, 0)
        self.input_R_tube = QLineEdit()
        form_layout.addWidget(self.input_R_tube, 0, 1)

        form_layout.addWidget(QLabel("Résistance de salissement côté calandre (m².K/W) :"), 1, 0)
        self.input_R_calandre = QLineEdit()
        form_layout.addWidget(self.input_R_calandre, 1, 1)

        form_layout.addWidget(QLabel("Conductivité thermique du matériau des tubes (W/m.K) :"), 2, 0)
        self.input_k_mat = QLineEdit()
        form_layout.addWidget(self.input_k_mat, 2, 1)

        section1_layout.addLayout(form_layout)
        layout.addLayout(section1_layout)
        layout.addSpacing(20)

        # Section 2 : Affichage du coefficient global calculé
        section2_layout = QVBoxLayout()
        section2_title = QLabel("Résultats du Coefficient Global")
        section2_title.setFont(QFont("Arial", 14, QFont.Bold))
        section2_layout.addWidget(section2_title)

        self.result_U_glob = QLabel("Coefficient global calculé")
        self.result_U_glob.setFont(QFont("Arial", 12, QFont.Bold))
        self.result_U_glob.setAlignment(Qt.AlignCenter)
        self.result_U_glob.setStyleSheet("background-color: #f4f4f4; padding: 10px; border: 1px solid #ccc;")
        section2_layout.addWidget(self.result_U_glob)

        self.result_marge = QLabel("Marge d'erreur")
        self.result_marge.setFont(QFont("Arial", 12, QFont.Bold))
        self.result_marge.setAlignment(Qt.AlignCenter)
        self.result_marge.setStyleSheet("background-color: #f4f4f4; padding: 10px; border: 1px solid #ccc;")
        section2_layout.addWidget(self.result_marge)

        layout.addLayout(section2_layout)
        layout.addSpacing(20)

        # Boutons de validation et navigation
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        bouton_retour = QPushButton("Retour")
        bouton_retour.setFont(QFont("Arial", 12))
        bouton_retour.setStyleSheet("background-color: #f44336; color: white; padding: 8px; border-radius: 5px;")
        bouton_retour.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.intermediate_results_page))
        button_layout.addWidget(bouton_retour)

        self.bouton_valider = QPushButton("Valider")
        self.bouton_valider.setFont(QFont("Arial", 12))
        self.bouton_valider.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px; border-radius: 5px;")
        self.bouton_valider.clicked.connect(self.validate_coefficient_global)
        button_layout.addWidget(self.bouton_valider)

        self.bouton_iteration = QPushButton("Nouvelle Itération")
        self.bouton_iteration.setFont(QFont("Arial", 12))
        self.bouton_iteration.setStyleSheet("background-color: #bbbbbb; color: white; padding: 8px; border-radius: 5px;")
        self.bouton_iteration.setEnabled(False)
        self.bouton_iteration.clicked.connect(self.call_perte_charge_page)
        button_layout.addWidget(self.bouton_iteration)

        self.bouton_suivant1 = QPushButton("Suivant")
        self.bouton_suivant1.setFont(QFont("Arial", 12))
        self.bouton_suivant1.setStyleSheet("background-color: #bbbbbb; color: white; padding: 8px; border-radius: 5px;")
        self.bouton_suivant1.setEnabled(False)
        self.bouton_suivant1.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.pertes_charge_page))
        button_layout.addWidget(self.bouton_suivant1)

        button_layout.addStretch()
        layout.addLayout(button_layout)
        page.setLayout(layout)

        return page


    def validate_coefficient_global(self):
        """Valider le coefficient global d'échange thermique et sauvegarder les résultats."""
        try:
            # Récupération des entrées utilisateur
            R_tube = float(self.input_R_tube.text())
            R_calandre = float(self.input_R_calandre.text())
            k_mat = float(self.input_k_mat.text())

            # Récupération des valeurs nécessaires depuis self.data
            Uo_supp = self.data["passes_results"]["Uo_supp"]
            h1 = self.data["results_tubes"]["h1"]  # Coefficient de convection côté tubes
            h2 = self.data["results_calandre"]["h2"]  # Coefficient de convection côté calandre
            de = self.data["dimensions_tubes"]["d_ext"]
            di = self.data["dimensions_tubes"]["d_int"]

            # Calcul du coefficient global
            U_glob = calculations.calcul_coefficient_global_echange(h1, h2, de, di, R_calandre, R_tube, k_mat)

            # Validation avec la fonction du backend
            is_valid, marge = calculations.validation_coefficient_global_echange(Uo_supp, U_glob)

            # Mise à jour des résultats affichés
            self.result_U_glob.setText(f"Coefficient global calculé : {U_glob:.2f} W/m².K")
            self.result_marge.setText(f"Marge d'erreur : {marge:.2%}")

            # Enregistrement des résultats dans self.data
            self.data["coefficient_global"] = {
                "U_glob": U_glob,
                "Uo_supp": Uo_supp,
                "R_tube": R_tube,
                "R_calandre": R_calandre,
                "k_mat": k_mat,
                "marge": marge,
                "validation": is_valid
            }


            # Mise à jour des boutons et couleurs
            if is_valid:
                self.bouton_suivant1.setEnabled(True)
                self.bouton_suivant1.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px; border-radius: 5px;")
                self.bouton_iteration.setEnabled(True)
                self.bouton_iteration.setStyleSheet("background-color: #FFA500; color: white; padding: 8px; border-radius: 5px;")
            else:
                self.bouton_suivant1.setEnabled(False)
                self.bouton_suivant1.setStyleSheet("background-color: #bbbbbb; color: white; padding: 8px; border-radius: 5px;")
                self.bouton_iteration.setEnabled(True)
                self.bouton_iteration.setStyleSheet("background-color: #FFA500; color: white; padding: 8px; border-radius: 5px;")

        except ValueError:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer des valeurs numériques valides pour les paramètres.")


    def call_perte_charge_page(self) :
        self.stacked_widget.setCurrentWidget(self.passes_results_page)
        self.valeur_renold

#===================================================================================================================
# Resultats finaux 
#===================================================================================================================

    def create_pertes_charge_page(self):
        """Créer la page des pertes de charge, du facteur de Colburn et du coût estimé."""
        page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # Titre principal
        title_label = QLabel("Calcul des Pertes de Charge et Facteur de Colburn")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        layout.addSpacing(40)

        # Section 1 : Pertes de charge côté calandre
        section1_layout = QVBoxLayout()
        section1_title = QLabel("Pertes de Charge Côté Calandre")
        section1_title.setFont(QFont("Arial", 13, QFont.Bold))
        section1_layout.addWidget(section1_title)

        self.label_Re_calandre = QLabel("Facteur de Colburn j = f(Re = ..., en % = 25.00)")
        self.label_Re_calandre.setFont(QFont("Arial", 11))
        self.label_Re_calandre.setAlignment(Qt.AlignCenter)
        section1_layout.addWidget(self.label_Re_calandre)

        form_layout1 = QGridLayout()
        form_layout1.addWidget(QLabel("Entrez le facteur de frottement j :"), 0, 0)
        self.input_j_calandre = QLineEdit()
        form_layout1.addWidget(self.input_j_calandre, 0, 1)

        self.result_DeltaP_calandre = QLabel("Pertes de charge côté calandre")
        self.result_DeltaP_calandre.setFont(QFont("Arial", 12, italic=True))
        self.result_DeltaP_calandre.setAlignment(Qt.AlignCenter)
        self.result_DeltaP_calandre.setStyleSheet("background-color: #f4f4f4; padding: 10px; border: 1px solid #ccc;")

        section1_layout.addLayout(form_layout1)
        section1_layout.addWidget(self.result_DeltaP_calandre)
        layout.addLayout(section1_layout)
        layout.addSpacing(40)

        # Section 2 : Facteur de Colburn et pertes de charge côté tubes
        section2_layout = QVBoxLayout()
        section2_title = QLabel("Facteur de Colburn et Pertes de Charge Côté Tubes")
        section2_title.setFont(QFont("Arial", 13, QFont.Bold))
        section2_layout.addWidget(section2_title)

        form_layout2 = QGridLayout()
        form_layout2.addWidget(QLabel("Entrez le facteur j (Colburn) :"), 0, 0)
        self.input_j_tubes = QLineEdit()
        form_layout2.addWidget(self.input_j_tubes, 0, 1)

        self.result_DeltaP_tubes = QLabel("Pertes de charge côté tubes")
        self.result_DeltaP_tubes.setFont(QFont("Arial", 12, italic=True))
        self.result_DeltaP_tubes.setAlignment(Qt.AlignCenter)
        self.result_DeltaP_tubes.setStyleSheet("background-color: #f4f4f4; padding: 10px; border: 1px solid #ccc;")

        section2_layout.addLayout(form_layout2)
        section2_layout.addWidget(self.result_DeltaP_tubes)
        layout.addLayout(section2_layout)
        layout.addSpacing(40)

        # Section 3 : Estimation du coût
        section3_layout = QVBoxLayout()
        section3_title = QLabel("Estimation du Coût de l'Échangeur de Chaleur")
        section3_title.setFont(QFont("Arial", 13, QFont.Bold))
        section3_layout.addWidget(section3_title)

        self.result_cout = QLabel("Coût estimé de l'échangeur de chaleur")
        self.result_cout.setFont(QFont("Arial", 12, QFont.Bold))
        self.result_cout.setAlignment(Qt.AlignCenter)
        self.result_cout.setStyleSheet("background-color: #f4f4f4; padding: 10px; border: 1px solid #ccc;")
        section3_layout.addWidget(self.result_cout)

        layout.addLayout(section3_layout)
        layout.addSpacing(40)

        # Boutons de validation et navigation
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        bouton_retour = QPushButton("Retour")
        bouton_retour.setFont(QFont("Arial", 12))
        bouton_retour.setStyleSheet("background-color: #f44336; color: white; padding: 8px; border-radius: 5px;")
        bouton_retour.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.coefficient_global_page))
        button_layout.addWidget(bouton_retour)

        self.bouton_calculer = QPushButton("Calculer")
        self.bouton_calculer.setFont(QFont("Arial", 12))
        self.bouton_calculer.setStyleSheet("background-color: #2196F3; color: white; padding: 8px; border-radius: 5px;")
        self.bouton_calculer.clicked.connect(self.calculer_pertes_et_cout)
        button_layout.addWidget(self.bouton_calculer)

        self.bouton_ajuster = QPushButton("Ajustements")
        self.bouton_ajuster.setFont(QFont("Arial", 12))
        self.bouton_ajuster.setStyleSheet("background-color: #bbbbbb; color: white; padding: 8px; border-radius: 5px;")
        self.bouton_ajuster.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.viscosity_dimensions_page))
        self.bouton_ajuster.setEnabled(False)
        button_layout.addWidget(self.bouton_ajuster)

        self.bouton_suivant = QPushButton("Synthèse Finale")
        self.bouton_suivant.setFont(QFont("Arial", 12))
        self.bouton_suivant.setStyleSheet("background-color: #bbbbbb; color: white; padding: 8px; border-radius: 5px;")
        self.bouton_suivant.setEnabled(False)
        self.bouton_suivant.clicked.connect(self.call_synthese_page)
        
        
        button_layout.addWidget(self.bouton_suivant)

        button_layout.addStretch()
        layout.addLayout(button_layout)
        page.setLayout(layout)

        return page


    def calculer_pertes_et_cout(self):
        """Calculer les pertes de charge et le coût estimé de l’échangeur de chaleur."""
        try:
            # Récupération des entrées utilisateur
            j_calandre = float(self.input_j_calandre.text())
            j_tubes = float(self.input_j_tubes.text())

            # Récupération des données nécessaires depuis self.data
            S0 = self.data["passes_results"]["S0"]
            fluide_chaud = self.data["fluide_chaud"]
            fluide_froid = self.data["fluide_froid"]
            results_tubes = self.data["results_tubes"]
            results_calandre = self.data["results_calandre"]
            dimensions = self.data["dimensions_tubes"]

            # Calcul des pertes de charge
            DeltaP_calandre = calculations.calcul_pertes_charge_calandre(
                fluide_froid["props"]["rho"], fluide_froid["props"]["mu"], self.data["viscosities"]["froid"],
                results_calandre["d_eq"], dimensions["longueur"], results_calandre["u_eq"],
                results_calandre["Re"], results_tubes["l_c0"], results_tubes["D_v0"], j_calandre
            )

            DeltaP_tubes = calculations.calcul_pertes_charge_cote_tubes(
                fluide_chaud["props"]["rho"], fluide_chaud["props"]["mu"], self.data["viscosities"]["chaud"],
                dimensions["d_int"], dimensions["longueur"], results_tubes["u1"],
                results_tubes["Re"], self.data["passes_results"]["passes"], j_tubes
            )

            # Calcul du coût estimé
            cout_estime = calculations.estimation_cout_echangeur(S0)

            # Mise à jour des résultats affichés
            self.result_DeltaP_calandre.setText(f"Pertes de charge côté calandre : {DeltaP_calandre:.4f} Pa")
            self.result_DeltaP_tubes.setText(f"Pertes de charge côté tubes : {DeltaP_tubes:.4f} Pa")
            self.result_cout.setText(f"Coût estimé de l'échangeur de chaleur : {cout_estime:.2f} USD")

            # Enregistrement des résultats dans self.data
            self.data["pertes_charge"] = {
                "j_calandre": j_calandre,
                "j_tubes": j_tubes,
                "DeltaP_calandre": DeltaP_calandre,
                "DeltaP_tubes": DeltaP_tubes,
                "cout_estime": cout_estime
            }

            # Activation du bouton "Synthèse Finale"
            self.bouton_suivant.setEnabled(True)
            self.bouton_suivant.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px; border-radius: 5px;")
            self.bouton_ajuster.setEnabled(True)
            self.bouton_ajuster.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px; border-radius: 5px;")

        except ValueError:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer des valeurs numériques valides pour les facteurs de Colburn.")
        except KeyError as e:
            QMessageBox.warning(self, "Erreur", f"Données manquantes pour les calculs : {e}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur inattendue est survenue : {e}")


    def call_synthese_page(self):
        """Passer à la page suivante (Page Synthèse) depuis la page de calcul des Pertes et Coût."""
        self.update_synthese_results()
        self.stacked_widget.setCurrentWidget(self.synthese_page)

    def valeur_renold(self):
        self.label_Re_calandre.setText(f"Facteur de Colburn j = f(Re = {self.data["results_tubes"]["Re"]:.2f}, en % = 25.00)")


#===================================================================================================================
# Synthèse finale
#===================================================================================================================


    def create_synthese_page(self):
        """Créer la page de synthèse des résultats."""
        page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # Titre principal
        title_label = QLabel("Synthèse des Résultats de l'Échangeur de Chaleur")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        layout.addSpacing(20)

        # Zone d'affichage des résultats
        self.result_summary = QTextEdit()
        self.result_summary.setReadOnly(True)
        self.result_summary.setFont(QFont("Courier", 12))
        self.result_summary.setStyleSheet("background-color: #f4f4f4; padding: 10px; border: 1px solid #ccc;")
        layout.addWidget(self.result_summary)

        # Boutons d'exportation
        export_layout = QHBoxLayout()
        self.bouton_export_pdf = QPushButton("Exporter en PDF")
        self.bouton_export_pdf.setFont(QFont("Arial", 12))
        self.bouton_export_pdf.setStyleSheet("background-color: #2196F3; color: white; padding: 8px; border-radius: 5px;")
        self.bouton_export_pdf.clicked.connect(self.export_to_pdf)
        export_layout.addWidget(self.bouton_export_pdf)

        self.bouton_export_txt = QPushButton("Exporter en Texte")
        self.bouton_export_txt.setFont(QFont("Arial", 12))
        self.bouton_export_txt.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px; border-radius: 5px;")
        self.bouton_export_txt.clicked.connect(self.export_to_txt)
        export_layout.addWidget(self.bouton_export_txt)

        layout.addLayout(export_layout)
        layout.addSpacing(20)

        # Boutons de navigation
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        bouton_retour = QPushButton("Retour")
        bouton_retour.setFont(QFont("Arial", 12))
        bouton_retour.setStyleSheet("background-color: #f44336; color: white; padding: 8px; border-radius: 5px;")
        bouton_retour.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.pertes_charge_page))
        button_layout.addWidget(bouton_retour)

        bouton_terminer = QPushButton("Terminer")
        bouton_terminer.setFont(QFont("Arial", 12))
        bouton_terminer.setStyleSheet("background-color: #FF9800; color: white; padding: 8px; border-radius: 5px;")
        bouton_terminer.clicked.connect(self.close)
        button_layout.addWidget(bouton_terminer)

        button_layout.addStretch()
        layout.addLayout(button_layout)
        page.setLayout(layout)

        return page


    def update_synthese_results(self):
        """Mettre à jour la synthèse des résultats."""
        try:
            fluide_chaud = self.data["fluide_chaud"]
            fluide_froid = self.data["fluide_froid"]
            passes_results = self.data["passes_results"]
            results_tubes = self.data["results_tubes"]
            results_calandre = self.data["results_calandre"]
            coefficient_global = self.data["coefficient_global"]
            pertes_charge = self.data["pertes_charge"]

            # Création du texte de synthèse
            synthese_text = f"""
=== Données des Fluides ===
Fluide Chaud : {fluide_chaud["type"]}
T_in : {fluide_chaud["T_in_chaud"]} °C | T_out : {fluide_chaud["T_out_chaud"]} °C
Débit massique : {fluide_chaud["debit_chaud"]} kg/s

Fluide Froid : {fluide_froid["type"]}
T_in : {fluide_froid["T_in_froid"]} °C | T_out : {fluide_froid["T_out_froid"]} °C
Débit massique : {fluide_froid["debit_froid"]} kg/s

=== Résultats Thermiques ===
NTU : {passes_results["NTU"]:.4f}
Rendement : {passes_results["eta"]:.2%}
Surface d'échange thermique : {passes_results["S0"]:.2f} m²

=== Paramètres des Tubes ===
Re : {results_tubes["Re"]:.2f}
Nu : {results_tubes["Nu"]:.4f}
Coefficient de convection : {results_tubes["h1"]:.2f} W/m².K

=== Paramètres de la Calandre ===
Re : {results_calandre["Re"]:.2f}
Nu : {results_calandre["Nu"]:.4f}
Coefficient de convection : {results_calandre["h2"]:.2f} W/m².K

=== Coefficient Global d'Échange ===
U_glob : {coefficient_global["U_glob"]:.2f} W/m².K
Marge d'erreur : {coefficient_global["marge"]:.2%}

=== Pertes de Charge et Coût ===
ΔP Tubes : {pertes_charge["DeltaP_tubes"]:.2f} Pa
ΔP Calandre : {pertes_charge["DeltaP_calandre"]:.2f} Pa
Coût estimé : {pertes_charge["cout_estime"]:.2f} USD
    """

            # Mettre à jour la zone d'affichage
            print("Texte généré pour la synthèse :\n", synthese_text) 
            self.result_summary.setPlainText(synthese_text)

        except KeyError as e:
            QMessageBox.warning(self, "Erreur", f"Données manquantes pour la synthèse : {e}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur inattendue est survenue : {e}")


    def export_to_txt(self):
        """Exporter les résultats en fichier texte."""
        try:
            file_path, _ = QFileDialog.getSaveFileName(self, "Exporter en fichier texte", "", "Fichiers texte (*.txt)")
            if file_path:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.result_summary.toPlainText())
                QMessageBox.information(self, "Succès", "Les résultats ont été exportés avec succès.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue lors de l'exportation : {e}")


    def export_to_pdf(self):
        """Exporter les résultats en PDF."""
        try:
            file_path, _ = QFileDialog.getSaveFileName(self, "Exporter en PDF", "", "Fichiers PDF (*.pdf)")
            if file_path:
                pdf = FPDF()
                pdf.add_page()

                # Chemin vers le dossier config/ relatif au fichier main.py
                base_dir = os.path.dirname(os.path.abspath(__file__))
                font_dir = os.path.join(base_dir, "config")

                font_path = os.path.join(font_dir, "DejaVuSans.ttf")
                font_bold_path = os.path.join(font_dir, "DejaVuSans-Bold.ttf")

                # Vérifier que les fichiers de police existent
                if not os.path.exists(font_path):
                    QMessageBox.warning(self, "Erreur", f"Police introuvable : {font_path}\nPlacez le fichier DejaVuSans.ttf dans le dossier config/.")
                    return

                pdf.add_font("DejaVu", "", font_path, uni=True)
                if os.path.exists(font_bold_path):
                    pdf.add_font("DejaVu", "B", font_bold_path, uni=True)

                pdf.set_font("DejaVu", "", 12)
                for line in self.result_summary.toPlainText().split("\n"):
                    pdf.cell(200, 10, txt=line, ln=True, align='L')
                pdf.output(file_path)
                QMessageBox.information(self, "Succès", "Les résultats ont été exportés avec succès en PDF.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue lors de l'exportation : {e}")


#===================================================================================================================
# 
#===================================================================================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

