import math

def calculer_debit_calorifique(flow_rate, cp):
    """
    Calcule le débit calorifique pour un fluide donné.

    :param flow_rate: Débit massique (kg/s).
    :param cp: Capacité calorifique spécifique (J/kg.K).
    :return: Débit calorifique (W).
    """
    return flow_rate * cp

def calculer_rendement(C_chaud, C_froid, T_in_chaud, T_out_chaud, T_in_froid, T_out_froid):
    """
    Compare les débits calorifiques des fluides chaud et froid pour calculer le rendement.

    :param C_chaud: Débit calorifique du fluide chaud (W).
    :param C_froid: Débit calorifique du fluide froid (W).
    :param T_in_chaud: Température d'entrée du fluide chaud (°C).
    :param T_out_chaud: Température de sortie du fluide chaud (°C).
    :param T_in_froid: Température d'entrée du fluide froid (°C).
    :param T_out_froid: Température de sortie du fluide froid (°C).
    :return: (rendement, condition).
    """
    if C_chaud < C_froid:
        eta = (T_in_chaud - T_out_chaud) / (T_in_chaud - T_in_froid)
        condition_eta = "C_chaud < C_froid"
    else:
        eta = (T_out_froid - T_in_froid) / (T_in_chaud - T_in_froid)
        condition_eta = "C_froid < C_chaud"
    return eta, condition_eta

def calculer_rapport_Z(C_chaud, C_froid):
    """
    Calcule le rapport Z entre les débits calorifiques minimum et maximum.

    :param C_chaud: Débit calorifique du fluide chaud (W).
    :param C_froid: Débit calorifique du fluide froid (W).
    :return: Rapport Z (sans unité).
    """
    return min(C_chaud, C_froid) / max(C_chaud, C_froid)

def calculer_surface_echange(NTU, C_min, Uo_supp):
    """
    Calcule la surface d'échange thermique.

    :param NTU: Nombre d'unités de transfert thermique (sans unité).
    :param C_min: Capacité calorifique minimale (W/K).
    :param Uo_supp: Coefficient d'échange thermique supposé (W/m².K).
    :return: Surface d'échange thermique (m²).
    """
    return NTU * C_min / Uo_supp


def calculer_NTU(eta, Z, passe):
    """
    Calcule le nombre d'unités de transfert (NTU).

    :param eta: Rendement (sans unité).
    :param Z: Rapport des capacités calorifiques (sans unité).
    :param passe: Type de passe (1 pour 1->1, 2 pour 1->2).
    :return: NTU (sans unité).
    """
    try:
        if passe == 1:
            if Z < 1:
                NTU = (1 / (Z - 1)) * math.log((eta - 1) / (eta * Z - 1))
            else:
                NTU = eta / (1 - eta)
        elif passe == 2:
            E = (2 / eta - (1 + Z)) / math.sqrt(1 + Z**2)
            NTU = -(1 + Z**2)**(-1/2) * math.log((E - 1) / (E + 1))
        else:
            raise ValueError("Type de passe invalide. Utilisez 1 pour 1->1 ou 2 pour 1->2.")
        return NTU
    except ValueError:
        return None



def calculer_temperature_paroi(T_m1, T_m2):
    """
    Calcule la température moyenne de la paroi.

    :param T_m1: Température moyenne du fluide chaud (°C).
    :param T_m2: Température moyenne du fluide froid (°C).
    :return: Température moyenne de la paroi (°C).
    """
    return (T_m1 + T_m2) / 2

def calcul_coefficient_global_echange(h1, h2, de, di, Rf_cal, Rf_tub, lambd_m):
    """
    Calcule le coefficient global d'échange thermique.

    :param h1: Coefficient de convection côté tubes (W/m².K).
    :param h2: Coefficient de convection côté calandre (W/m².K).
    :param de: Diamètre extérieur des tubes (m).
    :param di: Diamètre intérieur des tubes (m).
    :param Rf_cal: Résistance de salissement côté calandre (m².K/W).
    :param Rf_tub: Résistance de salissement côté tubes (m².K/W).
    :param lambd_m: Conductivité thermique du matériau des tubes (W/m.K).
    :return: Coefficient global d'échange thermique (W/m².K).
    """
    R_total = (
        1 / h2 +
        Rf_cal +
        (de * math.log(de / di)) / (2 * lambd_m) +
        (de * Rf_tub / di) +
        (de / (di * h1))
    )
    U_glo = 1 / R_total
    return U_glo

