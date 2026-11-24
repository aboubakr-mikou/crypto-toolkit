from core.asymmetric import AsymmetricCipher
from core.hashing import HashManager
from core.symmetric import SymmetricCipher
from core.signature import DigitalSignature
from core.certificate import CertificateManager

cipher= AsymmetricCipher()
hasher=HashManager()
aes=SymmetricCipher()
signature=DigitalSignature()
cm=CertificateManager()

#test de rsa
print("====Test de RSA:====")
cipher.generer_cles()
print("Cles generees !")

chiffre=cipher.chiffrer("Bonjour RSA !")
print("Message chiffre :",chiffre[:40],"...")

dechiffre=cipher.dechiffrer(chiffre)
print("Messafe dechiffre :",dechiffre)

#test de SHA-256
print("====Tets de SHA-256====")
hash1=hasher.generer_hash("Bonjour !")
print("Hash genere :",hash1)
resultathash=hasher.verifier_integrite("Bonjour !",hash1)
print("Message non altere ?",resultathash)
resultathash2=hasher.verifier_integrite("Bonjoor !",hash1)
print("Message non altere ?",resultathash2)

#test de AES
print("====Test de AES:====")
aes.generate_key()
print("Cle Genere:",aes.get_key_hex()[:20],"...")
resultatAes=aes.encrypt_text("Salut c est AES")
print("Message chiffre:",resultatAes["ciphertext"].hex()[:20],"...")
resultatAes2=aes.decrypt_text(resultatAes["ciphertext"],resultatAes["iv"])
print("Message dechiffre:",resultatAes2)

#Test de sifnature
print("====Test de Signature:====")
signature.generate_key_pair()
print("Cles generees !")
signature1=signature.sign_message("Hello signature")
print("Message signe :",signature1.hex()[:20],"...")
valide=signature.verify_signature("Hello signature",signature1)
print("Signature valide :",valide)
modifie=signature.verify_signature("Bonjour signature :",signature1)
print("Signature invalide :",modifie)

#test certificats
print("====Test Certificats:====")
resultatCert=cm.generate_self_signed_certificate("google.com")
print("Resultat:",resultatCert)
info=cm.display_certificate_info()
print("Infos Certificat :")
for k,v in info.items():
    print(" ", k,":",v)
