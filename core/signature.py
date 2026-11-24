# Importer la classe d'exception InvalidSignature
# Ceci est utilisé pour attraper quand la vérification d'une signature échoue
from cryptography.exceptions import InvalidSignature

# Importer les utilitaires de hachage et de sérialisation de la bibliothèque cryptography
# hashes: contient des algorithmes comme SHA256 pour créer des empreintes de messages
# serialization: utilisé pour convertir les clés vers/depuis le format PEM pour le stockage
from cryptography.hazmat.primitives import hashes, serialization

# Importer les utilitaires de rembourrage et RSA pour la cryptographie asymétrique
# padding: contient le schéma de rembourrage PSS pour les signatures sécurisées
# rsa: contient les fonctions pour générer et utiliser les clés RSA
from cryptography.hazmat.primitives.asymmetric import padding, rsa


class DigitalSignature:
    # Cette classe fournit toutes les fonctionnalités nécessaires pour signer et vérifier les signatures numériques en utilisant le chiffrement RSA
    # Les signatures numériques prouvent qu'un message provient d'une personne spécifique et n'a pas été modifié
    
    def __init__(self, key_size: int = 2048):
        # Méthode constructeur - s'exécute quand vous créez un nouvel objet DigitalSignature
        
        # Vérifier si le paramètre key_size est valide (doit être 2048 ou 4096 bits)
        # 2048 est plus rapide mais moins sécurisé, 4096 est plus lent mais plus sécurisé
        if key_size not in (2048, 4096):
            # Si invalide, arrêter et afficher un message d'erreur
            raise ValueError("key_size must be 2048 or 4096")
        
        # Enregistrer la key_size que l'utilisateur a choisie pour une utilisation ultérieure
        self.key_size = key_size
        
        # Initialiser private_key à None (vide)
        # Ceci stockera la clé secrète utilisée pour signer les messages
        # Nous la définissons à None car nous n'avons pas encore généré ou chargé une clé
        self.private_key = None
        
        # Initialiser public_key à None (vide)
        # Ceci stockera la clé publique utilisée pour vérifier les signatures
        # La clé publique est dérivée de la clé privée
        self.public_key = None
    
    def generate_key_pair(self) -> None:
        # Cette méthode crée une nouvelle paire de clés RSA (une clé privée + une clé publique)
        # La flèche (-> None) signifie que cette méthode ne retourne aucune valeur
        
        # Générer une nouvelle clé privée en utilisant l'algorithme RSA
        # Les paramètres expliqués:
        # - public_exponent=65537: C'est un nombre standard utilisé dans RSA (presque toujours 65537)
        # - key_size=self.key_size: Utiliser la taille en bits que nous avons enregistrée plus tôt (2048 ou 4096)
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.key_size
        )
        
        # Extraire la clé publique de la clé privée que nous venons de créer
        # La clé publique peut être partagée en toute sécurité avec n'importe qui, mais la clé privée doit rester secrète
        self.public_key = self.private_key.public_key()
    
    def sign_message(self, message: str) -> bytes:
        # Cette méthode crée une signature numérique pour un message
        # Entrée: message en tant que chaîne de caractères (texte brut)
        # Sortie: signature en tant que bytes (une longue série de nombres au format byte)
        
        # Vérifier si nous avons une clé privée chargée ou générée
        # Si non, nous ne pouvons pas signer car nous avons besoin de la clé privée pour créer des signatures
        if self.private_key is None:
            raise ValueError("Generate or load a private key first")
        
        # Convertir le message du texte (chaîne de caractères) en bytes en utilisant l'encodage UTF-8
        # Ceci est nécessaire car les fonctions cryptographiques fonctionnent avec des bytes, pas du texte
        # Exemple: "Hello" devient b'Hello'
        message_bytes = message.encode("utf-8")
        
        # Utiliser la clé privée pour signer le message
        # Nous appelons la méthode sign() sur notre objet clé privée
        # Trois choses principales que nous passons à la méthode sign:
        
        # 1. message_bytes: Le message réel que nous voulons signer (converti en bytes)
        signature = self.private_key.sign(
            message_bytes,
            
            # 2. padding.PSS(...): C'est le schéma de rembourrage (une façon d'ajouter des données supplémentaires pour la sécurité)
            # PSS est plus sécurisé que les anciennes méthodes comme PKCS#1 v1.5
            # - mgf=padding.MGF1(hashes.SHA256()): Ceci génère un rembourrage pseudo-aléatoire en utilisant SHA256
            # - salt_length=padding.PSS.MAX_LENGTH: Utiliser la longueur de salt maximale pour la sécurité maximale
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            
            # 3. hashes.SHA256(): L'algorithme de hachage à utiliser
            # SHA256 crée une "empreinte" unique du message
            hashes.SHA256(),
        )
        
        # Retourner la signature en tant que bytes
        return signature
    
    def verify_signature(self, message: str, signature: bytes) -> bool:
        # Cette méthode vérifie si une signature est valide pour un message donné
        # Entrée: message (le texte original) et signature (la signature à vérifier)
        # Sortie: True si valide, False si non valide (le type de retour est bool)
        
        # Vérifier si nous avons une clé publique chargée ou générée
        # Nous avons besoin de la clé publique pour vérifier les signatures
        if self.public_key is None:
            raise ValueError("Generate or load a public key first")
        
        # Utiliser un bloc try-except pour attraper les erreurs de vérification de signature
        try:
            # Essayer de vérifier la signature en utilisant la clé publique
            # Si la signature est valide pour ce message, cette ligne ne fait rien et nous continuons
            # Si la signature est NON valide, cette ligne lève une exception InvalidSignature
            self.public_key.verify(
                # Premier paramètre: les bytes de signature que nous vérifions
                signature,
                
                # Deuxième paramètre: le message original (converti en bytes)
                message.encode("utf-8"),
                
                # Troisième paramètre: le schéma de rembourrage (doit être EXACTEMENT le même que celui utilisé lors de la signature)
                # Si nous utilisons un rembourrage différent, la vérification échouera
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                
                # Quatrième paramètre: l'algorithme de hachage (doit être EXACTEMENT le même que celui utilisé lors de la signature)
                hashes.SHA256(),
            )
            
            # Si nous arrivons ici, la signature est valide (aucune exception n'a été levée)
            return True
        
        # Ceci capture l'exception InvalidSignature
        # Cela signifie que la signature NE CORRESPOND PAS au message
        except InvalidSignature:
            # Retourner False pour indiquer que la signature est invalide
            return False
    
    def save_private_key(self, file_path: str, password: str | None = None) -> None:
        # Cette méthode enregistre la clé privée dans un fichier sur le disque
        # La clé privée est très sensible et doit être protégée
        # 
        # Paramètres d'entrée:
        # - file_path: l'emplacement où nous voulons enregistrer le fichier (par exemple, "my_private_key.pem")
        # - password: mot de passe optionnel pour chiffrer la clé (utilisez None si vous ne voulez pas de mot de passe)
        
        # Vérifier si nous avons réellement une clé privée à enregistrer
        # Si non, arrêter et afficher une erreur
        if self.private_key is None:
            raise ValueError("No private key to save")
        
        # Décider si oui ou non de chiffrer la clé avec un mot de passe
        if password:
            # L'utilisateur a fourni un mot de passe, donc chiffrer la clé avec
            # Convertir le mot de passe du texte aux bytes avant de l'utiliser
            encryption = serialization.BestAvailableEncryption(password.encode("utf-8"))
        else:
            # Aucun mot de passe fourni, donc ne pas chiffrer la clé
            # AVERTISSEMENT: Cela signifie que le fichier de clé est stocké en texte brut (PAS SÉCURISÉ pour une utilisation réelle!)
            encryption = serialization.NoEncryption()
        
        # Convertir la clé privée au format PEM
        # PEM est un format de texte standard pour le stockage des clés (commence par -----BEGIN PRIVATE KEY-----)
        # Paramètres:
        # - encoding=serialization.Encoding.PEM: Utiliser le format PEM (format texte lisible)
        # - format=serialization.PrivateFormat.PKCS8: Utiliser la norme PKCS8 (format le plus compatible)
        # - encryption_algorithm=encryption: Appliquer le chiffrement que nous avons décidé ci-dessus
        pem_data = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=encryption,
        )
        
        # Ouvrir le fichier au chemin spécifié en mode écriture binaire
        # "wb" signifie write-binary (nous écrivons des bytes, pas du texte)
        # L'instruction 'with' ferme automatiquement le fichier quand c'est fait
        with open(file_path, "wb") as file:
            # Écrire les données PEM (la clé) dans le fichier
            file.write(pem_data)
    
    def save_public_key(self, file_path: str) -> None:
        # Cette méthode enregistre la clé publique dans un fichier
        # La clé publique est sûre à partager avec n'importe qui (elle n'est pas secrète)
        # Aucune protection par mot de passe n'est nécessaire car la clé publique n'est pas sensible
        #
        # Paramètre d'entrée:
        # - file_path: l'emplacement où nous voulons enregistrer le fichier (par exemple, "my_public_key.pem")
        
        # Vérifier si nous avons réellement une clé publique à enregistrer
        if self.public_key is None:
            raise ValueError("No public key to save")
        
        # Convertir la clé publique au format PEM (format texte standard lisible)
        # Paramètres:
        # - encoding=serialization.Encoding.PEM: Utiliser le format PEM (texte lisible)
        # - format=serialization.PublicFormat.SubjectPublicKeyInfo: Utiliser le format standard pour les clés publiques
        pem_data = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        
        # Ouvrir le fichier au chemin spécifié en mode écriture binaire
        with open(file_path, "wb") as file:
            # Écrire les données PEM (la clé publique) dans le fichier
            file.write(pem_data)
    
    def load_private_key(self, file_path: str, password: str | None = None) -> None:
        # Cette méthode charge une clé privée précédemment enregistrée depuis un fichier
        # Utilisez ceci pour utiliser une clé qui a été enregistrée avec save_private_key()
        #
        # Paramètres d'entrée:
        # - file_path: le chemin du fichier contenant la clé privée
        # - password: le mot de passe utilisé lors de l'enregistrement (le cas échéant). Doit correspondre exactement!
        
        # Ouvrir le fichier en mode lecture binaire
        # "rb" signifie read-binary (nous lisons des bytes)
        with open(file_path, "rb") as file:
            # Lire toutes les données du fichier (la clé au format PEM)
            key_data = file.read()
            
            # Charger la clé privée à partir des données PEM
            # Cette fonction détecte automatiquement le format et déchiffre si nécessaire
            # Si la clé est chiffrée, nous devons fournir le mot de passe correct
            self.private_key = serialization.load_pem_private_key(
                # Premier paramètre: les données de clé que nous venons de lire du fichier
                key_data,
                # Deuxième paramètre: le mot de passe (None s'il n'est pas chiffré)
                # Convertir le mot de passe en bytes s'il existe, sinon utiliser None
                password=password.encode("utf-8") if password else None
            )
        
        # Après avoir chargé la clé privée, calculer automatiquement la clé publique à partir de celle-ci
        # Ceci est sûr à faire car la clé publique est mathématiquement dérivée de la clé privée
        self.public_key = self.private_key.public_key()
    
    def load_public_key(self, file_path: str) -> None:
        # Cette méthode charge une clé publique précédemment enregistrée depuis un fichier
        # Utilisez ceci quand vous n'avez que la clé publique et que vous voulez vérifier les signatures
        #
        # Paramètre d'entrée:
        # - file_path: le chemin du fichier contenant la clé publique
        
        # Ouvrir le fichier en mode lecture binaire
        with open(file_path, "rb") as file:
            # Lire la clé publique au format PEM depuis le fichier
            key_data = file.read()
            
            # Charger la clé publique à partir des données PEM
            self.public_key = serialization.load_pem_public_key(key_data)