def validation_coefficient_global_echange(Uo_supp, U_glob):
    """
    Valide le coefficient global d'échange thermique en comparant la valeur calculée à une valeur supposée.

    :param Uo_supp: Coefficient d'échange supposé (W/m².K).
    :param U_glob: Coefficient global calculé (W/m².K).
    :return: (bool, marge) - Validation et marge d'erreur relative (en %).
    """
    marge = abs(U_glob - Uo_supp) / U_glob
    return marge <= 0.3, marge


def calcul_parametres_tubes(de, di, lt, L, S0, type_maille, np):
    """
    Calcule les paramètres des tubes, notamment le nombre de tubes, le diamètre de la calandre,
    et la distance entre les chicanes.

    :param de: Diamètre extérieur des tubes (m).
    :param di: Diamètre intérieur des tubes (m).
    :param lt: Répartition des tubes dans le faisceau (m).
    :param L: Longueur des tubes (m).
    :param S0: Surface d'échange thermique (m²).
    :param type_maille: Type de maille ("carré" ou "triangulaire").
    :param np: Nombre de passes.
    :return: Dictionnaire contenant n_t0, D_v0, et l_c0.
    """
    n_t0 = S0 / (math.pi * de * L * np)

    if type_maille not in ["carré", "triangulaire"]:
        raise ValueError("Type de maille invalide. Veuillez choisir 'carré' ou 'triangulaire'.")

    if type_maille == "carré":
        if np <= 1:
            D_v0 = 1.46 * lt * n_t0**0.466
        else:
            D_v0 = 1.46 * lt * n_t0**0.466 + 0.0085 * np
    elif type_maille == "triangulaire":
        if np <= 1:
            D_v0 = 1.57 * lt * n_t0**0.45
        else:
            D_v0 = 1.57 * lt * n_t0**0.45 + 0.0085 * np

    l_c0 = 0.4 * D_v0

    return {
        "n_t0": n_t0,
        "D_v0": D_v0,
        "l_c0": l_c0
    }

def calcul_supplementaire_tubes(flow_rate, rho, Pr, nt, di, mu, mu_paroi_chaud, k, L, np):
    """
    Calcule les paramètres supplémentaires des tubes, notamment Re, Pr, Nu et h1.

    :param flow_rate: Débit massique (kg/s).
    :param rho: Masse volumique (kg/m³).
    :param Pr: Nombre de Prandtl.
    :param nt: Nombre de tubes.
    :param di: Diamètre intérieur (m).
    :param mu: Viscosité dynamique (Pa.s).
    :param mu_paroi_chaud: Viscosité dynamique sur la paroi (Pa.s).
    :param k: Conductivité thermique (W/m.K).
    :param L: Longueur des tubes (m).
    :param np: Nombre de passes.
    :return: Dictionnaire contenant Re, Pr, Nu, u1 et h1.
    """
    # Vitesse moyenne
    u1 = 4 * flow_rate * np / (math.pi * di**2 * nt * rho)

    # Nombre de Reynolds
    Re = u1 * di * rho / mu
    
    # Nombre de Nusselt
    if Re < 2300:
        Nu = 1.86 * (Re * Pr * di / L)**(1/3) * (mu / mu_paroi_chaud)**0.14
    else:
        Nu = 0.023 * Re**0.8 * Pr**(1/3) * (mu / mu_paroi_chaud)**0.14

    # Coefficient de convection
    h1 = Nu * k / di

    return {
        "Re": Re,
        "Pr": Pr,
        "Nu": Nu,
        "u1": u1,
        "h1": h1
    }



