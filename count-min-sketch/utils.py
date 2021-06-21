import hashlib


def available_hash_functions():
    fns = [hashlib.sha3_512, hashlib.blake2s, hashlib.md5, hashlib.sha256, hashlib.sha384, hashlib.blake2b, hashlib.sha3_224, hashlib.sha3_384, hashlib.sha512, hashlib.sha1, hashlib.sha224, hashlib.sha3_256]
    return fns
