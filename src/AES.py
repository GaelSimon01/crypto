from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

import constantes
import gestionnaire_de_fichier
from time import time

def chiffrer_AES(cle: int, message_a_chiffrer: str, vecteur_initilisation: str):
    cle = cle.to_bytes(32, byteorder='big')  # Convertir la clé en bytes (256 bits ou 32 octets, taille des clés AES)
    mes_parametres = AES.new(cle, AES.MODE_CBC, vecteur_initilisation.encode('utf-8'))

    # Ajouter un padding aux données pour les ajuster à une longueur multiple de 16 octets
    donnees_a_chiffrer = pad(message_a_chiffrer.encode('utf-8'), AES.block_size)

    texte_chiffre = mes_parametres.encrypt(donnees_a_chiffrer)

    return texte_chiffre


def dechiffrer_AES(cle: int, message_a_dechiffrer: str, vecteur_initilisation: str):
    cle = cle.to_bytes(32, byteorder='big')  # Convertir la clé en bytes (256 bits)
    mes_parametres = AES.new(cle, AES.MODE_CBC, vecteur_initilisation.encode('utf-8'))

    donnees_dechiffrees = mes_parametres.decrypt(message_a_dechiffrer)

    # Retirer le padding après le déchiffrement
    donnees_originales = unpad(donnees_dechiffrees, AES.block_size).decode('utf-8')

    return donnees_originales

def cassage_AES_force_brut(message_chiffre: bytes, VI: str, message_dechiffre: str):
    for i in range(constantes.LONGUEUR_CLE_AES):
        try:
            texte_dechiffre = dechiffrer_AES(i, message_chiffre, VI)
            if texte_dechiffre == message_dechiffre:
                return i 
        except Exception:
            pass
    return None


import time

def temps_moyen_cassage_AES_force_brut(message_chiffre, VI, message_dechiffre, nombre_essais):
    temps_total = 0
    for _ in range(nombre_essais):
        debut = time.time()
        cassage_AES_force_brut(message_chiffre, VI, message_dechiffre)
        fin = time.time()
        temps_execution = fin - debut
        temps_total += temps_execution
    temps_moyen = temps_total / nombre_essais
    return temps_moyen


def chiffrer_deux_fois_AES(cle: int, message_original: str, vecteur_initilisation: str):
    message_chiffre_1 = chiffrer_AES(cle, message_original, vecteur_initilisation)
    message_chiffre_2 = chiffrer_AES(cle, message_chiffre_1.hex(), vecteur_initilisation)
    return message_chiffre_2

def dechiffrer_deux_fois_AES(cle: int, message_chiffre: bytes, vecteur_initialisation: str):
    message_dechiffre_2 = dechiffrer_AES(cle, message_chiffre, vecteur_initialisation)
    message_dechiffre_1 = dechiffrer_AES(cle, message_dechiffre_2, vecteur_initialisation)
    return message_dechiffre_1

fichier_en_clair = gestionnaire_de_fichier.lit_le_fichier(constantes.FICHIER_LETTRES_PERSANNES)

cle = 186
# debut = time()
chiffrement = chiffrer_AES(cle, fichier_en_clair, "nous chiffrons!!")
# fin = time()
# print("\n" + str(chiffrement) + "\n" + str(fin - debut) + " sec")wx

# print("\n# ================================================================= #\n")

# debut = time()
dechiffrement = dechiffrer_AES(cle, chiffrement, "nous dechiffrons")
# fin = time()
# print("\n" + dechiffrement + "\n" + str(fin - debut) + " sec")

# print(cassage_AES_force_brut(chiffrement, "nous dechiffrons", dechiffrement))
nb_essais = 2
temps_moyen_execution = temps_moyen_cassage_AES_force_brut(chiffrement, "nous dechiffrons", dechiffrement, nb_essais)
print(f"Temps moyen pour le cassage par force brute pour AES : {temps_moyen_execution} sec pour {nb_essais} essais")

chiffrement_deux_fois = chiffrer_deux_fois_AES(cle, fichier_en_clair, "nous chiffrons!!")
print(chiffrement_deux_fois)
print(dechiffrer_deux_fois_AES(cle, chiffrement_deux_fois, "nous dechiffrons"))
