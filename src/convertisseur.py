""" Est le fichier de conversion str to bin et bin to str """

from gestionnaire_de_fichier import lit_le_fichier
from constantes import FICHIER_LETTRES_PERSANNES, FICHIER_TXT_ARSENE_LUPIN

def convertit_str_en_dec(message_en_str: str) -> list[int]:
    return list(ord(c) for c in message_en_str)

arsene_lupin = lit_le_fichier(FICHIER_LETTRES_PERSANNES)
print(convertit_str_en_dec(arsene_lupin))

print("\n# ================================================================ #\n")

lettres_persannes = lit_le_fichier(FICHIER_TXT_ARSENE_LUPIN)
print(convertit_str_en_dec(lettres_persannes))