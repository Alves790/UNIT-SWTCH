"""
Ce fichier contient tous les facteurs de conversion pour les 7 grandeurs du SI.
Les valaeurs sont basées sur le système métrique et les unités courantes.
"""
# Facteur de conversion par rapport à l'unité SI de reférence
LONGUEUR = {
    # Unités SI (l'unité de reférence est le m)
    "m" : 1,
    "km" : 1000,
    "dm" : 0.1,
    "cm" : 0.01,
    "mm" : 0.001,
    "µm" : 1e-6,
    "nm" : 1e-9,
    "m" : 1,
    # Unités non SI
    "pouce" : 0.0254,
    "pied" : 0.3048,
    "mile" : 1609.34,
    "yard" : 0.9144
}

MASSE = {
    # Unités SI (l'unité de reférence est le Kg)
    "kg" : 1,
    "g" : 0.001,
    "mg" : 1e-6,
    "µg" : 1e-9,
    "tonne" : 1000,
    # Unités non SI
    "livre" : 0.453592,
    "once" : 0.283495
}

TEMPS = {
    # Unités SI
    "s" : 1,
    "ms" : 0.001,
    "µs" : 1e-6,
    "ns" : 1e-9,
    # Unités non SI
    "min" : 60,
    "h" : 3600,
    "jour" : 86400,
    "an" : 313536000 #Pour une année non bissextile.
}

INTENSITE_ELECTRIQUE = {
    # Unités SI
    "A" : 1,
    "mA" : 0.001,
    "kA" : 1000,
    "µA" : 1e-6
}

TEMPERATURE = {
    # Unités possibles et formules de conversion en fonction de K(supposée de reférence)
    "K" : {
        "vers_K": lambda x: x,
        "depuis_K": lambda x: x
    },
    "°C" : {
        "vers_K": lambda c: c + 273.15,
        "depuis_K": lambda k: k - 273.15
    },
    "°F" : {
        "vers_K": lambda f: (f - 32) * 5/9 + 273.15,
        "depuis_K": lambda k: (k - 273.15) * 9/5 + 32
    }
}

INTENSITE_LUMINEUSE = {
    # Unités SI
    "cd" : 1,
    "mcd" : 0.001,
    "kcd" : 1000,
}

QUANTITE_MATIERE = {
    # Unités SI
    "mol" : 1,
    "mmmol" : 0.001,
    "kmol" : 1000
}

# Dictionnaire principal pour accéder aux grandeurs
GRANDEURS = {
    "longueur" : LONGUEUR,
    "masse" : MASSE,
    "temps" : TEMPS,
    "intensite_electrique" : INTENSITE_ELECTRIQUE,
    "temperature" : TEMPERATURE,
    "intensite_lumineuse" : INTENSITE_LUMINEUSE,
    "quantite_matiere" : QUANTITE_MATIERE,
}