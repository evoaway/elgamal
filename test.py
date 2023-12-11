import unittest
from elgamal import *

class TestStringMethods(unittest.TestCase):
    def test_correct_verify(self):
        # we create 32-bit keys and generate a random g,
        # NOTE that in this case a bigger key length slows the program down a lot
        message = "Hello World. What's up?"
        private_key, public_key = generate_keys(32, True)
        r, s = sign(message, private_key)
        self.assertTrue(verify(message, r, s, public_key))

    def test_correct_verify_2(self):
        # default parameters are used for key generation: 256-bit key size and fixed g = 2
        # NOTE it is recommended to use keys of size 2048, but in this case the program will run very slowly
        message = "ElGamal signature scheme"
        private_key, public_key = generate_keys()
        r, s = sign(message, private_key)
        self.assertTrue(verify(message, r, s, public_key))

    def test_incorrect_key_verify(self):
        message = "What happened?"
        private_key, public_key = generate_keys()
        private_key2, public_key2 = generate_keys()
        r, s = sign(message, private_key)
        self.assertFalse(verify(message, r, s, public_key2))

    def test_incorrect_message_verify(self):
        message = "I'm Ok"
        private_key, public_key = generate_keys()
        r, s = sign(message, private_key)
        message2 = "I feel bad"
        self.assertFalse(verify(message2, r, s, public_key))

if __name__ == '__main__':
    unittest.main()