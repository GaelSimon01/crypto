import images
from scapy.all import *
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

from constantes import FICHIER_TRACE_RESEAUX

cle_de_base = images.trouve_la_cle_dans_images(images.compare_deux_images())
print(len(cle_de_base))

def duplique_cle_de_session(cle):
    cle*=4
    return cle

cle_duplique = ''.join(str(bit) for bit in duplique_cle_de_session(cle_de_base))
print(len(cle_duplique))

print("\nVoici la clé dupliqué de taille 256 : \n" + str(cle_duplique))

def analyser_fichier_cap(fichier_cap):
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

contenus_des_paquets_recuperes, liste_IV = analyser_fichier_cap(FICHIER_TRACE_RESEAUX)
print(contenus_des_paquets_recuperes)

# def binaire_to_decimal(cle_de_session: list[int]):
#     binaire_en_string = ''.join(str(bit) for bit in cle_de_session)
#     valeur_decimal_correspondante = int(binaire_en_string, 2)
#     return valeur_decimal_correspondante

# cle_de_session_duplique_en_decimal = binaire_to_decimal(cle_duplique)
# print("\nClé de session dupliquéé en décimal\n" + str(cle_de_session_duplique_en_decimal))

def decrypt_aes_with_key(key, iv, encrypted_data):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    
    return unpadded_data.decode('utf-8', errors='ignore')


for iv, donnes_encrypted in zip(liste_IV, contenus_des_paquets_recuperes):
    print(decrypt_aes_with_key(cle_duplique.encode('utf-8'), iv, donnes_encrypted))
