# Réponses aux question SAE crypto

## Membres du groupe

- Steven MARMION
- Gael SIMON

Groupe 2a2

## Questions

### **PARTIE 1**

#### Question 1

**En supposant que RSA soit utilisé correctement, Eve peut-elle espérer en venir à bout ?**

En supposant que RSA soit utilisé correctement, non, Eve ne peut espérer en venir à bout. Pourquoi ?
Car si l'on part du principe que RSA est utikisé correctement, on peut citer notammenet le fait que l'on factorise de très grand nombre durant le processus et quand l'on factorise deux nombres, il est très difficile de trouver le chemin arrière :

```text
▶ p, q -→ n = p.q facile (quadratique)
```

```text
▶ n = p.q -→ p, q difficile
```

De plus, pour un chiffrement RSA et son déchiffrement, on instancie les relations suivantes :

Clé publique est (e, n) et la clé privée est d.

**Chiffrer(T) :**

```text
▶ (T^e) mod n = (T^17) mod 3233
```

**Dechiffrer(C) :**

```text
▶ (C^d) mod n = (C^2753) mod 3233
```

Où **d = e^^−1 mod ϕ(n)** sauf que ϕ(n) = (p − 1)(q − 1) et p et q sont secrets. Le seul indice que l'on a pour trouver p et q est n et n = p*q. Ainsi, on revient au problème que nous avons énuméré tout à l'heure :

▶ p, q -→ n = p.q facile (quadratique)

▶ n = p.q -→ p, q difficile

#### Question 2

**En quoi l’algorithme SDES est-il peu sécurisé ?**

L'algo SDES utilise une clé de 10 bits pour chiffrer ce qui est peu 2^10=1024 combinaisons possible. il est donc possible de faire une attaque de force brute pour trouver la clé de chiffrement assez facilement.

#### Question 3

En utilsant un double SDES cela permet de de faire 2^10*2^10=1048576 combinaisons possible. il est donc possible de faire une attaque de force brute pour trouver la clé de chiffrement mais cela prendra plus de temps donc oui le double SDES est plus sécurisé.

## A vous de coder

### Chiffrement SDES

**Le code actuel de SDES ne permet que d’encoder un seul bloc de 8 bits, soit 1 octet. De plus, le double chiffrement n’est pas fourni. Proposez une extension permettant de coder un texte quelconque, quelle que soit sa taille. Vous chiffrerez notamment les textes disponibles sur Celene.**

Ici, suit on suit le sujet de la SAE, il est par logique décrit ceci :

le message est chiffré deux fois avec deux clés différentes:

**C = SDES(SDES(M, k1), k2)**
Par principe, le code que l'on récupère ne fait que théoriquement **C = SDES(k2, message)** et nous nous avons besoin de **SDES(SDES(M, k1), k2)**, c'est-à-dire littérallement un double chiffrement. Ainsi, nous avons juste à doubler ce chiffrement donnée, on répertorie donc le code suivant :

*prérequis : nous avons mit SDES dans une classe et toutes ces fonctions avec*.

Ici, on instancie une première fonction qui permet l'extension d'un double chiffrement comme le décrit SDES.

```py
def double_chiffrement(self, cle1, cle2, message):
    """Encrypt twice the plaintext"""
    return self.encrypt(cle2, self.encrypt(cle1, message))
```

En suite, le but est de pouvoir étendre le chiffrement plus loin qu'un encodage de 8 bits, ainsi, on instancie le programme qui permet de coder n'importe quel texte :

```py
def convertit_str_en_dec(message_en_str: str) -> list[str]:
    return list(ord(c) for c in message_en_str)
```

Ensuite, le but est de prendre la liste précédemment crée et d'encrypter chaque lettre avec la méthode double_chiffrement pour SDES, ainsi, on peut poser le programme suivant :

```py
def encrypte_tout_textes(self, plaintext, cle1, cle2):
    """Encrypt each character of the plaintext with one key"""
    liste_car = convertisseur.convertit_str_en_dec(plaintext)
    res = []
    for dec in liste_car:
        res.append(self.double_chiffrement(cle1, cle2, dec))
    return res
```

Et finalement, nous obtenons cette liste là pour le fichier arsene_lupin_extrait.txt :

