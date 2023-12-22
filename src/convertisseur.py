from gestionnaire_de_fichier import lit_le_fichier
from constantes import FICHIER_LETTRES_PERSANNES, FICHIER_TXT_ARSENE_LUPIN

def convertit_str_en_dec(message_en_str: str) -> list[int]:
    """
    Convertit une chaîne de caractères en une liste d'entiers représentant les codes ASCII des caractères.

    Args:
    - message_en_str (str): Chaîne de caractères à convertir.

    Returns:
    - list[int]: Liste des codes ASCII correspondants aux caractères de la chaîne.
    """
    return list(ord(c) for c in message_en_str)

# Lecture du fichier FICHIER_LETTRES_PERSANNES
arsene_lupin = lit_le_fichier(FICHIER_LETTRES_PERSANNES)
print(convertit_str_en_dec(arsene_lupin))

print("\n# ================================================================ #\n")

# Lecture du fichier FICHIER_TXT_ARSENE_LUPIN
lettres_persannes = lit_le_fichier(FICHIER_TXT_ARSENE_LUPIN)
print(convertit_str_en_dec(lettres_persannes))
