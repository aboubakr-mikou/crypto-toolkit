# symmetric.py
# Module de chiffrement symétrique AES utilisant la bibliothèque cryptography

import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


class SymmetricCipher:
    """ Classe qui implémente le chiffrement et déchiffrement AES.
        Supporte AES-128, AES-192 et AES-256 selon la taille de clé.
        Utilise le mode CBC avec un IV aléatoire et un padding PKCS7.
    """

    # Correspondance entre la taille en bits et la taille en octets
    VALID_KEY_SIZES = { 
        128: 16,
        192: 24,
        256: 32
    }

    def __init__(self, key_size=256): 
        if key_size not in self.VALID_KEY_SIZES:
            raise ValueError("Erreur !!! : la taille de clé doit être 128, 192 ou 256 bits")

        self.key_size_bits = key_size
        self.key_size_bytes = self.VALID_KEY_SIZES[key_size]
        self.key = None  # La clé AES sera stockée ici


    # ── Gestion de la clé ──

    def generate_key(self):
        """Génère une clé AES sécurisée aléatoire."""
        self.key = os.urandom(self.key_size_bytes)  # Génère une clé aléatoire de la taille spécifiée
        return self.key

    def set_key(self, key):
        """Charge une clé AES existante."""
        if len(key) != self.key_size_bytes:
            raise ValueError("Longueur de clé invalide")
        self.key = key  # Stocke la clé fournie pour le chiffrement/déchiffrement

    def get_key_hex(self):
        """Retourne la clé actuelle au format hexadécimal."""
        if self.key is None:
            raise ValueError("Clé non générée")
        return self.key.hex()  # Transforme les octets de la clé en chaîne hexadécimale


    # ── Chiffrement ──

    def encrypt_text(self, plaintext):
        """Chiffre une chaîne de caractères avec AES-CBC."""

        if self.key is None:
            raise ValueError("Clé non définie")

        # Convertit le texte en octets
        plaintext_bytes = plaintext.encode("utf-8")

        # Crée un IV aléatoire de 16 octets
        iv = os.urandom(16)

        # Ajoute du padding pour que la taille soit un multiple de 16
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext_bytes) + padder.finalize()

        # Prépare l'objet AES-CBC avec la clé et l'IV
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv)
        )

        # Crée un outil pour chiffrer
        encryptor = cipher.encryptor() 

        # Chiffre les données et termine le processus
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        # Retourne le texte chiffré et l'IV
        return {
            "ciphertext": ciphertext,
            "iv": iv
        }


    def encrypt_file(self, file_path):
        """Chiffre le contenu d'un fichier entier."""

        # Lit le fichier en octets
        with open(file_path, "rb") as f:
            file_bytes = f.read()

        # Crée un IV aléatoire de 16 octets
        iv = os.urandom(16)

        # Ajoute du padding pour que la taille soit multiple de 16
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(file_bytes) + padder.finalize()

        # Prépare l'objet AES-CBC
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv)
        )

        # Crée un outil pour chiffrer
        encryptor = cipher.encryptor()

        # Chiffre le contenu du fichier
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        # Retourne le fichier chiffré et l'IV
        return {
            "ciphertext": ciphertext,
            "iv": iv
        }


    # ── Déchiffrement ──

    def decrypt_text(self, ciphertext, iv):
        """Déchiffre un texte chiffré avec AES-CBC."""

        # Prépare AES-CBC avec la clé et l'IV utilisés pour le chiffrement
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv)
        )

        # Crée un outil pour déchiffrer
        decryptor = cipher.decryptor()

        # Déchiffre le ciphertext, résultat encore avec padding
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()

        # Enlève le padding pour récupérer le texte original
        unpadder = padding.PKCS7(128).unpadder()
        plaintext_bytes = unpadder.update(padded_data) + unpadder.finalize()

        # Convertit les octets en texte lisible
        return plaintext_bytes.decode("utf-8")


    def decrypt_file(self, ciphertext, iv):
        """Déchiffre le contenu d'un fichier chiffré avec AES-CBC."""

        # Prépare AES-CBC avec la clé et l'IV utilisés pour le chiffrement
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv)
        )

        # Crée un outil pour déchiffrer
        decryptor = cipher.decryptor()

        # Déchiffre le ciphertext, résultat encore avec padding
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()

        # Enlève le padding pour récupérer les octets originaux
        unpadder = padding.PKCS7(128).unpadder()
        return unpadder.update(padded_data) + unpadder.finalize()