def calcul_supplementaire_calandre(flow_rate, rho, Pr, de, mu, mu_paroi, k, D_v0, lt, lc):
    """
    Calcule les paramètres supplémentaires de la calandre, notamment d_eq, S_eq, u_eq, Re, Nu et h2.

    :param flow_rate: Débit massique (kg/s).
    :param rho: Masse volumique (kg/m³).
    :param Pr: Nombre de Prandtl.
    :param de: Diamètre extérieur des tubes (m).
    :param mu: Viscosité dynamique (Pa.s).
    :param mu_paroi: Viscosité dynamique sur la paroi (Pa.s).
    :param k: Conductivité thermique (W/m.K).
    :param D_v0: Diamètre de la calandre (m).
    :param lt: Répartition des tubes dans la calandre (m).
    :param lc: Distance entre les chicanes (m).
    :return: Dictionnaire contenant d_eq, S_eq, u_eq, Re, Nu et h2.
    """
    # Diamètre hydraulique
    d_eq = (4 * (lt**2 - math.pi * de**2 / 4)) / (math.pi * de)

    # Section équivalente
    S_eq = (D_v0 / lt) * (lt - de) * lc

    # Vitesse équivalente
    u_eq = flow_rate / (rho * S_eq)

    # Nombre de Reynolds
    Re = u_eq * d_eq * rho / mu

    # Facteur de friction et Nusselt
    if Re < 2300:
        y1 = 1.2971 *(Re)**(0.6384 + 0.0971 * math.log(Re))
    else:
        y1 = 0.1046 * Re**0.6464

    j_h = (1 - 0.49 * (1 - (lc / D_v0)))* y1 
    Nu = j_h * Pr**(1/3) * (mu / mu_paroi)**0.14

    # Coefficient de convection
    h2 = Nu * k / d_eq

    return {
        "d_eq": d_eq,
        "S_eq": S_eq,
        "u_eq": u_eq,
        "Re": Re,
        "Nu": Nu,
        "h2": h2
    }



def calculer_reynolds(debit_massique, d, mu, rho):
    """
    Calculer le nombre de Reynolds pour les tubes.
    Args:
        debit_massique (float): Débit massique (kg/s).
        d (float): Diamètre intérieur des tubes (m).
        mu (float): Viscosité dynamique (Pa.s).
        rho (float): Masse volumique (kg/m³).
    Returns:
        float: Nombre de Reynolds.
    """
    v = debit_massique / (rho * (3.1415 * (d ** 2) / 4))  # Vitesse moyenne dans les tubes
    return rho * v * d / mu


def calculer_nusselt(Re, Pr):
    """
    Calculer le nombre de Nusselt pour les tubes.
    Args:
        Re (float): Nombre de Reynolds.
        Pr (float): Nombre de Prandtl.
    Returns:
        float: Nombre de Nusselt.
    """
    if Re < 2300:  # Régime laminaire
        return 3.66
    else:  # Régime turbulent
        return 0.023 * (Re ** 0.8) * (Pr ** 0.3)


def calculer_coefficient_convection(Nu, k, d):
    """
    Calculer le coefficient de convection thermique.
    Args:
        Nu (float): Nombre de Nusselt.
        k (float): Conductivité thermique (W/m.K).
        d (float): Diamètre intérieur des tubes (m).
    Returns:
        float: Coefficient de convection thermique (W/m².K).
    """
    return Nu * k / d


def calculer_diametre_hydraulique(d_ext, d_int, rho):
    """
    Calculer le diamètre hydraulique pour la calandre.
    Args:
        d_ext (float): Diamètre extérieur des tubes (m).
        d_int (float): Diamètre intérieur des tubes (m).
        rho (float): Masse volumique (kg/m³).
    Returns:
        float: Diamètre hydraulique (m).
    """
    A = 3.1415 * ((d_ext / 2) ** 2 - (d_int / 2) ** 2)  # Aire transversale
    P = 3.1415 * d_ext  # Périmètre mouillé
    return 4 * A / P


