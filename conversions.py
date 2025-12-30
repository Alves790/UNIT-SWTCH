from constantes import GRANDEURS, TEMPERATURE

def convertir(valeur, unite_source, unite_cible, grandeur):
    """
    Convertit une valeur d'une unité à une autre pour une grandeur donnée.
    Gère automatiquement le cas particulier de la température.
    
    Args:
        valeur (float): Valeur à convertir
        unite_source (str): Unité de départ
        unite_cible (str): Unité cible
        grandeur (str): Type de grandeur physique
        
    Returns:
        float: Valeur convertie
    """
    # Vérification des unités valides
    if grandeur not in GRANDEURS and grandeur != "temperature":
        raise ValueError(f"Grandeur inconnue : {grandeur}")
    
    if grandeur == "temperature":
        return convertir_temperature(valeur, unite_source, unite_cible)
    else:
        return convertir_standard(valeur, unite_source, unite_cible, grandeur)

def convertir_standard(valeur, unite_source, unite_cible, grandeur):
    """
    Conversion standard pour les grandeurs utilisant des facteurs multiplicatifs.
    """
    facteurs = GRANDEURS[grandeur]
    
    # Vérification des unités existantes
    if unite_source not in facteurs:
        raise ValueError(f"Unité source inconnue pour {grandeur}: {unite_source}")
    if unite_cible not in facteurs:
        raise ValueError(f"Unité cible inconnue pour {grandeur}: {unite_cible}")
    
    return valeur * facteurs[unite_source] / facteurs[unite_cible]

def convertir_temperature(valeur, unite_source, unite_cible):
    """
    Conversion spéciale pour la température entre K, °C et °F.
    """
    if unite_source not in TEMPERATURE:
        raise ValueError(f"Unité source température inconnue: {unite_source}")
    if unite_cible not in TEMPERATURE:
        raise ValueError(f"Unité cible température inconnue: {unite_cible}")
    
    # Conversion via Kelvin (unité SI)
    kelvin = TEMPERATURE[unite_source]["vers_K"](valeur)
    return round(TEMPERATURE[unite_cible]["depuis_K"](kelvin), 2)

# Fonctions pratiques pour chaque grandeur
def convertir_longueur(valeur, unite_source, unite_cible):
    return convertir(valeur, unite_source, unite_cible, "longueur")

def convertir_masse(valeur, unite_source, unite_cible):
    return convertir(valeur, unite_source, unite_cible, "masse")

def convertir_temps(valeur, unite_source, unite_cible):
    return convertir(valeur, unite_source, unite_cible, "temps")

def convertir_intensite_electrique(valeur, unite_source, unite_cible):
    return convertir(valeur, unite_source, unite_cible, "intensite_electrique")

def convertir_intensite_lumineuse(valeur, unite_source, unite_cible):
    return convertir(valeur, unite_source, unite_cible, "intensite_lumineuse")

def convertir_quantite_matiere(valeur, unite_source, unite_cible):
    return convertir(valeur, unite_source, unite_cible, "quantite_matiere")

