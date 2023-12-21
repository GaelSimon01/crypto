from constantes import DOSSIER_SRC

import os

def lit_le_fichier(nom_du_fichier: str) -> None:
    try:
        fichier = open(nom_du_fichier, "r")
    except ValueError:
        print("Je pense qu'il y a un problème dans le chemin du fichier, revoit ton chemin")
    contenu = fichier.read()
    fichier.close()
    return contenu

def ecris_dans_un_fichier(nom_du_fichier: str, datas: list[str]) -> None:
    f = open("./src/" + nom_du_fichier, 'w')
    f.write(str(datas))
    print('on écrit dans ' + nom_du_fichier)

def efface_un_fichier(nom_du_fichier: str) -> None:
    os.remove(nom_du_fichier)
    print('on détruit ' + nom_du_fichier)