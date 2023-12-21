from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from scapy.all import *
from constantes import FICHIER_TRACE_RESEAUX
from trace_reseaux import cle_de_base, liste_IV

def decrypt_aes_with_key(key, iv, encrypted_data):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    
    return unpadded_data.decode('utf-8', errors='ignore')

def replicate_key(key_part):
    return key_part * 4  # Réplique la partie de clé 4 fois pour obtenir la clé complète

def process_packets(packet_list, keys, ivs):
    for i, packet in enumerate(packet_list):
        if "UDP" in packet and packet["UDP"].dport == 9999:  # Vérifie si le paquet correspond au bon port UDP
            encrypted_data = packet.load[16:]  # Les données chiffrées (après les 16 premiers octets : IV)
            key_part = keys[i]  # Partie de la clé récupérée
            full_key = replicate_key(key_part)  # Réplique la partie de clé pour obtenir la clé complète
            iv = ivs[i]  # Récupère le vecteur d'initialisation (IV) correspondant

            decrypted_data = decrypt_aes_with_key(full_key, iv, encrypted_data)
            print("Message déchiffré :", decrypted_data)

# Charger votre fichier de capture ici
packets = rdpcap(FICHIER_TRACE_RESEAUX)

# Liste des clés partielles (64 bits chacune)
keys = [str(cle_de_base), str(cle_de_base)]  # Remplacez avec vos clés partielles
# Liste des vecteurs d'initialisation (IV)
ivs = liste_IV  # Remplacez avec vos IV

# Traiter les paquets pour extraire les messages chiffrés et les déchiffrer
process_packets(packets, keys, ivs)
