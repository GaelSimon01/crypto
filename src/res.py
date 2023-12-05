import DES
import gestionnaire_de_fichier
import convertisseur
import constantes
from time import time

def cassage_brutal(sdes: DES.SDES, message_clair: list[int], message_chiffre: list[int]):
    for i in range(constantes.LONGUEUR_CLE_BINAIRE):
        for j in range(constantes.LONGUEUR_CLE_BINAIRE):
            liste = sdes.encrypte_tout_textes(message_clair, i, j)
            if liste == message_chiffre:
                return i, j
    return None, None

def cassage_astucieux(sdes: DES.SDES, message_clair: list[int], message_chiffre: list[int]):
    for i in range(constantes.LONGUEUR_CLE_BINAIRE):
        for j in range(constantes.LONGUEUR_CLE_BINAIRE):
            liste = sdes.encrypte_tout_textes(message_clair, i, j)
            if liste == message_chiffre:
                return i, j
    return None, None

sdes = DES.SDES(5, 250)
fichier_en_clair = gestionnaire_de_fichier.lit_le_fichier(constantes.FICHIER_TXT_ARSENE_LUPIN)
fichier_en_clair = convertisseur.convertit_str_en_dec(fichier_en_clair)
fichier_chiffre = sdes.encrypte_tout_textes(fichier_en_clair, sdes.cle1, sdes.cle2)

t1 = time()
print(cassage_brutal(sdes, fichier_en_clair, fichier_chiffre))
t2 = time()
print(str(t2-t1) + " s")
# doit retourner (5, 250), les valeurs dans l'instance sdes