from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

import constantes
import gestionnaire_de_fichier

def chiffrer_AES(cle: int, message_a_chiffrer: str, nombre: str):
    cle = cle.to_bytes(32, byteorder='big')  # Convertir la clé en bytes (256 bits ou 32 octets, taille des clés AES)
    mes_parametres = AES.new(cle, AES.MODE_CBC, nombre.encode('utf-8'))

    # Ajouter un padding aux données pour les ajuster à une longueur multiple de 16 octets
    donnees_a_chiffrer = pad(message_a_chiffrer.encode('utf-8'), AES.block_size)

    texte_chiffre = mes_parametres.encrypt(donnees_a_chiffrer)

    return texte_chiffre


def dechiffrer_AES(cle: int, message_a_dechiffrer: bytes, nombre: str):
    cle = cle.to_bytes(32, byteorder='big')  # Convertir la clé en bytes (256 bits)
    mes_parametres = AES.new(cle, AES.MODE_CBC, nombre.encode('utf-8'))

    donnees_dechiffrees = mes_parametres.decrypt(message_a_dechiffrer)

    # Retirer le padding après le déchiffrement
    donnees_originales = unpad(donnees_dechiffrees, AES.block_size).decode('utf-8')

    return donnees_originales


fichier_en_clair = gestionnaire_de_fichier.lit_le_fichier(constantes.FICHIER_LETTRES_PERSANNES)
chiffrement = chiffrer_AES(250, fichier_en_clair, "nous chiffrons!!")
print(chiffrement)

print("\n# ================================================================= #\n")

dechiffrement = dechiffrer_AES(250, chiffrement, "nous dechiffrons")
print(dechiffrement)

