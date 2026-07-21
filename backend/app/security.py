"""Password hashing — PBKDF2-HMAC-SHA256 (ported from AIMS portal helpers)."""
import binascii
import hashlib
import hmac
import os

_PBKDF2_ITERS = 200_000


def hash_password(password: str) -> tuple[str, str]:
    """Return (pbkdf2_hex, salt_hex). Salt is 16 random bytes encoded as hex."""
    salt = os.urandom(16).hex()
    h = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), _PBKDF2_ITERS)
    return binascii.hexlify(h).decode(), salt


def verify_password(password: str, stored_hash: str, salt: str) -> bool:
    h = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), _PBKDF2_ITERS)
    return hmac.compare_digest(binascii.hexlify(h).decode(), stored_hash)
