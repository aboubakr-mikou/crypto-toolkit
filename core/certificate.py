from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import datetime
import os
import hashlib
import time

class CertificateManager:

    def generate_self_signed_certificate(self, common_name="example.com"):

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "MA"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "ENSAF"),
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
        ])

        cert = x509.CertificateBuilder()\
            .subject_name(subject)\
            .issuer_name(issuer)\
            .public_key(private_key.public_key())\
            .serial_number(x509.random_serial_number())\
            .not_valid_before(datetime.datetime.utcnow())\
            .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))\
            .sign(private_key, hashes.SHA256())

        with open("private_key.pem", "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))

        with open("certificate.pem", "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))

        return "Certificate generated successfully"


    def display_certificate_info(self, cert_path="certificate.pem"):

        with open(cert_path, "rb") as f:
            cert = x509.load_pem_x509_certificate(f.read())

        info = {
            "Subject": cert.subject.rfc4514_string(),
            "Issuer": cert.issuer.rfc4514_string(),
            "Serial Number": cert.serial_number,
            "Valid From": cert.not_valid_before,
            "Valid Until": cert.not_valid_after
        }

        return info


if __name__ == "__main__":

    cm = CertificateManager()

    print(cm.generate_self_signed_certificate())

    info = cm.display_certificate_info()

    print("\nCertificate Information:")
    for k, v in info.items():
        print(k, ":", v)