import DES
import gestionnaire_de_fichier
import convertisseur
import constantes
from time import time

def cassage_brutal(sdes: DES.SDES, message_clair: list[int], message_chiffre: list[int]):
    for i in range(message_clair):
        for j in range(message_clair):
            liste = sdes.encrypte_tout_textes(message_clair, i, j)
            if liste == message_chiffre:
                return i, j, liste
    return None, None

def cassage_astucieux(sdes: DES.SDES, message_clair: list[int], message_chiffre: list[int]):
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

sdes = DES.SDES(1, 1)
fichier_en_clair = gestionnaire_de_fichier.lit_le_fichier(constantes.FICHIER_TXT_ARSENE_LUPIN)
fichier_en_clair = convertisseur.convertit_str_en_dec(fichier_en_clair)


fichier_chiffre = sdes.encrypte_tout_textes(fichier_en_clair, sdes.cle1, sdes.cle2)

# t1 = time()
# print(cassage_brutal(sdes, fichier_en_clair, fichier_chiffre))
# t2 = time()
# print(str(t2-t1) + " s")
cassage_astucieux(sdes, fichier_en_clair, fichier_chiffre)
# doit retourner (5, 250), les valeurs dans l'instance sdes