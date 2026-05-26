from hashlib import sha256

def hash_bytes(data: bytes) -> str:
    return sha256(data).hexdigest()