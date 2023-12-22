from constantes import DOSSIER_SRC

import os

def lit_le_fichier(nom_du_fichier: str) -> None:
    """
    Lit le contenu d'un fichier spécifié.

    Args:
    - nom_du_fichier (str): Nom du fichier à lire.

    Returns:
    - str: Contenu du fichier.
    """
    try:
        fichier = open(nom_du_fichier, "r")
    except ValueError:
        print("Je pense qu'il y a un problème dans le chemin du fichier, revoit ton chemin")
    contenu = fichier.read()
    fichier.close()
    return contenu

def ecris_dans_un_fichier(nom_du_fichier: str, datas: list[str]) -> None:
    """
    Écrit des données dans un fichier spécifié.

    Args:
    - nom_du_fichier (str): Nom du fichier où écrire les données.
    - datas (list[str]): Données à écrire dans le fichier.
    """
    f = open(DOSSIER_SRC + nom_du_fichier, 'w')
    f.write(str(datas))
    print('on écrit dans ' + nom_du_fichier)

def efface_un_fichier(nom_du_fichier: str) -> None:
    """
    Efface un fichier spécifié.

    Args:
    - nom_du_fichier (str): Nom du fichier à supprimer.
    """
    os.remove(nom_du_fichier)
    print('on détruit ' + nom_du_fichier)