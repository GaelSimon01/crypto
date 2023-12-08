#!/usr/bin/python3
#
# Author: Joao H de A Franco (jhafranco@acm.org)
#
# Description: Simplified DES implementation in Python 3
#
# Date: 2012-02-10
#
# License: Attribution-NonCommercial-ShareAlike 3.0 Unported
#          (CC BY-NC-SA 3.0)
#===========================================================
from sys import exit
from time import time
import convertisseur
import gestionnaire_de_fichier
import constantes

class SDES():
    """Est la classe de chiffrement dévié de DES"""
    KeyLength = 10
    SubKeyLength = 8
    DataLength = 8
    FLength = 4
    
    # Tables for initial and final permutations (b1, b2, b3, ... b8)
    IPtable = (2, 6, 3, 1, 4, 8, 5, 7)
    FPtable = (4, 1, 3, 5, 7, 2, 8, 6)
    
    # Tables for subkey generation (k1, k2, k3, ... k10)
    P10table = (3, 5, 2, 7, 4, 10, 1, 9, 8, 6)
    P8table = (6, 3, 7, 4, 8, 5, 10, 9)
    
    # Tables for the fk function
    EPtable = (4, 1, 2, 3, 2, 3, 4, 1)
    S0table = (1, 0, 3, 2, 3, 2, 1, 0, 0, 2, 1, 3, 3, 1, 3, 2)
    S1table = (0, 1, 2, 3, 2, 0, 1, 3, 3, 0, 1, 0, 2, 1, 0, 3)
    P4table = (2, 4, 3, 1)

    def __init__(self, cle_bin_one: int, cle_bin_two: int):
        """Est le constructeur de la class SDES pour démarrer le processus de chiffrage

        Args:
            cle_bin_one : la première clé binaire du premier chiffrement
            cle_bin_two : la deuxième clé binaire du deuxième chiffrement
        """
        self.cle1 = cle_bin_one
        self.cle2 = cle_bin_two
 
    def perm(self, inputByte, permTable):
        """Permute input byte according to permutation table"""
        outputByte = 0
        for index, elem in enumerate(permTable):
            if index >= elem:
                outputByte |= (inputByte & (128 >> (elem - 1))) >> (index - (elem - 1))
            else:
                outputByte |= (inputByte & (128 >> (elem - 1))) << ((elem - 1) - index)
        return outputByte
 
    def ip(self, inputByte):
        """Perform the initial permutation on data"""
        return self.perm(inputByte, self.IPtable)
    
    def fp(self, inputByte):
        """Perform the final permutation on data"""
        return self.perm(inputByte, self.FPtable)
    
    def swapNibbles(self, inputByte):
        """Swap the two nibbles of data"""
        return (inputByte << 4 | inputByte >> 4) & 0xff
    
    def keyGen(self, key):
        """Generate the two required subkeys"""
        def leftShift(keyBitList):
            """Perform a circular left shift on the first and second five bits"""
            shiftedKey = [None] * self.KeyLength
            shiftedKey[0:9] = keyBitList[1:10]
            shiftedKey[4] = keyBitList[0]
            shiftedKey[9] = keyBitList[5]
            return shiftedKey
    
        # Converts input key (integer) into a list of binary digits
        keyList = [(key & 1 << i) >> i for i in reversed(range(self.KeyLength))]
        permKeyList = [None] * self.KeyLength
        for index, elem in enumerate(self.P10table):
            permKeyList[index] = keyList[elem - 1]
        shiftedOnceKey = leftShift(permKeyList)
        shiftedTwiceKey = leftShift(leftShift(shiftedOnceKey))
        subKey1 = subKey2 = 0
        for index, elem in enumerate(self.P8table):
            subKey1 += (128 >> index) * shiftedOnceKey[elem - 1]
            subKey2 += (128 >> index) * shiftedTwiceKey[elem - 1]
        return (subKey1, subKey2)
    
    def fk(self, subKey, inputData):
        """Apply Feistel function on data with given subkey"""
        def F(sKey, rightNibble):
            aux = sKey ^ self.perm(self.swapNibbles(rightNibble), self.EPtable)
            index1 = ((aux & 0x80) >> 4) + ((aux & 0x40) >> 5) + \
                    ((aux & 0x20) >> 5) + ((aux & 0x10) >> 2)
            index2 = ((aux & 0x08) >> 0) + ((aux & 0x04) >> 1) + \
                    ((aux & 0x02) >> 1) + ((aux & 0x01) << 2)
            sboxOutputs = self.swapNibbles((self.S0table[index1] << 2) + self.S1table[index2])
            return self.perm(sboxOutputs, self.P4table)
    
        leftNibble, rightNibble = inputData & 0xf0, inputData & 0x0f
        return (leftNibble ^ F(subKey, rightNibble)) | rightNibble
    
    def encrypt(self, key, plaintext):
        """Encrypt plaintext with given key"""
        data = self.fk(self.keyGen(key)[0], self.ip(plaintext))
        return self.fp(self.fk(self.keyGen(key)[1], self.swapNibbles(data)))
    
    def decrypt(self, key, ciphertext):
        """Decrypt ciphertext with given key"""
        data = self.fk(self.keyGen(key)[1], self.ip(ciphertext))
        return self.fp(self.fk(self.keyGen(key)[0], self.swapNibbles(data)))
    
    def double_chiffrement(self, message, cle1, cle2):
        """Encrypt twice the plaintext"""
        return self.encrypt(cle2, self.encrypt(cle1, message))
    
    def encrypte_tout_textes(self, plaintext, cle1, cle2):
        """Encrypt each character of the plaintext with one key"""
        res = []
        for dec in plaintext:
            res.append(self.double_chiffrement(dec, cle1, cle2))
        return res
    
    def double_dechiffrement(self, message_chiffre, cle1, cle2):
        """Return the plaintext twice decrypted"""
        return self.decrypt(cle2, self.decrypt(cle1, message_chiffre))

# =================== TESTS ================ #

# 0b indique le type binaire de la valeur
cle1=0b1010101000 # 680
cle2=0b0110001011 # 395

message=0b00000001 # 1
message_arsene = gestionnaire_de_fichier.lit_le_fichier(constantes.FICHIER_TXT_ARSENE_LUPIN)
message_persannes = gestionnaire_de_fichier.lit_le_fichier(constantes.FICHIER_LETTRES_PERSANNES)
# # print("\n on essaie de chiffrer " + str(message) + " avec les clés ( " + str(cle1) + ", " + str(cle2) + " ) ")
# message = None
# sdes = SDES(cle1, cle2, message)

# print(sdes.encrypte_tout_textes(message_arsene, cle1, cle2))
# print("\n#==============================================#\n")
# print(sdes.encrypte_tout_textes(message_persannes, cle1, cle2))

# Principe de SDES, double chiffrements
sdes = SDES(cle1, cle2)
mc1 = sdes.encrypt(cle1, message)
mc2 = sdes.encrypt(cle2, mc1)
print(mc1) # 87
print(mc2) # 241
# ===========================


# Double chiffrement 
# encrypt(cle2, encrypt(cle1,message)) == SDES(SDES(M, k1), k2)

print("\n")
mdc1 = sdes.decrypt(cle2, mc2)
print(mdc1) # 87
print("la réponse est")
mdc2 = sdes.decrypt(cle1, mdc1)
print(mdc2)