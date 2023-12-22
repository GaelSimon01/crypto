import images
from scapy.all import *
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from constantes import FICHIER_TRACE_RESEAUX

def duplique_cle_de_session(cle):
    """
    Duplique une clé de session en multipliant sa taille par 4.

    Args:
    - cle (list[int]): Clé de session à dupliquer.

    Returns:
    - list[int]: Clé de session dupliquée.
    """
    cle *= 4
    return cle

def analyser_fichier_cap(fichier_cap):
    """
    Analyse un fichier de capture réseau au format .cap, extrait les paquets UDP, et récupère leur contenu et IV.

    Args:
    - fichier_cap (str): Chemin vers le fichier .cap à analyser.

    Returns:
    - Tuple[list[bytes], list[bytes]]: Contenu des paquets et liste des IV.
    """
    packets = rdpcap(fichier_cap)
    udp_packets = [packet for packet in packets if "UDP" in packet and packet["UDP"].dport == 9999]
    contenu_des_paquets = []
    liste_IV = []
    for packet in udp_packets:
        print(packet.summary())
        print("\nContenu du paquet :")
        if Raw in packet:
            contenu_des_paquets.append(packet[Raw].load[16:])
            print(packet[Raw].load[16:])
        iv = packet.load[:16]
        liste_IV.append(iv)
        print("IV : " + str(iv) + "\n")
    return contenu_des_paquets, liste_IV

def binaire_to_decimal(cle_de_session: list[int]):
    """
    Convertit une clé de session binaire en valeur décimale.

    Args:
    - cle_de_session (list[int]): Clé de session en binaire.

    Returns:
    - int: Valeur décimale correspondante.
    """
    binaire_en_string = ''.join(str(bit) for bit in cle_de_session)
    valeur_decimal_correspondante = int(binaire_en_string, 2)
    return valeur_decimal_correspondante

def decrypt_aes_with_key(key, iv, encrypted_data):
    """
    Déchiffre des données chiffrées en utilisant AES avec une clé et un IV donnés.

    Args:
    - key (bytes): Clé de chiffrement.
    - iv (bytes): Vecteur d'initialisation.
    - encrypted_data (bytes): Données chiffrées.

    Returns:
    - str: Données déchiffrées.
    """
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    
    return unpadded_data.decode('utf-8', errors='ignore')

cle_de_base = images.trouve_la_cle_dans_images(images.compare_deux_images())
cle_duplique = duplique_cle_de_session(cle_de_base)

print("\nVoici la clé dupliqué de taille 256 : \n" + str(cle_duplique))

contenus_des_paquets_recuperes, liste_IV = analyser_fichier_cap(FICHIER_TRACE_RESEAUX)
print("Contenus des paquets :\n" + str(contenus_des_paquets_recuperes) + "\n")

cle_de_session_duplique_en_decimal = binaire_to_decimal(cle_duplique)
print("\nClé de session dupliquéé en décimal\n" + str(cle_de_session_duplique_en_decimal) + "\n")

for iv, donnes_encrypted in zip(liste_IV, contenus_des_paquets_recuperes):
    print(decrypt_aes_with_key(cle_duplique.encode('utf-8'), iv, donnes_encrypted))
