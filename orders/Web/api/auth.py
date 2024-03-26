import jwt
import os
import requests
from cryptography.x509 import load_pem_x509_certificate

X509_CERT_TEMPLATE = \
    "-----BEGIN CERTIFICATE-----\n{key}\n-----END CERTIFICATE-----"

publick_keys = requests.get(
    os.environ["AUTH_WELL_KNOWN_URL"]
).json()["keys"]

def _get_certificate_for_kid(kid):
    for key in publick_keys:
        if key["kid"] == kid:
            return key["x5c"][0]
    raise Exception(f"Key not found for kid: {kid}")

def load_public_key_from_x509_cert(certificate):
    return load_pem_x509_certificate(certificate).public_key()
    

def decode_and_validate_token(access_token):
    """
    アクセストークンを検証。トークンが有効な場合はトークンペイロードを返す
    """
    unverified_header = jwt.get_unverified_header(access_token)
    x509_cetificate = _get_certificate_for_kid(unverified_header["kid"])
    publick_key = load_public_key_from_x509_cert(X509_CERT_TEMPLATE.format(key=x509_cetificate).encode("utf-8"))
    
    return jwt.decode(
        access_token,
        key=publick_key,
        algorithms=unverified_header["alg"],
        audience=[
                "http://127.0.0.1:8000/orders",
                os.environ["AUTH_USERINFO_URL"]
                ]
    )