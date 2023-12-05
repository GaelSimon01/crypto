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
