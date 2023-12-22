import DES
import gestionnaire_de_fichier
import convertisseur
import constantes
from time import time

def cassage_brutal(sdes: DES.SDES, message_clair: list[int], message_chiffre: list[int]):
    """
    Casse la clé en utilisant une méthode brutale en comparant toutes les combinaisons possibles.

    Args:
    - sdes (DES.SDES): Instance de l'algorithme de chiffrement.
    - message_clair (list[int]): Message clair en entiers.
    - message_chiffre (list[int]): Message chiffré en entiers.

    Returns:
    - Tuple[int, int, list[int]]: Clés trouvées et liste des messages chiffrés.
    """
    for i in range(constantes.LONGUEUR_CLE_BINAIRE):
        for j in range(constantes.LONGUEUR_CLE_BINAIRE):
            liste = sdes.encrypte_tout_textes(message_clair, i, j)
            if liste == message_chiffre:
                return i, j, liste
    return None, None

def cassage_astucieux(sdes: DES.SDES, message_clair: list[int], message_chiffre: list[int]):
    """
    Casse la clé en utilisant une méthode plus efficace en construisant un dictionnaire.

    Args:
    - sdes (DES.SDES): Instance de l'algorithme de chiffrement.
    - message_clair (list[int]): Message clair en entiers.
    - message_chiffre (list[int]): Message chiffré en entiers.

    Returns:
    - Union[Tuple[int, int], bool]: Clés trouvées ou False si aucune clé n'est trouvée.
    """
    dico=dict()
    for i in range(constantes.LONGUEUR_CLE_BINAIRE):
        res = []
        for dec in message_clair:
            res.append(sdes.encrypt(i,dec))
        dico[tuple(res)]=i  # convertit la liste en tuple
    keys=dico.keys()

    keys=set(keys)
    for y in range(constantes.LONGUEUR_CLE_BINAIRE):
        res = []
        for dec in message_chiffre:
            res.append(sdes.decrypt(y,dec))
        if tuple(res) in keys:  # Convertit la liste en tuple
            return (dico[tuple(res)],y)
    return False

def run_experiment(sdes, message_clair, message_chiffre, nombre_executions):
    """
    Exécute plusieurs fois les méthodes de cassage pour obtenir des statistiques.

    Args:
    - sdes (DES.SDES): Instance de l'algorithme de chiffrement.
    - message_clair (list[int]): Message clair en entiers.
    - message_chiffre (list[int]): Message chiffré en entiers.
    - nombre_executions (int): Nombre d'exécutions à effectuer.

    Returns:
    - Tuple[float, float, float, float]: Moyennes des tentatives et temps pour les méthodes brutale et astucieuse.
    """
    total_tentatives_astucieux = 0
    total_tentatives_brutal = 0
    total_temps_astucieux = 0
    total_temps_brutal = 0

    for _ in range(nombre_executions):
        debut = time()
        tentatives_astucieux = cassage_astucieux(sdes, message_clair, message_chiffre)
        fin = time()
        temps_astucieux = fin - debut

        debut = time()
        tentatives_brutal = cassage_brutal(sdes, message_clair, message_chiffre)
        fin = time()
        temps_brutal = fin - debut

        total_tentatives_astucieux += tentatives_astucieux[0] if tentatives_astucieux else 0
        total_tentatives_brutal += tentatives_brutal[0] if tentatives_brutal else 0
        total_temps_astucieux += temps_astucieux
        total_temps_brutal += temps_brutal

    moyenne_tentatives_astucieux = total_tentatives_astucieux / nombre_executions
    moyenne_tentatives_brutal = total_tentatives_brutal / nombre_executions
    moyenne_temps_astucieux = total_temps_astucieux / nombre_executions
    moyenne_temps_brutal = total_temps_brutal / nombre_executions

    return (moyenne_tentatives_astucieux, moyenne_temps_astucieux,
            moyenne_tentatives_brutal, moyenne_temps_brutal)

sdes = DES.SDES(10, 30)
# fichier_en_clair = gestionnaire_de_fichier.lit_le_fichier(constantes.FICHIER_TXT_ARSENE_LUPIN)
fichier_en_clair = gestionnaire_de_fichier.lit_le_fichier(constantes.FICHIER_LETTRES_PERSANNES)
fichier_en_clair = convertisseur.convertit_str_en_dec(fichier_en_clair)


fichier_chiffre = sdes.encrypte_tout_textes(fichier_en_clair, sdes.cle1, sdes.cle2)

# Résultats pour 10 exécutions
resultats = run_experiment(sdes, fichier_en_clair, fichier_chiffre, 10)
print("Moyenne de tentatives (astucieux):", resultats[0])
print("Moyenne de temps (astucieux):", resultats[1], "s")
print("Moyenne de tentatives (brutal):", resultats[2])
print("Moyenne de temps (brutal):", resultats[3], "s")

t1 = time()
print(fichier_en_clair)
print(cassage_brutal(sdes, fichier_en_clair, fichier_chiffre))
t2 = time()
print(str(t2-t1) + " s")

t1 = time()
print(cassage_astucieux(sdes, fichier_en_clair, fichier_chiffre))
t2 = time()
print(str(t2-t1) + " s")
# doit retourner (5, 250), les valeurs dans l'instance sdes