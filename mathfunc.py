from random import randrange, getrandbits
from math import sqrt

def gcd(a, b):
    while b != 0:
        c = a % b
        a = b
        b = c
    return a
def is_prime(n, k=128):
    """ Test if a number is prime

        Args:
            n -- int -- the number to test
            k -- int -- the number of tests to do

        Return:
        True if n is prime
    """
    # Test if n is not even.
    # But care, 2 is prime !
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    # find r and s
    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2
    # do k tests
    for _ in range(k):
        a = randrange(2, n - 1)
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False
    return True


def generate_prime_candidate(length):
    """ Generate an odd integer randomly

        Args:
        length -- int -- the length of the number to generate, in bits

        Return:
        an integer
    """
    # generate random bits
    p = getrandbits(length)
    # apply a mask to set MSB and LSB to 1
    p |= (1 << length - 1) | 1
    return p

# find n-bits prime number
# this implementation uses the Miller-Rabin algorithm and is described in detail here:
# https://medium.com/@ntnprdhmm/how-to-generate-big-prime-numbers-miller-rabin-49e6e6af32fb
def generate_prime_number(length=256):
    """ Generate a prime

        Args:
        length -- int -- length of the prime to generate, in bits

        Return:
        a prime number
    """
    while 1:
        p = generate_prime_candidate(length)
        if is_prime(p, 8):
            return p


def find_primefactors(s, n):
    # Print the number of 2s that divide n
    while (n % 2 == 0):
        s.add(2)
        n = n // 2

    # n must be odd at this point. So we can
    # skip one element (Note i = i +2)
    for i in range(3, int(sqrt(n)), 2):

        # While i divides n, print i and divide n
        while (n % i == 0):
            s.add(i)
            n = n // i

        # This condition is to handle the case
    # when n is a prime number greater than 2
    if (n > 2):
        s.add(n)

    # Function to find the smallest primitive


# find the number of primitive roots modulo prime
# this algorithm is described in detail here:
# https://www.geeksforgeeks.org/find-the-number-of-primitive-roots-modulo-prime/
def find_primitive(n):
    s = set()

    # Check if n is prime or not
    if (is_prime(n) == False):
        return -1

    # Find value of Euler Totient function
    # of n. Since n is a prime number, the
    # value of Euler Totient function is n-1
    # as there are n-1 relatively prime numbers.
    phi = n - 1

    # Find prime factors of phi and store in a set
    find_primefactors(s, phi)

    # Check for every number from 2 to phi
    for r in range(2, phi + 1):

        # Iterate through all prime factors of phi.
        # and check if we found a power with value 1
        flag = False
        for it in s:

            # Check if r^((phi)/primefactors)
            # mod n is 1 or not
            if (pow(r, phi // it, n) == 1):
                flag = True
                break

        # If there was no power with value 1.
        if (flag == False):
            return r

        # If no primitive root found
    return -1