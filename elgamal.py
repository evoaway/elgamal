from mathfunc import *
from random import randint
from hashlib import sha256


class PrivateKey(object):
    r"""Class defining an ElGamal private key.
    Do not instantiate directly.
    Use :func:`generate_keys`.

    :ivar p: Modulus
    :vartype p: integer

    :ivar g: Generator
    :vartype g: integer

    :ivar a: Private key component
    :vartype a: integer

    :ivar bits: Key size in bits
    :vartype bits: integer
    """

    def __init__(self, p=None, g=None, a=None, bits=None):
        self.p = p
        self.g = g
        self.a = a
        self.bits = bits


class PublicKey(object):
    r"""Class defining an ElGamal public key.
    Do not instantiate directly.
    Use :func:`generate_keys`.

    :ivar p: Modulus
    :vartype p: integer

    :ivar g: Generator
    :vartype g: integer

    :ivar b: Public key component
    :vartype b: integer

    :ivar bits: Key size in bits
    :vartype bits: integer
    """

    def __init__(self, p=None, g=None, b=None, bits=None):
        self.p = p
        self.g = g
        self.b = b
        self.bits = bits


def generate_keys(length=256, generate_root=False):
    """ Randomly generates private and public keys

        Args:
        length -- int -- key size in bits
        generate_root -- bool -- flag for random generation g (primitive root) if false,
        g defaults to a fixed value of 2 for simplicity

        Return:
        tuple of two objects :class:`PrivateKey` and :class:`PublicKey`
    """
    p = generate_prime_number(length)
    if generate_root:
        g = find_primitive(p)
    else:
        g = 2
    a = randint(1, p - 1)
    b = pow(g, a, p)
    return PrivateKey(p, g, a, length), PublicKey(p, g, b, length)


def sign(m, private_key, hash_func=sha256):
    hash_num = int_from_hex(hash_func(m.encode()).hexdigest())
    while 1:
        k = randint(2, private_key.p - 1)
        if gcd(k, private_key.p - 1) == 1:
            break
    r = pow(private_key.g, k, private_key.p)
    s = ((hash_num - private_key.a * r) * pow(k, -1, private_key.p - 1)) % (private_key.p - 1)
    return r, s


def verify(m, r, s, public_key, hash_func=sha256):
    if 0 < r < public_key.p and 0 < s < public_key.p - 1:
        hash_num = int_from_hex(hash_func(m.encode()).hexdigest())
        v1 = (pow(public_key.b, r, public_key.p) * pow(r, s, public_key.p)) % public_key.p
        v2 = pow(public_key.g, hash_num, public_key.p)
        return v1 == v2
    return False


def encrypt(m, public_key):
    y = []
    chunks, chunk_size = len(m), public_key.bits // 8
    enc_msg = [m[i:i + chunk_size] for i in range(0, chunks, chunk_size)]
    k = randint(1, public_key.p - 1)
    x = pow(public_key.g, k, public_key.p)
    for i in enc_msg:
        plaintext = int.from_bytes(i.encode(), 'big')
        y.append((plaintext * pow(public_key.b, k, public_key.p)) % public_key.p)
    return x, y


def decrypt(cipher_text, private_key):
    x, m = cipher_text
    message = []
    s = pow(x, private_key.a, private_key.p)
    for i in m:
        plaintext = (i * pow(s, -1, private_key.p)) % private_key.p
        message.append(plaintext.to_bytes((plaintext.bit_length() + 7) // 8, 'big').decode())
    return ''.join(message)


def int_from_hex(hexadecimal):
    return int(hexadecimal, 16)
