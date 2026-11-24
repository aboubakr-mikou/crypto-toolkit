from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

class AsymmetricCipher:
    def __init__(self):
        self.cle_privee=None
        self.cle_publique=None

    def generer_cles(self):
        self.cle_privee=rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.cle_publique=self.cle_privee.public_key()

    def chiffrer(self,message):
        message_bytes=message.encode('utf-8')
        message_chiffre=self.cle_publique.encrypt(
            message_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return message_chiffre.hex()

    def dechiffrer(self,message_chiffreHex):
        message_chiffre=bytes.fromhex(message_chiffreHex)
        message_dechiffre=self.cle_privee.decrypt(
            message_chiffre,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return message_dechiffre.decode('utf-8')

    def sauvegarder_cle_privee(self,chemin):
        with open(chemin,'wb') as f:
            f.write(self.cle_privee.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))

    def sauvegarder_cle_publique(self,chemin):
        with open(chemin,'wb') as f:
            f.write(self.cle_publique.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

    def charger_cle_privee(self,chemin):
        with open(chemin,'rb') as f:
            self.cle_privee=serialization.load_pem_private_key(
                f.read(),
                password=None
            )
            self.cle_publique=self.cle_privee.public_key()

    def charger_cle_publique(self,chemin):
        with open(chemin,'rb') as f:
            self.cle_publique=serialization.load_pem_public_key(
                f.read()
            )
