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
    liste = []
    for i in range(message_clair):
        sous_liste = [(i)]
        for elem in message_clair:
            sous_liste.append(sdes.encrypt(i, elem))
        liste.append(sous_liste)
    liste2 = []
    for j in range(message_clair):
        sous_liste = []
        for elem in message_clair:
            sous_liste.append(sdes.decrypt(j, elem))
        liste2.append(sous_liste)
    
    for (index1, liste1_1), (index2, liste2_2) in zip(enumerate(liste), enumerate(liste2)):
        possible_res = []
        for elem1_1_1, elem2_2_2 in zip(liste1_1, liste2_2):
            if elem1_1_1 == elem2_2_2: 
                possible_res.append(elem1_1_1)
    return None

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