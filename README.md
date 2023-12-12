# About
Implementation of ElGamal [encryption](https://en.wikipedia.org/wiki/ElGamal_encryption) and [signature scheme](https://en.wikipedia.org/wiki/ElGamal_signature_scheme).

# Description
The El-Gamal scheme is a public-key cryptographic system based on the complexity of computing discrete logarithms in a finite field.
### Key generation
There is a `generate_keys(length=256, generate_root=False)` function to generate a pair of keys. It uses  the [Miller-Rabin algorithm](https://medium.com/@ntnprdhmm/how-to-generate-big-prime-numbers-miller-rabin-49e6e6af32fb) to find a prime number 
and [this algorithm (from GeeksforGeeks)](https://www.geeksforgeeks.org/primitive-root-of-a-prime-number-n-modulo-n/) to choose `g` as the primitive root of `p`. Note:
* By default, a key size of 256 bits is used because finding  for large prime numbers takes a long time
* By default, the value `g`=2 is fixed, because the find for a primitive root for a large prime number takes a long time.
However, the user can specify the `True` parameter to generate the root.\

How to use:
* generate 32-bits keys and generate `g`
```python
private_key, public_key = generate_keys(32, True)
```
* generate 256-bits and use fixed `g` = 2
```python
private_key, public_key = generate_keys(256)
```
### Signature
Message and private key are used to sign the message. The message digest is calculated using a hash function (SHA-256 by default).
Choose an integer `k` randomly then compute `r` and `s`. So the signature of the message `M` is the pair `(r, s)`\
The public key, signature `(r,s)`, and message are passed for verification.\
To sign and verify a message do
```python
message = "ElGamal signature scheme"
private_key, public_key = generate_keys()
r, s = sign(message, private_key)
ver = verify(message, r, s, public_key)
```
### Encryption
The public key is used for encryption. Choose an integer `k` randomly then compute `a` and `b`.
So the pair of numbers `(a,b)` is a ciphertext.\
To encrypt and decrypt a message do
```python
message = "Plain text"
private_key, public_key = generate_keys()
enc_message = encrypt(message, public_key)
dec_message = decrypt(enc_message, private_key)
```