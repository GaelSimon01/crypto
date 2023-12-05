def lit_le_fichier(nom_du_fichier: str) -> None:
    try:
        fichier = open(nom_du_fichier, "r")
    except ValueError:
        print("Je pense qu'il y a un problème dans le chemin du fichier, revoit ton chemin")
    contenu = fichier.read()
    fichier.close()
    return contenu