def calculer_vitesse_equivalente(debit_massique, d_eq, rho):
    """
    Calculer la vitesse équivalente pour la calandre.
    Args:
        debit_massique (float): Débit massique (kg/s).
        d_eq (float): Diamètre hydraulique (m).
        rho (float): Masse volumique (kg/m³).
    Returns:
        float: Vitesse équivalente (m/s).
    """
    A = 3.1415 * (d_eq ** 2) / 4  # Aire transversale
    return debit_massique / (rho * A)


def calculer_coefficient_calandre(Nu, k, d_eq):
    """
    Calculer le coefficient de convection thermique côté calandre.
    Args:
        Nu (float): Nombre de Nusselt.
        k (float): Conductivité thermique (W/m.K).
        d_eq (float): Diamètre hydraulique (m).
    Returns:
        float: Coefficient de convection thermique (W/m².K).
    """
    return Nu * k / d_eq


#=========================================================================================

def calcul_pertes_charge_calandre(rho, mu, mu_paroi_froid, d_eq, L, u_eq, Re, l_c0, D_v0, j):
    """
    Calcule les pertes de charge du côté calandre.

    :param rho: Masse volumique du fluide froid (kg/m^3)
    :param mu: Viscosité dynamique du fluide froid (Pa.s)
    :param mu_paroi_froid: Viscosité dynamique à la paroi (Pa.s)
    :param d_eq: Diamètre hydraulique (m)
    :param L: Longueur des tubes (m)
    :param u_eq: Vitesse équivalente (m/s)
    :param Re: Nombre de Reynolds
    :param l_c0: Distance entre les chicanes (m)
    :param D_v0: Diamètre de la calandre (m)
    :param j: Facteur de frottement donné par l'utilisateur
    :return: Pertes de charge côté calandre (Pa)
    """
    try:
        # Calcul du nombre de chicanes
        N_c = L / l_c0

        # Calcul des pertes de charge
        Delta_P_calandre = ((8 * j * (u_eq**2) * (N_c + 1) * D_v0 * rho / (2 * d_eq)) *
                             ((mu / mu_paroi_froid) ** -0.14))

        return Delta_P_calandre

    except ZeroDivisionError:
        return None
    except Exception as e:
        print(f"Erreur dans calcul_pertes_charge_calandre : {e}")
        return None



def calcul_pertes_charge_cote_tubes(rho, mu, mu_paroi_chaud, di, L, u1, Re, np, j):
    """
    Calcule les pertes de charge côté tubes.

    :param rho: Masse volumique du fluide chaud (kg/m^3)
    :param mu: Viscosité dynamique du fluide chaud (Pa.s)
    :param mu_paroi_chaud: Viscosité dynamique sur la paroi (Pa.s)
    :param di: Diamètre intérieur des tubes (m)
    :param L: Longueur des tubes (m)
    :param u1: Vitesse moyenne (m/s)
    :param Re: Nombre de Reynolds
    :param np: Nombre de passes
    :param j: Facteur de Colburn donné par l'utilisateur
    :return: Pertes de charge totales côté tubes (Pa)
    """
    try:
        # Coefficient de correction
        K = 2.5
        m = 0.14 if Re > 2300 else 0.25

        # Calcul des pertes de charge
        Delta_P_tubes = (K + 8 * j * np * (L / di) * (mu / mu_paroi_chaud) ** -m) * ((rho * (u1 ** 2)) / 2)

        return Delta_P_tubes

    except ZeroDivisionError:
        return None
    except Exception as e:
        print(f"Erreur dans calcul_pertes_charge_cote_tubes : {e}")
        return None


def estimation_cout_echangeur(S0):
    """
    Estime le coût de l'échangeur de chaleur à partir de la surface d'échange thermique S0.

    :param S0: Surface d'échange thermique (m²)
    :return: Estimation du coût (unité monétaire) ou None en cas d'erreur
    """
    try:
        if S0 <= 0:
            print("Erreur : La surface d'échange thermique (S0) doit être positive.")
            return None

        # Formule d'estimation du coût
        cout = 2143 * (S0 ** 0.514)
        return cout

    except Exception as e:
        print(f"Erreur dans estimation_cout_echangeur : {e}")
        return None


