"""Local cryptographic utilities. No network access or persistence of secrets."""
import base64
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

AAD = b'crypto-toolkit:v1'

def encrypt_text(key_hex, text):
    key = bytes.fromhex(key_hex)
    if len(key) != 32: raise ValueError('Use a 256-bit key (64 hex characters).')
    nonce = secrets.token_bytes(12)
    return base64.b64encode(nonce + AESGCM(key).encrypt(nonce, text.encode(), AAD)).decode()

def decrypt_text(key_hex, token):
    key = bytes.fromhex(key_hex)
    if len(key) != 32: raise ValueError('Use a 256-bit key (64 hex characters).')
    raw = base64.b64decode(token, validate=True)
    if len(raw) < 28: raise ValueError('Invalid ciphertext.')
    return AESGCM(key).decrypt(raw[:12], raw[12:], AAD).decode()

def digest(data, algorithm='sha256'):
    return hashlib.new(algorithm, data).hexdigest()

def file_digest(path, algorithm='sha256'):
    obj = hashlib.new(algorithm)
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''): obj.update(chunk)
    return obj.hexdigest()

def inspect_certificate(data):
    cert = x509.load_pem_x509_certificate(data) if b'-----BEGIN CERTIFICATE-----' in data else x509.load_der_x509_certificate(data)
    now = datetime.now(timezone.utc)
    return '\n'.join([f'Subject: {cert.subject.rfc4514_string()}', f'Issuer: {cert.issuer.rfc4514_string()}', f'Serial: {cert.serial_number:X}', f'Valid from: {cert.not_valid_before_utc}', f'Valid until: {cert.not_valid_after_utc}', f'Within validity period: {cert.not_valid_before_utc <= now <= cert.not_valid_after_utc}', f'SHA-256 fingerprint: {cert.fingerprint(hashes.SHA256()).hex()}', 'Trust chain and hostname are NOT verified.'])

def generate_certificate(domain):
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, domain)])
    now = datetime.now(timezone.utc)
    cert = (x509.CertificateBuilder().subject_name(name).issuer_name(name).public_key(key.public_key()).serial_number(x509.random_serial_number()).not_valid_before(now).not_valid_after(now+timedelta(days=30)).add_extension(x509.BasicConstraints(ca=False,path_length=None),critical=True).add_extension(x509.SubjectAlternativeName([x509.DNSName(domain)]),critical=False).sign(key,hashes.SHA256()))
    return key, cert.public_bytes(serialization.Encoding.PEM)