>[124, 180, 203, 90, 244, 142, 90, 59, 90, 244, 142, 76, 1, 93, 142, 59, 254, 233, 59, 236, 93, 165, 76, 90, 59, 214, 19, 76, 225, 218, 252, 90, 59, 126, 233, 34, 93, 252, 144, 59, 159, 90, 252, 142, 236, 90, 89, 1, 252, 37, 242, 1, 89, 240, 76, 93, 253, 236, 90, 233, 76, 214, 59, 254, 90, 59, 60, 1, 233, 76, 93, 242, 90, 59, 126, 90, 240, 236, 1, 252, 242, 152, 124, 59, 193, 253, 233, 76, 242, 90, 107, 59, 236, 90, 59, 34, 76, 253, 248, 90, 142, 59, 83, 233, 142, 90, 252, 240, 90, 76, 159, 59, 55, 142, 142, 34, 225, 107, 189, 189, 8, 8, 8, 20, 159, 233, 142, 90, 252, 240, 90, 76, 159, 20, 253, 76, 159, 189, 90, 240, 253, 253, 85, 225, 189, 9, 132, 136, 145, 102, 152, 152, 19, 76, 225, 218, 252, 90, 59, 126, 233, 34, 93, 252, 59, 34, 1, 76, 89, 93, 59, 252, 253, 233, 225, 125, 59, 236, 71, 93, 252, 225, 1, 93, 225, 93, 225, 225, 1, 240, 236, 90, 59, 242, 1, 89, 240, 76, 93, 253, 236, 90, 233, 76, 59, 254, 253, 252, 142, 59, 253, 252, 59, 76, 1, 242, 253, 252, 142, 1, 93, 142, 152, 236, 90, 225, 59, 34, 76, 253, 233, 90, 225, 225, 90, 225, 59, 254, 1, 252, 225, 59, 142, 253, 233, 225, 59, 236, 90, 225, 59, 248, 253, 233, 76, 252, 1, 233, 244, 59, 254, 90, 34, 233, 93, 225, 59, 254, 90, 225, 59, 89, 253, 93, 225, 125, 59, 236, 71, 63, 252, 93, 159, 89, 1, 142, 93, 32, 233, 90, 152, 34, 90, 76, 225, 253, 252, 252, 1, 159, 90, 59, 1, 165, 90, 242, 59, 32, 233, 93, 59, 236, 90, 59, 165, 93, 90, 233, 244, 59, 83, 1, 252, 93, 89, 1, 76, 254, 144, 59, 252, 253, 142, 76, 90, 59, 89, 90, 93, 236, 236, 90, 233, 76, 59, 34, 253, 236, 93, 242, 93, 90, 76, 144, 59, 1, 165, 1, 93, 142, 152, 90, 252, 159, 1, 159, 63, 59, 242, 90, 59, 254, 233, 90, 236, 59, 200, 59, 89, 253, 76, 142, 59, 254, 253, 252, 142, 59, 236, 90, 225, 59, 34, 63, 76, 93, 34, 63, 142, 93, 90, 225, 59, 225, 90, 59, 254, 63, 76, 253, 233, 236, 1, 93, 90, 252, 142, 59, 254, 90, 59, 110, 1, 81, 253, 252, 59, 225, 93, 152, 34, 93, 142, 142, 253, 76, 90, 225, 32, 233, 90, 125, 59, 19, 76, 225, 218, 252, 90, 59, 126, 233, 34, 93, 252, 144, 59, 236, 90, 59, 110, 1, 252, 142, 1, 93, 225, 93, 225, 142, 90, 59, 159, 90, 252, 142, 236, 90, 89, 1, 252, 59, 32, 233, 93, 59, 252, 71, 253, 34, 218, 76, 90, 59, 32, 233, 90, 152, 254, 1, 252, 225, 59, 236, 90, 225, 59, 242, 55, 216, 142, 90, 1, 233, 244, 59, 90, 142, 59, 236, 90, 225, 59, 225, 1, 236, 253, 252, 225, 144, 59, 90, 142, 59, 32, 233, 93, 144, 59, 233, 252, 90, 59, 252, 233, 93, 142, 144, 59, 253, 181, 59, 93, 236, 59, 1, 165, 1, 93, 142, 59, 34, 63, 252, 63, 142, 76, 63, 152, 242, 55, 90, 5, 59, 236, 90, 59, 240, 1, 76, 253, 252, 59, 193, 242, 55, 253, 76, 89, 1, 252, 252, 144, 59, 90, 252, 59, 63, 142, 1, 93, 142, 59, 34, 1, 76, 142, 93, 59, 236, 90, 225, 59, 89, 1, 93, 252, 225, 59, 165, 93, 254, 90, 225, 59, 90, 142, 59, 1, 165, 1, 93, 142, 152, 236, 1, 93, 225, 225, 63, 59, 225, 1, 59, 242, 1, 76, 142, 90, 144, 59, 253, 76, 252, 63, 90, 59, 254, 90, 59, 242, 90, 142, 142, 90, 59, 110, 253, 76, 89, 233, 236, 90, 107, 59, 212, 19, 76, 225, 218, 252, 90, 59, 126, 233, 34, 93, 252, 144, 152, 159, 90, 252, 142, 236, 90, 89, 1, 252, 37, 242, 1, 89, 240, 76, 93, 253, 236, 90, 233, 76, 144, 59, 76, 90, 165, 93, 90, 252, 254, 76, 1, 59, 32, 233, 1, 252, 254, 59, 236, 90, 225, 59, 89, 90, 233, 240, 236, 90, 225, 59, 225, 90, 76, 253, 252, 142, 152, 1, 233, 142, 55, 90, 252, 142, 93, 32, 233, 90, 225, 41, 20, 59, 19, 76, 225, 218, 252, 90, 59, 126, 233, 34, 93, 252, 144, 59, 236, 71, 55, 253, 89, 89, 90, 59, 1, 233, 244, 59, 89, 93, 236, 236, 90, 59, 254, 63, 159, 233, 93, 225, 90, 89, 90, 252, 142, 225, 107, 59, 142, 253, 233, 76, 59, 200, 152, 142, 253, 233, 76, 59, 242, 55, 1, 233, 110, 110, 90, 233, 76, 144, 59, 142, 63, 252, 253, 76, 144, 59, 240, 253, 253, 85, 89, 1, 85, 90, 76, 144, 59, 110, 93, 236, 225, 59, 254, 90, 59, 110, 1, 89, 93, 236, 236, 90, 144, 59, 1, 254, 253, 236, 90, 225, 242, 90, 252, 142, 144, 152, 165, 93, 90, 93, 236, 236, 1, 76, 254, 144, 59, 242, 253, 89, 89, 93, 225, 37, 165, 253, 238, 1, 159, 90, 233, 76, 59, 89, 1, 76, 225, 90, 93, 236, 236, 1, 93, 225, 144, 59, 89, 63, 254, 90, 242, 93, 252, 59, 76, 233, 225, 225, 90, 144, 59, 142, 253, 76, 90, 76, 253, 152, 90, 225, 34, 1, 159, 252, 253, 236, 125]

