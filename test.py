import customtkinter as ctk
from tkinter import messagebox
from conversions import convertir, GRANDEURS, TEMPERATURE
import json
import os
import webbrowser
from datetime import datetime
import csv

class ConvertisseurApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌟 Super Convertisseur Universel 🌟")
        self.root.geometry("750x550")
        
        # Configuration initiale
        self.setup_dossiers()
        self.charger_config()
        
        # Emojis pour chaque grandeur
        self.grandeur_emojis = {
            "longueur": "📏",
            "masse": "⚖️",
            "temps": "⏱️",
            "volume": "🧪",
            "surface": "📐",
            "vitesse": "🚗",
            "temperature": "🌡️",
            "devise": "💵",
            "donnees": "💾",
            "intensite_electrique": "⚡",
            "intensite_lumineuse": "💡",
            "quantite_matiere": "🧪"
        }
        
        # Variables
        self.grandeurs = list(GRANDEURS.keys()) + ["temperature"]
        self.unites = {}
        self.historique = []
        
        # Interface
        self.setup_ui()
        self.changer_theme_customtkinter()
        
        # Démarrer avec une grandeur commune (longueur)
        self.grandeur_combobox.set("📏 longueur")
        self.update_unites()
        
    def setup_dossiers(self):
        """Crée le dossier data si inexistant"""
        if not os.path.exists("data"):
            os.makedirs("data")
    
    def charger_config(self):
        """Charge la configuration ou crée un fichier par défaut"""
        self.config = {
            "theme": "light",
            "couleur": "blue",
            "historique": [],
            "unite_preferees": {}
        }
        
        try:
            with open("data/config.json", "r") as f:
                loaded_config = json.load(f)
                self.config.update(loaded_config)
        except (FileNotFoundError, json.JSONDecodeError):
            self.sauvegarder_config()
    
    def sauvegarder_config(self):
        """Sauvegarde la configuration"""
        with open("data/config.json", "w") as f:
            json.dump(self.config, f, indent=4)
    
    def setup_ui(self):
        """Construit l'interface avec CustomTkinter"""
        # Configuration du grid principal
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Frame principale avec onglets
        self.tabview = ctk.CTkTabview(self.root)
        self.tabview.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Création des onglets
        self.tabview.add("Conversion")  # Onglet 1
        self.tabview.add("Calculatrice")  # Onglet 2
        self.tabview.add("Historique")  # Onglet 3
        self.tabview.add("Aide")  # Onglet 4
        
        # Onglet Conversion
        self.setup_onglet_conversion()
        
        # Onglet Calculatrice
        self.setup_onglet_calculatrice()
        
        # Onglet Historique
        self.setup_onglet_historique()
        
        # Onglet Aide
        self.setup_onglet_aide()
        
        # Barre de statut
        self.setup_barre_statut()
        
        # Configuration du redimensionnement
        self.root.minsize(750, 550)

    def setup_onglet_conversion(self):
        """Configure l'onglet de conversion"""
        tab = self.tabview.tab("Conversion")
        
        # Contrôles supérieurs
        top_frame = ctk.CTkFrame(tab)
        top_frame.pack(fill="x", pady=5)
        
        # Sélecteur de thème
        self.theme_switch = ctk.CTkSwitch(
            top_frame, 
            text="Mode Sombre",
            command=self.changer_theme_customtkinter
        )
        self.theme_switch.pack(side="left", padx=5)
        if self.config["theme"] == "dark":
            self.theme_switch.select()
        
        # Frame de conversion
        conv_frame = ctk.CTkFrame(tab)
        conv_frame.pack(fill="both", expand=True, pady=10)
        
        # Grandeur avec emoji
        grandeur_frame = ctk.CTkFrame(conv_frame)
        grandeur_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(grandeur_frame, text="Type de grandeur:").pack(side="left")
        self.grandeur_combobox = ctk.CTkComboBox(
            grandeur_frame, 
            values=[f"{self.grandeur_emojis.get(g, '📊')} {g}" for g in self.grandeurs],
            command=self.update_unites
        )
        self.grandeur_combobox.pack(side="left", padx=10, fill="x", expand=True)
        
        # Valeur
        valeur_frame = ctk.CTkFrame(conv_frame)
        valeur_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(valeur_frame, text="Valeur:").pack(side="left")
        self.valeur_entry = ctk.CTkEntry(valeur_frame)
        self.valeur_entry.pack(side="left", padx=10, fill="x", expand=True)
        
        # Unités
        unites_frame = ctk.CTkFrame(conv_frame)
        unites_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(unites_frame, text="De:").pack(side="left")
        self.unite_source_combobox = ctk.CTkComboBox(unites_frame)
        self.unite_source_combobox.pack(side="left", padx=10, fill="x", expand=True)
        
        ctk.CTkLabel(unites_frame, text="À:").pack(side="left")
        self.unite_cible_combobox = ctk.CTkComboBox(unites_frame)
        self.unite_cible_combobox.pack(side="left", padx=10, fill="x", expand=True)
        
        # Bouton de conversion
        ctk.CTkButton(
            conv_frame, 
            text="🚀 Convertir", 
            command=self.convertir,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(fill="x", pady=10)
        
        # Résultat
        self.resultat_var = ctk.StringVar(value="Résultat apparaîtra ici")
        resultat_label = ctk.CTkLabel(
            conv_frame, 
            textvariable=self.resultat_var,
            font=ctk.CTkFont(size=14, weight="bold"),
            wraplength=550
        )
        resultat_label.pack(fill="x", pady=10)
    
    def setup_onglet_calculatrice(self):
        """Configure l'onglet calculatrice avancée"""
        tab = self.tabview.tab("Calculatrice")
        
        # Zone d'expression
        ctk.CTkLabel(tab, text="Entrez une expression avec unités:").pack(pady=5)
        
        self.calc_entry = ctk.CTkEntry(
            tab, 
            placeholder_text="Ex: 2 km + 300 m - 0.5 mile",
            font=ctk.CTkFont(size=14)
        )
        self.calc_entry.pack(fill="x", pady=5, padx=10)
        
        # Boutons de calcul
        btn_frame = ctk.CTkFrame(tab)
        btn_frame.pack(fill="x", pady=5)
        
        ctk.CTkButton(
            btn_frame, 
            text="🧮 Calculer", 
            command=self.calculer_complexe
        ).pack(side="left", padx=5, fill="x", expand=True)
        
        ctk.CTkButton(
            btn_frame, 
            text="📊 Convertir le résultat en:", 
            command=self.convertir_resultat
        ).pack(side="left", padx=5, fill="x", expand=True)
        
        self.unite_resultat_combobox = ctk.CTkComboBox(btn_frame)
        self.unite_resultat_combobox.pack(side="left", padx=5, fill="x", expand=True)
        
        # Résultat
        self.calc_resultat_var = ctk.StringVar(value="Résultat apparaîtra ici")
        ctk.CTkLabel(
            tab, 
            textvariable=self.calc_resultat_var,
            font=ctk.CTkFont(size=14, weight="bold"),
            wraplength=550
        ).pack(fill="x", pady=10)
        
        # Exemples
        exemples_frame = ctk.CTkFrame(tab)
        exemples_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(exemples_frame, text="Exemples:").pack(anchor="w")
        exemples = [
            "2h30min + 45min → 3.25 h",
            "500 g × 10 → 5 kg",
            "1 m² + 500 cm² → 1.05 m²"
        ]
        for ex in exemples:
            ctk.CTkLabel(exemples_frame, text=ex, font=ctk.CTkFont(size=12)).pack(anchor="w")
    
    def setup_onglet_historique(self):
        """Configure l'onglet historique"""
        tab = self.tabview.tab("Historique")
        
        # Barre d'outils
        toolbar_frame = ctk.CTkFrame(tab)
        toolbar_frame.pack(fill="x", pady=5)
        
        ctk.CTkButton(
            toolbar_frame, 
            text="🗑️ Effacer l'historique", 
            command=self.effacer_historique
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            toolbar_frame, 
            text="💾 Exporter en CSV", 
            command=self.exporter_historique
        ).pack(side="left", padx=5)
        
        # Liste d'historique
        self.histoire_text = ctk.CTkTextbox(
            tab, 
            wrap="word",
            font=ctk.CTkFont(family="Courier", size=12)
        )
        self.histoire_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.histoire_text.insert("1.0", "Historique des conversions:\n\n")
        self.histoire_text.configure(state="disabled")
        
        # Charger l'historique existant
        self.actualiser_affichage_historique()
    def setup_onglet_aide(self):
        """Configure l'onglet d'aide et informations"""
        tab = self.tabview.tab("Aide")
        
        # Logo et titre
        title_frame = ctk.CTkFrame(tab, fg_color="transparent")
        title_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            title_frame, 
            text="🌟 Super Convertisseur Universel 🌟", 
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack()
        
        # Description
        desc_frame = ctk.CTkFrame(tab, fg_color="transparent")
        desc_frame.pack(fill="x", pady=10)
        
        features = [
            "✅ Conversion entre toutes les unités standards",
            "✅ Prise en charge de la température (Celsius, Fahrenheit, Kelvin)",
            "✅ Calculs complexes avec unités hétérogènes",
            "✅ Interface moderne et personnalisable",
            "✅ Historique complet des conversions",
            "✅ Export des données en CSV"
        ]
        
        for feat in features:
            ctk.CTkLabel(desc_frame, text=feat).pack(anchor="w", pady=2)
        
        # Boutons importants
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.pack(fill="x", pady=20)
        
        ctk.CTkButton(
            btn_frame, 
            text="📚 Documentation", 
            command=lambda: webbrowser.open("file://" + os.path.abspath("documentation.html"))  # Modifié pour ouvrir un fichier local
        ).pack(side="left", padx=10, fill="x", expand=True)
        
        ctk.CTkButton(
            btn_frame, 
            text="🐞 Signaler un bug", 
            command=lambda: webbrowser.open("https://wa.me/237699490748")  # Remplacez 1234567890 par votre numéro WhatsApp
        ).pack(side="left", padx=10, fill="x", expand=True)

    def setup_barre_statut(self):
        """Configure la barre de statut en bas de la fenêtre"""
        self.statut_var = ctk.StringVar(value="Prêt")
        
        statut_frame = ctk.CTkFrame(self.root, height=25)
        statut_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        ctk.CTkLabel(
            statut_frame, 
            textvariable=self.statut_var,
            font=ctk.CTkFont(size=12)
        ).pack(side="left", padx=10)
        
        ctk.CTkLabel(
            statut_frame, 
            text=f"v1.0 • {datetime.now().year}",
            font=ctk.CTkFont(size=12)
        ).pack(side="right", padx=10)
    
    def changer_theme_customtkinter(self):
        """Change le thème avec CustomTkinter"""
        theme = "dark" if self.theme_switch.get() == 1 else "light"
        self.config["theme"] = theme
        self.sauvegarder_config()
        ctk.set_appearance_mode(theme)
    
    def update_unites(self, event=None):
        """Met à jour les unités disponibles"""
        # Extraire le nom de grandeur sans l'emoji
        grandeur_full = self.grandeur_combobox.get()
        grandeur = grandeur_full.split(" ")[1] if " " in grandeur_full else grandeur_full
        
        if grandeur == "temperature":
            unites = list(TEMPERATURE.keys())
        elif grandeur in GRANDEURS:
            unites = list(GRANDEURS[grandeur].keys())
        else:
            unites = []
        
        self.unite_source_combobox.configure(values=unites)
        self.unite_cible_combobox.configure(values=unites)
        self.unite_resultat_combobox.configure(values=unites)
        
        if unites:
            self.unite_source_combobox.set(unites[0])
            self.unite_cible_combobox.set(unites[1] if len(unites) > 1 else unites[0])
            self.unite_resultat_combobox.set(unites[0])
        
        self.statut_var.set(f"Unités de {grandeur} chargées")
    
    def convertir(self):
        """Effectue une conversion simple"""
        try:
            # Extraire le nom de grandeur sans l'emoji
            grandeur_full = self.grandeur_combobox.get()
            grandeur = grandeur_full.split(" ")[1] if " " in grandeur_full else grandeur_full
            
            valeur = float(self.valeur_entry.get())
            unite_source = self.unite_source_combobox.get()
            unite_cible = self.unite_cible_combobox.get()
            
            resultat = convertir(valeur, unite_source, unite_cible, grandeur)
            texte_resultat = f"{valeur} {unite_source} = {resultat:.6g} {unite_cible}"
            
            self.resultat_var.set(texte_resultat)
            self.ajouter_historique(texte_resultat)
            self.statut_var.set("Conversion réussie!")
            
        except ValueError as e:
            messagebox.showerror("Erreur", f"Données invalides: {str(e)}")
            self.statut_var.set("Erreur: données invalides")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")
            self.statut_var.set(f"Erreur: {str(e)}")
    
    def calculer_complexe(self):
        """Effectue un calcul complexe avec unités"""
        try:
            expression = self.calc_entry.get()
            grandeur_full = self.grandeur_combobox.get()
            grandeur = grandeur_full.split(" ")[1] if " " in grandeur_full else grandeur_full
            
            # Implémentation simplifiée - devrait utiliser un vrai parser
            if "+" in expression:
                parties = expression.split("+")
                val1, unite1 = parties[0].strip().split()
                val2, unite2 = parties[1].strip().split()
                
                # Convertir tout dans la première unité
                val2_conv = convertir(float(val2), unite2, unite1, grandeur)
                total = float(val1) + val2_conv
                
                texte_resultat = f"{expression} = {total:.6g} {unite1}"
                self.calc_resultat_var.set(texte_resultat)
                self.ajouter_historique(f"Calcul: {texte_resultat}")
                self.statut_var.set("Calcul réussi!")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Expression invalide: {str(e)}")
            self.statut_var.set("Erreur dans le calcul")
    
    def convertir_resultat(self):
        """Convertit le résultat précédent dans une autre unité"""
        try:
            unite_cible = self.unite_resultat_combobox.get()
            grandeur_full = self.grandeur_combobox.get()
            grandeur = grandeur_full.split(" ")[1] if " " in grandeur_full else grandeur_full
            
            # Implémentation simplifiée - devrait parser le résultat précédent
            if "=" in self.calc_resultat_var.get():
                valeur, unite_source = self.calc_resultat_var.get().split("=")[1].strip().split()
                valeur = float(valeur)
                
                resultat = convertir(valeur, unite_source, unite_cible, grandeur)
                texte_resultat = f"{valeur} {unite_source} = {resultat:.6g} {unite_cible}"
                self.calc_resultat_var.set(texte_resultat)
                self.ajouter_historique(f"Conversion: {texte_resultat}")
                self.statut_var.set("Résultat converti")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de convertir: {str(e)}")
            self.statut_var.set("Erreur de conversion")
    
    def ajouter_historique(self, texte):
        """Ajoute une entrée à l'historique"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entree = f"[{timestamp}] {texte}"
        
        self.historique.append(entree)
        self.config["historique"] = self.historique[-50:]  # Garde 50 entrées
        self.sauvegarder_config()
        self.actualiser_affichage_historique()
    
    def actualiser_affichage_historique(self):
        """Met à jour l'affichage de l'historique"""
        self.histoire_text.configure(state="normal")
        self.histoire_text.delete("1.0", "end")
        self.histoire_text.insert("1.0", "Historique des conversions:\n\n")
        
        for entree in reversed(self.config["historique"]):
            self.histoire_text.insert("end", entree + "\n")
        
        self.histoire_text.configure(state="disabled")
    
    def effacer_historique(self):
        """Efface tout l'historique"""
        if messagebox.askyesno("Confirmer", "Voulez-vous vraiment effacer tout l'historique?"):
            self.historique = []
            self.config["historique"] = []
            self.sauvegarder_config()
            self.actualiser_affichage_historique()
            self.statut_var.set("Historique effacé")
    
    def exporter_historique(self):
        """Exporte l'historique en CSV"""
        try:
            with open("data/historique_conversions.csv", "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(["Date", "Heure", "Conversion"])
                for entree in self.historique:
                    # Format: "[2023-01-01 12:00:00] 1 km = 0,621371 mile"
                    parts = entree.split("] ")
                    date_heure = parts[0][1:]
                    conversion = parts[1]
                    date, heure = date_heure.split(" ")
                    writer.writerow([date, heure, conversion])
            
            messagebox.showinfo("Succès", "Historique exporté dans data/historique_conversions.csv")
            self.statut_var.set("Historique exporté en CSV")
            
            # Ouvrir le dossier contenant le fichier (Windows)
            if os.name == 'nt':
                os.startfile("data")
            # Pour Mac/Linux, vous pourriez utiliser:
            # subprocess.run(["open", "data"])  # Mac
            # ou subprocess.run(["xdg-open", "data"])  # Linux
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec de l'export: {str(e)}")
            self.statut_var.set("Erreur lors de l'export")
    
  

if __name__ == "__main__":
    ctk.set_appearance_mode("system")
    root = ctk.CTk()
    app = ConvertisseurApp(root)
    root.mainloop()