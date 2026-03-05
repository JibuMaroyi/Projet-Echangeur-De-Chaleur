from CoolProp.CoolProp import PropsSI

def choisir_fluide(choix):
    """
    Permet de sélectionner un fluide parmi les options disponibles.

    :param choix: Numéro correspondant au fluide choisi (1, 2 ou 3).
    :return: Nom du fluide sélectionné.
    """
    options = {"1": "air", "2": "eau", "3": "huile lubrifiant"}
    return options.get(str(choix), None)

def obtenir_proprietes(fluide, temperature, pression):
    """
    Récupère les propriétés thermophysiques d'un fluide donné à une température et pression spécifiques.
    Si le fluide est "huile lubrifiant", les propriétés doivent être fournies manuellement.

    :param fluide: Nom du fluide ("air", "eau", ou "huile lubrifiant").
    :param temperature: Température en Kelvin.
    :param pression: Pression en Pascal.
    :return: Dictionnaire des propriétés thermophysiques ou None en cas d'erreur.
    """
    temperature = temperature + 273.15
    FLUIDE_MAP = {
        "air": "Air",
        "eau": "Water",
    }
    try:
        return {
            "cp": PropsSI("C", "T", temperature, "P", pression, FLUIDE_MAP[fluide]),
            "k": PropsSI("L", "T", temperature, "P", pression, FLUIDE_MAP[fluide]),
            "Pr": PropsSI("PRANDTL", "T", temperature, "P", pression, FLUIDE_MAP[fluide]),
            "rho": PropsSI("D", "T", temperature, "P", pression, FLUIDE_MAP[fluide]),
            "mu": PropsSI("V", "T", temperature, "P", pression, FLUIDE_MAP[fluide])
        }
    except Exception as e:
        print(f"Erreur lors de l'obtention des propriétés pour {fluide} à {temperature} K et {pression} Pa : {e}")
        return None

def entrer_donnees_fluide(T_in, T_out, pression, flow_rate):
    """
    Structure les données pour un fluide donné.

    :param T_in: Température d'entrée (°C).
    :param T_out: Température de sortie (°C).
    :param pression: Pression (Pa).
    :param flow_rate: Débit massique (kg/s).
    :return: Dictionnaire des données saisies pour le fluide.
    """
    T_moy = (T_in + T_out) / 2
    return {"T_in": T_in, "T_out": T_out, "pression": pression, "flow_rate": flow_rate, "T_moy": T_moy}