**Proposez une méthode cassage_brutal(message_clair,message_chiffre) qui tente de retrouver les clés utilisées pour chiffrer le message en testant toutes les possibilités.**

En partant du principe que donc les tailles de clés sont de 2^8, on sait que le maximum d'une clé est 256, on peut donc poser le programme très simple mais très brutal suivant :

```py
def cassage_brutal(sdes: DES.SDES, message_clair: str, message_chiffre: list[str]):
    for i in range(256):
        for j in range(256):
            liste = sdes.encrypte_tout_textes(message_clair, i, j)
            if liste == message_chiffre:
                return i, j
    return None, None
```

Malheureusement, ce programme est un massacre, rien que pour déchiffrer le tuple de clés (5, 250), nous prenons 49sec. Nous imaginons pas pour un programme chiffrant les messages avec les clés (250, 250) ... Posons donc le tuple de clés (5, 250), nous prenons 49sec. Ainsi, pour faire une itération entière du premier élement du tuple, nous prenons 49/5 sec par itération de première boucle "for i in range(256):", c'est-à-dire environ 10 sec par itéaration. On peut donc imaginer que pour le tuple de clés (250, 250), nous prenons 250 * 10sec ~= 0,6944444 heure, c'est-à-dire environ 41,666664 min. Ainsi, le cassage_brutal est une catastrophe pourtant le programme est le plus simple possible.

Passons donc au cassage_astucieux :

**Proposez une fonction cassage_astucieux(message_clair,message_chiffre) qui permettra de tester moinsde possibilité de clés et ainsi réduire le temps d’exécution du cassage**.



### Partie 2

#### Question 1 Est-ce vraiment un problème? Justifiez votre réponse.

Le changement d'algo pose un problème car pour les SDES , nous utilisions une clé de 8 bits donc 2^8=256 possibilités de clés. Pour l'AES nous utilisons une clé de 256 bits donc 2^256 possibilités de clés. 
Par exemple pour juste une clé de 8 bits avce le SDES il nous faut 42 min maximum pour trouver la clé avec le cassege brutal. Pour une clés de 256 bits sur le SDES
il nous faudrait des siècles voir des millénaires pour trouver la clé.

#### Question 2 Nous allons tenter d’illustrer expérimentalement les différences entre les deux protocoles. Vous évaluerez:



##### Question 2.1 Le temps d’exécution du chiffrement/déchiffrement d’un message avec chacun des deux protocoles. Ici vous devez le mesurer expérimentalement et donc fournir le code Python associé.



##### Question 2.2 Le temps de cassage d’AES (même pour un cassage astucieux) si vous deviez l’exécuter sur votre ordinateur. Ici il faut uniquement estimer le temps nécessaire (sinon vous ne pourriez pas rendre votre rapport à temps!). Vous préciserez votre configuration et vous fournirez le détail des calculs.



#### Question 3 Il existe d’autres types d’attaques que de tester les différentes possibilités de clés. Lesquelles? Vous donnerez une explication succincte de l’une d’elles.
