import unittest, tempfile, hashlib
from pathlib import Path
from cryptography.exceptions import InvalidTag
from core import toolkit as t
from core.asymmetric import AsymmetricCipher
from core.signature import DigitalSignature
class TestToolkit(unittest.TestCase):
    def test_aes(self):
        k='01'*32; token=t.encrypt_text(k,'hello'); self.assertEqual(t.decrypt_text(k,token),'hello'); self.assertNotEqual(token,t.encrypt_text(k,'hello'))
        with self.assertRaises(InvalidTag): t.decrypt_text('02'*32,token)
    def test_hash(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'sample'; p.write_bytes(b'abc'); self.assertEqual(t.file_digest(p),hashlib.sha256(b'abc').hexdigest()); self.assertEqual(t.digest(b'abc'),t.file_digest(p))
    def test_rsa(self):
        c=AsymmetricCipher(); c.generer_cles(); self.assertEqual(c.dechiffrer(c.chiffrer('hello')),'hello')
    def test_signature(self):
        s=DigitalSignature(); s.generate_key_pair(); sig=s.sign_message('hello'); self.assertTrue(s.verify_signature('hello',sig)); self.assertFalse(s.verify_signature('changed',sig))
    def test_certificate(self):
        _,pem=t.generate_certificate('lab.example'); self.assertIn('CN=lab.example',t.inspect_certificate(pem))
