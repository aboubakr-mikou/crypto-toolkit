import hashlib

class HashManager :
    def __init__(self):
        self.algorithme="sha256"

    def generer_hash(self,message):
        message_bytes=message.encode('utf-8')
        resultat=hashlib.sha256(message_bytes).hexdigest()
        return resultat
    
    def comparer_hash(self,hash1,hash2):
        return hash1 == hash2
    
    def verifier_integrite(self,message,hashOriginal):
        hashActuel=self.generer_hash(message)
        return self.comparer_hash(hashActuel,hashOriginal)
    