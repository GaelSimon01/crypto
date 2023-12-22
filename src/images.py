"""Code provenant de https://raymond-namyst.emi.u-bordeaux.fr/ens/lycee/TD1.html et de https://stackoverflow.com/questions/11064786/get-pixels-rgb-using-pil"""

from constantes import IMAGE_ROSSIGNOL1, IMAGE_ROSSIGNOL2, IMAGE_ROSSIGNOL1_STORED, IMAGE_ROSSIGNOL2_STORED, FICHIER_TXT_ROSSIGNOL1, FICHIER_TXT_ROSSIGNOL2, DIFFERENCE_FILE_IMAGE_1_AND_IMAGE_2, DIFFERENCE_FILE_IMAGE_1_AND_IMAGE_2_STORED
from gestionnaire_de_fichier import ecris_dans_un_fichier, lit_le_fichier, efface_un_fichier
from PIL.Image import *
import os

def lis_la_valeur_des_pixels(image, nom_du_fichier: str):
    """
    Lit les valeurs des pixels d'une image et les écrit dans un fichier texte.

    Args:
    - image (str): Chemin de l'image.
    - nom_du_fichier (str): Nom du fichier où écrire les valeurs des pixels.
    """
    (l, h) = i.size
    liste_values_pixels = []
    for y in range(h):
        for x in range(l):
            pixel = Image.getpixel(i, (x, y))
            liste_values_pixels.append(pixel)

    if nom_du_fichier == FICHIER_TXT_ROSSIGNOL1:
        if os.path.exists(IMAGE_ROSSIGNOL1_STORED): 
            efface_un_fichier(IMAGE_ROSSIGNOL1_STORED)
            ecris_dans_un_fichier(nom_du_fichier, liste_values_pixels)
        else:
            ecris_dans_un_fichier(nom_du_fichier, liste_values_pixels)

    if nom_du_fichier == FICHIER_TXT_ROSSIGNOL2:
        if os.path.exists(IMAGE_ROSSIGNOL2_STORED): 
            efface_un_fichier(IMAGE_ROSSIGNOL2_STORED)
            ecris_dans_un_fichier(nom_du_fichier, liste_values_pixels)
        else:
            ecris_dans_un_fichier(nom_du_fichier, liste_values_pixels)

liste_images_a_traiter = [IMAGE_ROSSIGNOL1, IMAGE_ROSSIGNOL2]

for image in liste_images_a_traiter:
    i = open(image)
    if (image==IMAGE_ROSSIGNOL1):
        lis_la_valeur_des_pixels(i, FICHIER_TXT_ROSSIGNOL1)
    else:
        lis_la_valeur_des_pixels(i, FICHIER_TXT_ROSSIGNOL2)

def compare_deux_images():
    """
    Compare les valeurs des pixels de deux images et stocke les différences dans un fichier texte.

    Returns:
    - list[int]: Liste des différences entre les pixels des deux images.
    """
    liste_difference = []
    for pixel_image_1, pixel_image_2 in zip(lit_le_fichier(IMAGE_ROSSIGNOL1_STORED), lit_le_fichier(IMAGE_ROSSIGNOL2_STORED)):
        if pixel_image_2.isdigit() and pixel_image_1.isdigit():
            if (int(pixel_image_2) - int(pixel_image_1)) == 1:
                liste_difference.append(int(pixel_image_2) - int(pixel_image_1))
            else:
                liste_difference.append(0)
    
    if os.path.exists(DIFFERENCE_FILE_IMAGE_1_AND_IMAGE_2_STORED): 
        efface_un_fichier(DIFFERENCE_FILE_IMAGE_1_AND_IMAGE_2_STORED)
        ecris_dans_un_fichier(DIFFERENCE_FILE_IMAGE_1_AND_IMAGE_2, liste_difference)
    else:
        ecris_dans_un_fichier(DIFFERENCE_FILE_IMAGE_1_AND_IMAGE_2, liste_difference)
    
    return liste_difference

def trouve_la_cle_dans_images(liste):
    """
    Récupère les premières 64 différences entre les pixels de deux images.

    Args:
    - liste (list[int]): Liste des différences entre les pixels des images.

    Returns:
    - list[int]: Liste des 64 premières différences.
    """
    res = []
    for i, bit in enumerate(liste):
        if i == 64:
            return res
        res.append(bit)
    return res

# Fonction principale pour récupérer les 64 premières différences entre les pixels
print(trouve_la_cle_dans_images(compare_deux_images()))
